import argparse
import io
import json
import os
from pathlib import Path
from urllib.parse import quote
import zipfile

import requests


def _github_api_get(url: str, token: str) -> requests.Response:
    response = requests.get(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response


def restore_latest_state(
    platform: str,
    state_path: Path,
    token: str,
    repository: str,
    workflow_ref: str,
    branch: str,
    current_run_id: str,
    api_url: str,
) -> None:
    workflow_path = workflow_ref.split("@", maxsplit=1)[0].split(
        "/.github/workflows/", maxsplit=1
    )
    if len(workflow_path) != 2:
        raise ValueError("GITHUB_WORKFLOW_REF does not identify a workflow file.")

    workflow_file = workflow_path[1]
    workflow_runs_url = (
        f"{api_url}/repos/{repository}/actions/workflows/"
        f"{workflow_file}/runs?status=completed&per_page=100"
        f"&branch={quote(branch, safe='')}"
    )
    workflow_runs = _github_api_get(workflow_runs_url, token).json()
    artifact_name = f"weather-station-state-{platform}"
    selected_artifact = None

    runs = sorted(
        workflow_runs["workflow_runs"],
        key=lambda run: run["created_at"],
        reverse=True,
    )
    for run in runs:
        if str(run["id"]) == current_run_id:
            continue

        artifacts_url = (
            f"{api_url}/repos/{repository}/actions/runs/"
            f"{run['id']}/artifacts?per_page=100"
        )
        artifacts = _github_api_get(artifacts_url, token).json()["artifacts"]
        selected_artifact = next(
            (
                artifact for artifact in artifacts
                if artifact["name"] == artifact_name
                and not artifact["expired"]
            ),
            None,
        )
        if selected_artifact is not None:
            break

    if selected_artifact is None:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text("{}\n", encoding="utf-8")
        return

    archive = _github_api_get(
        selected_artifact["archive_download_url"], token
    ).content
    with zipfile.ZipFile(io.BytesIO(archive)) as archive_file:
        state_data = json.loads(archive_file.read("publishing-state.json"))
    if not isinstance(state_data, dict):
        raise ValueError("Restored publication state must be a JSON object.")
    for record in state_data.values():
        if (
            not isinstance(record, dict)
            or record.get("status") not in {"publishing", "published"}
            or (
                record["status"] == "published"
                and not isinstance(record.get("url"), str)
            )
        ):
            raise ValueError("Restored publication state contains an invalid entry.")

    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(state_data, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Restore the latest publication state artifact."
    )
    parser.add_argument("--platform", choices=("facebook", "x"), required=True)
    parser.add_argument(
        "--state-path",
        default=".weather_station/publishing-state.json",
    )
    args = parser.parse_args()

    required_environment = (
        "GITHUB_TOKEN",
        "GITHUB_REPOSITORY",
        "GITHUB_WORKFLOW_REF",
        "GITHUB_REF_NAME",
        "GITHUB_RUN_ID",
    )
    missing = [name for name in required_environment if not os.getenv(name)]
    if missing:
        raise RuntimeError(
            "Missing required GitHub Actions environment variables: "
            + ", ".join(missing)
        )

    restore_latest_state(
        platform=args.platform,
        state_path=Path(args.state_path),
        token=os.environ["GITHUB_TOKEN"],
        repository=os.environ["GITHUB_REPOSITORY"],
        workflow_ref=os.environ["GITHUB_WORKFLOW_REF"],
        branch=os.environ["GITHUB_REF_NAME"],
        current_run_id=os.environ["GITHUB_RUN_ID"],
        api_url=os.getenv("GITHUB_API_URL", "https://api.github.com"),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
