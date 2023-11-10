import asyncio

from app.resources.otzyvua.parser_otzyvua import run_parser
from app.resources.novaposhta.api import get_tracking_from_novaposhta


async def main():

    await run_parser()
    # await get_tracking_from_novaposhta('59001019981517', '380999696104')



if __name__ == '__main__':
    asyncio.run(main())
