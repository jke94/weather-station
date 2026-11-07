import requests

def create_post(
        page_id,
        access_token,
        post_content
) -> str:
    
    created_post_url = "NONE"

    try:
        
        # Facebook Graph API endpoint
        url = f"https://graph.facebook.com/v25.0/{page_id}/feed"
        
        # Headers para indicar que enviamos JSON
        headers = {
            "Content-Type": "application/json"
        }
        
        # Parámetros del post
        data = {
            "message": post_content,
            "access_token": access_token
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        post_id = response.json().get("id")
        if post_id:
            created_post_url = f"https://www.facebook.com/{post_id}"

        return created_post_url

    except requests.exceptions.HTTPError as error:
        error_response = error.response
        if error_response is None:
            print({'error': f"Facebook Graph API request failed: {error}"})
        else:
            try:
                error_details = error_response.json()
            except ValueError:
                error_details = error_response.text

            print({
                'error': (
                    'Facebook Graph API returned HTTP '
                    f'{error_response.status_code}'
                ),
                'details': error_details
            })

        return created_post_url

    except requests.exceptions.RequestException as error:
        print({'error': f"Facebook Graph API request failed: {error}"})
        return created_post_url
