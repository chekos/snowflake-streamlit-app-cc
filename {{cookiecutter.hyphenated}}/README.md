# {{ cookiecutter.app_name }}

{{ cookiecutter.app_description }}

### Directory Structure

```plaintext
.
├── README.md
├── .python-version
├── app.py
├── pyproject.toml
├── snowflake.yml
├── utils
│   ├── data.py
│   └── helpers.py
├── .streamlit/
│   └── secrets-example.toml    <- update this and rename to secrets.toml
└── pages/                      <- if you selected multi page
```

* `app.py`: The main entry point for the Streamlit app.
* `utils/helpers.py`: Helper functions to retrieve Snowflake sessions for both local development and deployment.
* `utils/data.py`: Placeholder file for data-specific helper functions.
* `snowflake.yml`: Configuration file for deploying the app to Snowflake.
* `environment.yml`: Manage packages. Read more in the [docs](https://docs.snowflake.com/en/developer-guide/streamlit/create-streamlit-sql#manage-packages-by-using-the-environment-yml-file).
* `pyproject.toml`: Python project dependencies and setup configuration.
* `uv.lock`: Environment lock file for Astral's `uv` tool.
* `.python-version`: Specifies the python version for `uv` to use. Simply "3.11". Snowflake supports only python 3.8-3.11 as of Sept. 2024 [docs](https://docs.snowflake.com/en/developer-guide/snowpark/python/setup#prerequisites).

## Prerequisites
* Snowflake account
* Astral's `uv` tool for managing Python environments. More information can be found in the official documentation at [docs.astral.sh/uv](https://docs.astral.sh/uv/#getting-started)
* If you would like to deploy apps directly (not through the CI/CD pipeline), you will need to have the Snowflake CLI installed and a `~/.snowflake/connections.toml` file in your local machine. For more information visit the [official documentation](https://docs.snowflake.com/en/developer-guide/snowflake-cli-v2/index#what-s-in-this-guide).

## Getting started
To run the app locally, you need to store Snowflake connection details in a `.streamlit/secrets.toml` file in the root directory of the project.

The file looks like this:
```toml
[snowflake]
accountname = "accountname"
username = "username"
role = "role"
warehouse = "warehousename"
database = "databasename"
schema = "schemaname"
private_key_path = "/path/to/private_key.pem"
private_key_passphrase = "passphrase"
session_parameters.query_tag = "streamlit"
```

### Running the App locally
You can use `uv` to run commands and automatically pick up the virtual environment by using `uv run <command>`. In this case:
```bash
uv run streamlit run app.py
```

This is the equivalent of activating the virtual environment and running `streamlit run app.py`

```bash
source .venv/bin/activate
streamlit run app.py
```
