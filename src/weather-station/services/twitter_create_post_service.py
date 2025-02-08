import tweepy

def create_tweet(
        api_key, 
        api_secret,
        access_token,
        access_secret, 
        tweet_content
) -> str:
    
    created_tweet_url = "NONE"

    try:
        
        # Create X (Twitter) client.
        client = tweepy.Client(
            consumer_key=api_key, 
            consumer_secret=api_secret,
            access_token=access_token, 
            access_token_secret=access_secret
        )

        response = client.create_tweet(
            text=tweet_content
        )

        created_tweet_url = f"https://twitter.com/user/status/{response.data['id']}"

        return created_tweet_url

    except Exception as error:
        
        print({'error': f"Create tweet HTTP status code: {error}"})
        return created_tweet_url    