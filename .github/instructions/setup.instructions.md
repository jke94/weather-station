---
applyTo: "**/*"
---

# Setup commands

Run the commands from the repository root.

## Linux and macOS

Create and activate a Python virtual environment, then install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Windows (PowerShell)

Create and activate a Python virtual environment, then install dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r .\requirements.txt
```
