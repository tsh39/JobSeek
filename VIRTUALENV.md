Virtual environment

We recommend using a project-local virtual environment to keep dependencies isolated.

Create and activate a venv (macOS, bash):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

To deactivate:

```bash
deactivate
```

Optional: direnv integration

If you use direnv you can auto-activate the virtualenv by allowing the provided `.envrc` in the project root. To enable direnv, install it and then run `direnv allow` once.
