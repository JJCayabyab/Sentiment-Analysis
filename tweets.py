import tweepy
import csv

# Replace these values with your own Twitter API credentials
consumer_key = "vwsbNQcSdCnvta627Z7J1mSSW"
consumer_secret = "sGmYuvNsM4OggIX2WqdsVteCZwwiWqIoImdCcMbQCxpSzsDNMW"
access_token = "1430430506865233924-3uasd0wFLv2rzzhhwW4UxaWDN6ACMe"
access_token_secret = "HEa2gPGSlSKq6RiAQEacEVvUqZMEa6M7aIwF9SG2dTZy1"

# Set up authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

def scrape_tweets(query, count=100, filename='tweets.csv'):
    # Open a CSV file for writing
    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Write header row to CSV file
        csv_writer.writerow(['Tweet ID', 'Text', 'Username', 'Created At'])

        try:
            # Use the Cursor for searching tweets
            for tweet in tweepy.Cursor(api.search_tweets, q=query, count=count, lang='en').items(count):
                # Write tweet data to CSV file
                csv_writer.writerow([tweet.id_str, tweet.text, tweet.user.screen_name, tweet.created_at])

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    # Replace 'YOUR_SEARCH_QUERY' with the desired search query
    search_query = 'YOUR_SEARCH_QUERY'

    # Specify the number of tweets to retrieve
    tweet_count = 100

    # Specify the output CSV file name
    output_filename = 'tweets.csv'

    # Call the function to scrape tweets
    scrape_tweets(search_query, tweet_count, output_filename)

    print(f'Tweets scraped successfully and saved to {output_filename}.')
