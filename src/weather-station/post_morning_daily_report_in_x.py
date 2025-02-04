import tweepy

# Create Tweet

# The app and the corresponding credentials must have the Write permission

# Check the App permissions section of the Settings tab of your app, under the
# Twitter Developer Portal Projects & Apps page at
# 

# Make sure to reauthorize your app / regenerate your access token and secret 
# after setting the Write permission

def main():

    # TODO: Sustitute by envrionment variables or arguments

    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""

    client = tweepy.Client(
        consumer_key=consumer_key, 
        consumer_secret=consumer_secret,
        access_token=access_token, 
        access_token_secret=access_token_secret
    )

    response = client.create_tweet(
        text="This is a test post."
    )

    print(f"https://twitter.com/user/status/{response.data['id']}")

    response.close()

if __name__ == "__main__":
    main()