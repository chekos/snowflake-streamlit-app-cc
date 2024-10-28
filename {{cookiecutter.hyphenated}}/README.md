# {{ cookiecutter.app_name }}

## Streamlit App Deployment to Snowflake

This repository provides an example setup for deploying Streamlit apps to Snowflake using the Snowflake CLI tool and Astral's uv tool to manage Python environments.

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
* `.gitlab-ci.yml`: Optional CI/CD pipeline configuration for GitLab (if applicable).
* `pyproject.toml`: Python project dependencies and setup configuration.
* `uv.lock`: Environment lock file for Astral's `uv` tool.
* `.python-version`: Specifies the python version for `uv` to use. Simply "3.11". Snowflake supports only python 3.8-3.11 as of Sept. 2024 [docs](https://docs.snowflake.com/en/developer-guide/snowpark/python/setup#prerequisites).

## Prerequisites
* Snowflake account
* Astral's `uv` tool for managing Python environments. More information can be found in the official documentation at [docs.astral.sh/uv](https://docs.astral.sh/uv/#getting-started)
* If you would like to deploy apps directly (not through the CI/CD pipeline), you will need to have the Snowflake CLI installed and a `~/.snowflake/connections.toml` file in your local machine. For more information visit the [official documentation](https://docs.snowflake.com/en/developer-guide/snowflake-cli-v2/index#what-s-in-this-guide).

## Getting started

### Step 0: Create a project in the `streamlit-apps` subgroup using this template. 
TODO: Add more details and screenshots here.

### Step 1: Clone the repository
```bash
git clone https://gitlab.com/talkingpoints/data/streamlit-apps/${PROJECT_NAME}

cd ${PROJECT_NAME}
```
:spiral_notepad: Note: Use your project's name instead of `${PROJECT_NAME}`

### Step 2: Set up the Python Environment with `uv`

If you haven't installed `uv` run the following:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
More information about `uv` can be found in the official documentation at [docs.astral.sh/uv](https://docs.astral.sh/uv/)

Run `uv sync` to create a virtual environment in the directory and install the dependencies specified in `pyproject.toml`

```bash
uv sync
```
:spiral_notepad: Note: You can install more packages using `uv add <package name>` which is kind of running `python3 -m pip install <package name>` except it also adds it to the `pyproject.toml` file and updates the `uv.lock` file so others can reproduce your environment. However, Snowflake only allows certain packages in the Streamlit Apps they host and they use Anaconda to install them. If you need to add a third-party package you will have to create an `environment.yml` file and check the Snowflake channel to ensure it's available. We usually do not need third-party packages. Both `streamlit` and `snowflake-snowpark-python` are available by default in the Snowflake environment. They are added explicitly in our `pyproject.toml` file for local development. 

### Step 3: Local Secrets
To run the app locally, you need to store Snowflake connection details in a `.streamlit/secrets.toml` file in the root directory of the project.

You can take a look at `.streamlit/secrets-example.toml` to use it as a guide or simply update the values there and rename the file just `secrets.toml` (delete the `-example`). 

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

### Step 4: Running the App locally
You can use `uv` to run commands and automatically pick up the virtual environment by using `uv run <command>`. In this case:
```bash
uv run streamlit run app.py
```

This is the equivalent of activating the virtual environment and running `streamlit run app.py`

```bash
source .venv/bin/activate
streamlit run app.py
```

:spiral_notepad: Note: If you are using VSCode with the python extension, your IDE might automatically pick up the virtual environment and make things easier.

### Next steps
If you need to deploy directly you'll need to set up the Snowflake CLI and create the `~/.snowflake/connections.toml` file. Otherwise, you may want to add a `.gitlab-ci.yml` file to deploy this using Gitlab's CI/CD. 

A minimal example `.gitlab-ci.yml`:
```yaml
stages:
  - build
  - deploy

variables:
  PYTHON_VERSION: "3.11"
  SNOWFLAKE_ACCOUNT: $SNOWFLAKE_ACCOUNT
  SNOWFLAKE_USER: $SNOWFLAKE_USER
  SNOWFLAKE_PASSWORD: $SNOWFLAKE_PASSWORD

before_script:
  - python -m pip install --upgrade pip

build_and_deploy:
  stage: build
  image: python:${PYTHON_VERSION}
  environment:
    name: dev
  script:
    # Install Snowflake CLI
    - pip install snowflake-cli-labs

deploy:
  stage: deploy
  script:
    - snow streamlit deploy --replace --account $SNOWFLAKE_ACCOUNT --user $SNOWFLAKE_USER --password $SNOWFLAKE_PASSWORD
  only:
    - main
```

If you use this, you'll need to add `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER` and `SNOWFLAKE_PASSWORD` as environmental variables in the project's CI/CD settings. 

:warning: This CI/CD pipeline is still being developed. This is just a placeholder. :warning: