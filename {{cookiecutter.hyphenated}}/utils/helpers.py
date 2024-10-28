from pathlib import Path

import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session

local_secrets = Path(__file__).parent.parent / ".streamlit" / "secrets.toml"


def get_snowflake_session():
    if local_secrets.exists():
        session = Session.builder.configs(
            {
                "account": st.secrets.snowflake.account,
                "user": st.secrets.snowflake.user,
                "private_key_file": st.secrets.snowflake.private_key_file,
                "private_key_file_pwd": st.secrets.snowflake.private_key_file_pwd,
                "role": st.secrets.snowflake.role,
                "warehouse": st.secrets.snowflake.warehouse,
                "database": st.secrets.snowflake.database,
                "schema": st.secrets.snowflake.schema,
            }
        ).create()
    else:
        session = get_active_session()

    return session
