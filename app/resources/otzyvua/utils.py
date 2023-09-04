import asyncio
import json
import os
from datetime import datetime
from typing import Any, Dict, Generator


# working with files
async def get_dict_from_json_files(dirname: str) -> Generator[Dict, Any, None]:
    loop = asyncio.get_running_loop()
    async for filename in _get_file_from_dir(dirname):
        yield await loop.run_in_executor(None,
                                         _sync_open_file_for_read,
                                         dirname,
                                         filename,
                                         )


async def _get_file_from_dir(dirname: str) -> Generator[str, Any, None]:
    for filename in os.listdir(dirname):
        yield filename


def _sync_open_file_for_read(dirname: str, filename: str) -> Dict:
    with open(os.path.join(dirname, filename), encoding='utf8') as data:
        comment = json.loads(data.read())
        comment['date'] = datetime.strptime(
            comment['date'], '%Y-%m-%d %H:%M:%S')
        return comment
