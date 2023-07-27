import asyncio
import aiohttp

from app.resources.otzyvua.parser_otzyvua import run_parser
from app.resources.otzyvua.db_api import insert_data_to_db


async def main():

    # await db_create_tables()
    await run_parser()
    # await insert_data_to_db_from_files(tablename='otzyvua', dirname='otzyvua')
    # await insert_data_to_db('app/resources/otzyvua/files')


if __name__ == '__main__':
    asyncio.run(main())
