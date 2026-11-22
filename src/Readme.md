# weather-station

The `weather_station` package is implemented under `src/weather_station/`;
repository tests are in `test/`. From the repository root, activate `.venv`
and set `PYTHONPATH` before running a package CLI with
`python -m weather_station.<module>`.

### Linux and macOS

```bash
source .venv/bin/activate
export PYTHONPATH=src
python -m weather_station.<module>
```

### Windows (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "src"
python -m weather_station.<module>
```