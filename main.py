import asyncio

from app.resources.otzyvua.parser_otzyvua import run_parser


async def main():

    await run_parser()



if __name__ == '__main__':
    asyncio.run(main())
