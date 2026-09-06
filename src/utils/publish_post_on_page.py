import requests
import os
from dotenv import load_dotenv

# Reads variables from a .env file and sets them in os.environ
load_dotenv()

def create_post(
        page_id,
        access_token,
        post_content
) -> str:
    
    created_post_url = "NONE"

    # Facebook Graph API endpoint
    url = f"https://graph.facebook.com/v25.0/{page_id}/feed"

    # Headers for the request
    headers = {
        "Content-Type": "application/json"
    }
    
    # Parameters for the post
    data = {
        "message": post_content,
        "access_token": access_token
    }

    try:

        response = requests.post(url, headers=headers, json=data)

        response.raise_for_status()

        post_id = response.json().get("id")

        if post_id:
            created_post_url = f"https://www.facebook.com/{post_id}"

        return created_post_url

    except Exception as error:
        
        print({'error': f"Create post HTTP status code: {error}"})
        return created_post_url

def main():

    # Message to post on the Facebook page
    message = "Test post from Python script."

    FACEBOOK_LONG_LIVED_ACCESS_TOKEN = os.getenv('FACEBOOK_LONG_LIVED_ACCESS_TOKEN')
    FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')

    if not FACEBOOK_LONG_LIVED_ACCESS_TOKEN or not FACEBOOK_PAGE_ID:
        print("Error: Missing FACEBOOK_LONG_LIVED_ACCESS_TOKEN or FACEBOOK_PAGE_ID in environment variables.")
        return

    result = create_post(
        FACEBOOK_PAGE_ID,
        FACEBOOK_LONG_LIVED_ACCESS_TOKEN,
        message
    )

    print(f"\nCreated post:\n{result}")

if __name__ == "__main__":
    main()