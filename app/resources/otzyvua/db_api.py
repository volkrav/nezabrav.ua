from app.resources.otzyvua.utils import get_dict_from_json_files
from app.resources.otzyvua.dao import OtzyvuaDAO


async def insert_data_to_db(dirname: str):
    print(await OtzyvuaDAO.find_by_id('comment12864022'))
    # async for data in get_dict_from_json_files(dirname):
    #     comment = await OtzyvuaDAO.add(**data)
    #     print(comment)
    #     break


# from app.data.db_utils import insert_to_table_from_dict
# from app.database import UseDataBase
# from app.resources.otzyvua.utils import get_dict_from_json_files


# async def db_create_tables():
#     try:
#         async with UseDataBase() as conn:
#             with open('app/data/init.sql', 'r') as f:
#                 sql = f.read()
#             await conn.execute(sql)
#     except OSError:
#         print(f'cannot connect to database')
#     except Exception as err:
#         print(f'get {err.args}')


# async def insert_data_to_db() -> None:
#     async with UseDataBase() as conn:
#         await insert_to_table_from_dict(tablename='other_table',
#                                         column_values={
#                                             'key1': 'val1',
#                                             'key2': 'val2'
#                                         },
#                                         conn=conn)


# async def insert_data_to_db_from_files(tablename: str, dirname: str) -> None:
#     async with UseDataBase() as conn:
#         async for data in get_dict_from_json_files(dirname):
#             await insert_to_table_from_dict(tablename=tablename,
#                                             column_values=data,
#                                             conn=conn)
