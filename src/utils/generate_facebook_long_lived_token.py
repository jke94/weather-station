import requests
import argparse
import sys


GRAPH_API_VERSION = "v19.0"


def get_long_lived_token(app_id, app_secret, short_token):
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/oauth/access_token"

    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_token
    }

    r = requests.get(url, params=params)

    if r.status_code != 200:
        print("Error obteniendo long-lived token:")
        print(r.text)
        sys.exit(1)

    return r.json()


def main():
    parser = argparse.ArgumentParser(description="Generate Facebook Long-Lived User Token")

    parser.add_argument("--app_id", required=True)
    parser.add_argument("--app_secret", required=True)
    parser.add_argument("--short_token", required=True)

    args = parser.parse_args()

    result = get_long_lived_token(
        args.app_id,
        args.app_secret,
        args.short_token
    )

    print("\nLong-Lived Token generado:\n")
    print(result["access_token"])

    if "expires_in" in result:
        days = int(result["expires_in"]) // 86400
        print(f"\nExpira en aproximadamente {days} días")


if __name__ == "__main__":
    main()