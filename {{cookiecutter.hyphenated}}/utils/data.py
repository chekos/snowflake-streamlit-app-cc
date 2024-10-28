from .helpers import get_snowflake_session


def get_table(table_name: str):
    session = get_snowflake_session()
    table = session.table(table_name)
    return table
