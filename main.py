import asyncio
import aiohttp

from app.data.db_api import db_create_tables, insert_data_to_db_from_files
from app.service.parser_otzyvua import run_parser


async def main():

    await db_create_tables()
    async with aiohttp.ClientSession() as session:
        await run_parser(session)
    await insert_data_to_db_from_files(tablename='otzyvua', dirname='otzyvua')


if __name__ == '__main__':
    asyncio.run(main())
