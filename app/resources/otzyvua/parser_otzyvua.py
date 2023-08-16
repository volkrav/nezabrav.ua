import asyncio
from datetime import datetime
import enum
import json
import os
import re

import aiohttp
from bs4 import BeautifulSoup, Tag

from app.reports.dao import ReportsDAO

from app.reports.models import ESource


url = 'https://www.otzyvua.net/cherniy-spisok-pokupateley-nedobrosovestnye-pokupateli'
pathdir = 'app/resources/otzyvua/files'


async def get_page(page: int, session: aiohttp.ClientSession) -> int:
    count = 0
    async with session.get(url + f'?page={page}') as response:
        soup = BeautifulSoup(await response.text(), 'lxml')
        comment_tags = soup.find('div', id='comments_container').find_all(
            'div', class_='commentbox')
        if comment_tags == None:
            return count
        comments = []
        for comment_tag in comment_tags:
            for comment in parse_comment(comment_tag):
                if comment:
                    comments.append(comment)


        for comment in comments:
            if not os.path.exists(f"{pathdir}/{comment['ext_id']}.json"):
                with open(f"{pathdir}/{comment['ext_id']}.json", 'w', encoding='utf-8') as file:
                    file.write(json.dumps(
                        comment, indent=4, ensure_ascii=False, default=str))
            if await ReportsDAO.find_one_or_none(ext_id=comment['ext_id']):
                return count
            count += 1
            await ReportsDAO.add(**comment)

    return count


async def crawl(session: aiohttp.ClientSession):
    total = 0
    for i in range(1, 500):
        res = await get_page(i, session)
        if res == 0:
            break
        total += res
        print(f"parsed {res} comments on page {i}")
    print(f"total parsed {total} comments")


def parse_comment(tag: Tag):
    try:
        h2 = tag.find('h2')
        title = h2.find('a').text.strip() if h2 else ''
        str_date = tag.find('span', class_='value-title').attrs['title'].strip()
        date = datetime.strptime(str_date, '%Y-%m-%d')

        text_with_newlines = (tag.find('span', class_='review-full-text')
                or tag.find('span', class_='review-snippet'))
        if text_with_newlines.find('br'):
            text = ''
            for e in text_with_newlines.descendants:
                if isinstance(e, str):
                    text += e.strip()
                elif e.name == 'br':
                    text += '\n'
        else:
            text = text_with_newlines.text.strip()

        phone = search_phone(title + ' ' + text)
        if not phone:
            return None

        a = tag.find('div', class_='advantages')
        advantages = [t.text.strip()
                      for t in a.find('ol').find_all('li')] if a else []

        d = tag.find('div', class_='disadvantages')
        disadvantages = [t.text.strip()
                         for t in d.find('ol').find_all('li')] if d else []

        report = '\n'.join([title, text] + advantages + disadvantages)

        i = tag.find('div', class_='hs-image')
        images = [a.attrs['href'] for a in i.find_all('a')] if i else None
        yield {
            'ext_id': tag.attrs['id'].strip(),
            'source': ESource.otzyvua,
            'created': date,
            'updated': date,
            'phone': phone,
            'report': report,
            'images': images,
        }
    except Exception as err:
        print(f"Error parsing comment - {tag}")
        raise err


def search_phone(s: str) -> str:
    regex = r'(38)?(\d{3})\D{0,4}(\d{3})\D{0,3}(\d{2})\D{0,3}(\d{2})'
    match = re.search(regex, s)
    if match == None:
        return None
    return ''.join(match.group(2, 3, 4, 5))


async def run_parser():
        async with aiohttp.ClientSession() as session:
            await crawl(session)


if __name__ == '__main__':
    asyncio.run(run_parser())
