import asyncio
import aiohttp
from bs4 import BeautifulSoup, Tag
import re
import json
import os


url = 'https://www.otzyvua.net/cherniy-spisok-pokupateley-nedobrosovestnye-pokupateli'


async def get_page(page: int, session: aiohttp.ClientSession) -> int:
    count = 0
    async with session.get(url + f'?page={page}') as response:
        soup = BeautifulSoup(await response.text(), 'lxml')
        comment_tags = soup.find('div', id='comments_container').find_all(
            'div', class_='commentbox')
        if comment_tags == None:
            return count
        comments = [parse_comment(comment_tag)
                    for comment_tag in comment_tags]

        for comment in comments:
            if os.path.exists(f"otzyvua/{comment['id']}.json"): return count
            with open(f"otzyvua/{comment['id']}.json", 'w', encoding='utf-8') as file:
                count += 1
                file.write(json.dumps(
                    comment, indent=4, ensure_ascii=False))

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
        title = h2.find('a').text.strip() if h2 else 'no title'
        text = (tag.find('span', class_='review-full-text')
                or tag.find('span', class_='review-snippet')).text.strip()

        a = tag.find('div', class_='advantages')
        advantages = [t.text.strip()
                      for t in a.find('ol').find_all('li')] if a else None

        d = tag.find('div', class_='disadvantages')
        disadvantages = [t.text.strip()
                         for t in d.find('ol').find_all('li')] if d else None

        i = tag.find('div', class_='hs-image')
        images = [a.attrs['href'] for a in i.find_all('a')] if i else None
        return {
            'id': tag.attrs['id'].strip(),
            'title': title,
            'date': tag.find('span', class_='value-title').attrs['title'].strip(),
            'text': text,
            'phone': search_phone(title + ' ' + text),
            'advantages': advantages,
            'disadvantages': disadvantages,
            'images': images,
        }
    except Exception as err:
        print(f"Error parsing comment - {tag}")
        raise err.with_traceback()


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
