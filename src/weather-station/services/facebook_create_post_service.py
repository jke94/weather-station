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

    except Exception as error:
        
        print({'error': f"Create post HTTP status code: {error}"})
        return created_post_url
