import argparse
import os

import requests
from dotenv import load_dotenv

load_dotenv()

GRAPH_API_VERSION = "v25.0"
REQUEST_TIMEOUT_SECONDS = 30


def get_long_lived_token(app_id, app_secret, short_token):
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_token,
    }

    response = requests.get(
        url,
        params=params,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    try:
        result = response.json()
    except ValueError as error:
        raise RuntimeError(
            "Facebook returned a response that was not valid JSON."
        ) from error

    if not response.ok or "error" in result:
        error = result.get("error", {})
        message = error.get("message", response.text)
        raise RuntimeError(
            f"Facebook token exchange failed (HTTP "
            f"{response.status_code}): {message}"
        )

    if not result.get("access_token"):
        raise RuntimeError(
            "Facebook's response did not contain an access token."
        )

    return result


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Exchange a short-lived Facebook user token."
    )
    parser.add_argument(
        "--app_id",
        default=os.getenv("FACEBOOK_APP_ID"),
        help="Facebook App ID (or FACEBOOK_APP_ID).",
    )
    parser.add_argument(
        "--app_secret",
        default=os.getenv("FACEBOOK_APP_SECRET"),
        help="Facebook App Secret (or FACEBOOK_APP_SECRET).",
    )
    parser.add_argument(
        "--short_token",
        default=os.getenv("FACEBOOK_SHORT_TOKEN"),
        help="Short-lived user access token (or FACEBOOK_SHORT_TOKEN).",
    )
    args = parser.parse_args(argv)

    missing_arguments = [
        argument
        for argument, value in (
            ("--app_id", args.app_id),
            ("--app_secret", args.app_secret),
            ("--short_token", args.short_token),
        )
        if not value
    ]
    if missing_arguments:
        parser.error(
            "provide the required values: " + ", ".join(missing_arguments)
        )

    try:
        result = get_long_lived_token(
            args.app_id,
            args.app_secret,
            args.short_token,
        )
    except (requests.RequestException, RuntimeError) as error:
        print(f"Error obteniendo long-lived token: {error}")
        return 1

    print("\nLong-Lived User Token generado:\n")
    print(result["access_token"])

    if "expires_in" in result:
        days = int(result["expires_in"]) // 86400
        print(f"\nExpira en aproximadamente {days} días")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
