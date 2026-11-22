from urllib.parse import quote, quote_plus

import requests
import tweepy


def create_tweet(
    api_key: str,
    api_secret: str,
    access_token: str,
    access_secret: str,
    tweet_content: str,
) -> str:
    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret,
        )
        response = client.create_tweet(text=tweet_content)
        return f"https://twitter.com/user/status/{response.data['id']}"
    except (
        tweepy.TweepyException,
        requests.exceptions.RequestException,
        KeyError,
    ) as error:
        error_message = str(error)
        for credential in (
            api_key,
            api_secret,
            access_token,
            access_secret,
        ):
            if credential:
                for secret in {
                    credential,
                    quote(credential, safe=""),
                    quote_plus(credential),
                }:
                    error_message = error_message.replace(
                        secret, "[REDACTED]"
                    )
        print({"error": f"Create tweet failed: {error_message}"})
        return "NONE"
