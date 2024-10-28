from pathlib import Path
import sys
import subprocess

Path(".streamlit/secrets-example.toml").rename(".streamlit/secrets.toml")

if "{{ cookiecutter.multi_page_app }}" == "True":
    Path("pages").mkdir()
    with open("pages/hello.py", "w") as f:
        f.write("import streamlit as st\n\n")
        f.write('st.write("Hello!")')


def is_uv_installed() -> bool:
    try:
        subprocess.run(["uv", "--version"], capture_output=True, check=True)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    if is_uv_installed():
        try:
            subprocess.run(
                ["uv", "sync"],
                check=True,
            )
            subprocess.run(
                ["git", "init"],
                check=True,
            )
            subprocess.run(
                ["uv", "run", "pre-commit", "install"],
                check=True,
            )
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
