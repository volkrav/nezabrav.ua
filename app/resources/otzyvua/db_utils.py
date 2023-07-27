# from asyncpg import Connection


# async def insert_to_table_from_dict(tablename: str, column_values: dict, conn: Connection):
#     columns = ', '.join(column_values.keys())
#     values = tuple(column_values.values())
#     placeholders = ', '.join(f'${i}' for i in range(1, len(column_values.keys())+1))
#     try:
#         await conn.execute(
#             f'INSERT INTO {tablename} '
#             f'({columns}) '
#             f'VALUES '
#             f'({placeholders})'
#             f'ON CONFLICT DO NOTHING;',
#             *values
#         )
#         # logger.info(
#         #     f'inserting "{values[0]}" into a "{tablename}"'
#         # )
#         print(
#             f'inserting "{values[0]}" into a "{tablename}"'
#         )
#     except OSError:
#         # raise ConnectionErrorDB()
#         print("ConnectionErrorDB()")
#     except Exception as err:
#         # logger.error(
#         #     f'get {err.args}'
#         # )
#         print(f'get {err.args}')
