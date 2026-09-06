import requests
import sys
import os

from dotenv import load_dotenv

# Reads variables from a .env file and sets them in os.environ
load_dotenv()

GRAPH_API_VERSION = "v25.0"

FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')
FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET')
FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')

def get_long_lived_token(
        app_page_id,
        app_secret,
        access_token
    ):
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/oauth/access_token"

    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_page_id,
        "client_secret": app_secret,
        "fb_exchange_token": access_token
    }

    r = requests.get(url, params=params)

    if r.status_code != 200:
        print("Error obteniendo long-lived token:")
        print(r.text)
        sys.exit(1)

    return r.json()


def main():

    result = get_long_lived_token(
        FACEBOOK_PAGE_ID,
        FACEBOOK_APP_SECRET,
        FACEBOOK_ACCESS_TOKEN
    )

    print("\nLong-Lived Token generado:\n")
    print(result["access_token"])

    if "expires_in" in result:
        days = int(result["expires_in"]) // 86400
        print(f"\nExpira en aproximadamente {days} días")

if __name__ == "__main__":
    main()