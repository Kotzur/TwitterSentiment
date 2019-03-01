import csv
import json
import os
import re
import sys

import tweepy


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "..", "data")
SENTIMENT_TWEETS_PATH = os.path.join(DATA_DIR, "sentiment_tweets.csv")
ANONYMOUS_SENTIMENT_TWEETS_PATH = os.path.join(DATA_DIR, "anonymous_sentiment_tweets.csv")
SMALL_DATASET_PATH = os.path.join(DATA_DIR, "small_dataset.csv")
MODEL_PATH = os.path.join(DATA_DIR, "nb_model")
AIRLINE_TWEETS_PATH = os.path.join(DATA_DIR, "airline_tweets.csv")
JSON_PATH = os.path.join(DATA_DIR, "spectrum.json")
TWITTER_ACCESS_PATH = os.path.join(DATA_DIR, "twitter_access")

study_number = -1


def anonymize_sentiment_tweets():
    """Read the original Stanford sentiment corpus file, anonymize it and write the simplified results to a new file."""
    fieldnames = ['sentiment', 'tweet']
    with open(SENTIMENT_TWEETS_PATH, encoding="utf-8", errors="ignore") as original_file:
        with open(ANONYMOUS_SENTIMENT_TWEETS_PATH, "w") as anonymized_file:
            original_reader = csv.DictReader(original_file)
            writer = csv.DictWriter(anonymized_file, fieldnames=fieldnames)
            writer.writeheader()
            for i, line in enumerate(original_reader):
                raw_sent = line['polarity']
                # Don't consider neutral tweets.
                if raw_sent == "0":
                    sent = 0
                elif raw_sent == "4":
                    sent = 1
                else:
                    continue

                tweet = line["text"]
                tweet = clean_data(tweet)
                writer.writerow({'sentiment': sent, 'tweet': str(tweet)})


def round_robin_split(reviews):
    """Split the dataset inot 10 even folds with the round robin schema.
    :param reviews dataset to split.
    :return list of 10 collections of tweets.
    """
    ten_splits = []
    for i in range(10):
        ten_splits.append([reviews[r] for r in range(len(reviews)) if r % 10 == i])
    return ten_splits


def clean_data(text):
    """Reformat data for processing.
    Substitute all linebreaks with a whitespace. Surround all punctuation with a whitespace to also treat them as
    tokens. Anonymize the data.
    :param text line of text to be cleaned.
    :return text ready for processing.
    """
    norm_text = text.lower()
    # Replace breaks with spaces
    norm_text = norm_text.replace('<br />', ' ')
    norm_text = re.sub("(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?", "link", norm_text)
    norm_text = re.sub("&amp;", "&", norm_text)
    # Pad punctuation with spaces on both sides
    norm_text = re.sub(r"([\.\",\(\)!\?;:(...)])", " \\1 ", norm_text)
    norm_text = re.sub(r"@\w+", "@username", norm_text)
    norm_text = re.sub(r"(@username)((\s)*@username)+", "@username", norm_text)
    return norm_text


def tokenize(text):
    """Tokenize a text.
    :param text tweet to tokenize
    :return list of words in text
    """
    return [word for word in text.split()]


def load_anonymized_sentiment_tweets(small=True):
    """Load the anonymized file with Stanford data.
    :param small boolean whether to load the big or small dataset version.
    :return collection of tuples (tweet, sentiment 0 or 1)
    """
    tweets = []
    sentiments = []
    if small:
        filename = SMALL_DATASET_PATH
    else:
        filename = ANONYMOUS_SENTIMENT_TWEETS_PATH

    with open(filename) as file:
        tweet_reader = csv.DictReader(file)
        for row in tweet_reader:
            sentiments.append(int(row['sentiment']))
            tweets.append(row['tweet'])

    dataset = [[t, s] for t, s in zip(tweets, sentiments)]
    # random.shuffle(dataset)
    return dataset


# The whole dataset is too big for me to run. Create a file of first 5000 pos and 5000 neg tweets.
def create_small_dataset():
    """Create the file with only 1000 tweets from the Stanford sentiment corpus."""
    full_dataset = load_anonymized_sentiment_tweets(small=False)
    negative_tweets = [item for item in full_dataset if item[1] == 0][:5000]
    positive_tweets = [item for item in full_dataset if item[1] == 1][:5000]

    with open(SMALL_DATASET_PATH, "w") as file:
        fieldnames = ["sentiment", "tweet"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for neg in negative_tweets:
            writer.writerow({"sentiment": neg[1], "tweet": neg[0]})
        for pos in positive_tweets:
            writer.writerow({"sentiment": pos[1], "tweet": pos[0]})


def load_airline_tweets():
    """Load a sentiment dataset of tweets about US airlines."""
    reviews = []
    sentiments = []
    with open(AIRLINE_TWEETS_PATH) as file:
        tweet_reader = csv.DictReader(file)
        for row in tweet_reader:
            sentiments.append(row['airline_sentiment'])
            reviews.append(row['text'])
    clean_reviews = []
    for review, sentiment in zip(reviews, sentiments):
        if sentiment == "negative":
            num_sent = 0
        elif sentiment == "positive":
            num_sent = 1
        elif sentiment == "neutral":
            continue
        else:
            "Invalid sentiment type."
            sys.exit(-1)
        clean_reviews.append([clean_data(review), num_sent])
    return clean_reviews


def get_dataset(topic):
    """Load from Tweeter a set of tweets on a specific topic.
    Use the topic to query as a hashtag and fetch as many as possible tweets through the Twitter API. Prepare them for
    processing.
    :param topic query used to search twitter.
    :return dataset on the topic ready for processing.
    """
    print(topic)
    topic = topic.lower()
    topic = topic.replace(" ", "_")
    print(topic)
    topic_path = os.path.join(DATA_DIR, "topics", topic)
    if os.path.isfile(topic_path):
        print(f"Reading local file from: {topic_path}")
        with open(topic_path, "r") as file:
            tweets = json.load(file)
        print(f"length of this loaded list: {len(tweets)}")
        return tweets
    else:
        return request_tweets_from_twitter(topic)


def request_tweets_from_twitter(topic, request_number=100):
    # Authenticate as an app not a user to increase the rate limit.
    api_key, api_secret, _, _ = get_twitter_keys()
    auth = tweepy.AppAuthHandler(api_key, api_secret)

    # Tweepy holds on until the end of the window if it gets rate limit messages back.
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    if not api:
        print("Can't Authenticate")
        sys.exit(-1)

    since_id = None
    max_id = -1
    tweet_count = 0
    dataset = set([])

    print(f"Downloading max {request_number} tweets")

    while tweet_count < request_number:
        try:
            new_tweets = call_twitter_search(api, topic, 100, since_id, max_id)
            if not new_tweets:
                print("No more tweets found.")
                break
            add_new_tweets_to_dataset(new_tweets, dataset)
            tweet_count += len(new_tweets)
            print(f"Downloaded {tweet_count} tweets")
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("Error from Twitter API: " + str(e))
            break
    return dataset


def call_twitter_search(api, search_query, tweets_per_page, since_id, max_id):
    if max_id <= 0:
        if not since_id:
            new_tweets = api.search(q=search_query,
                                    lang='en',
                                    count=tweets_per_page,
                                    tweet_mode="extended")
        else:
            new_tweets = api.search(q=search_query,
                                    lang='en',
                                    count=tweets_per_page,
                                    tweet_mode="extended",
                                    since_id=since_id)
    else:
        if not since_id:
            new_tweets = api.search(q=search_query,
                                    lang='en',
                                    count=tweets_per_page,
                                    tweet_mode="extended",
                                    max_id=str(max_id - 1))
        else:
            new_tweets = api.search(q=search_query,
                                    lang='en',
                                    count=tweets_per_page,
                                    tweet_mode="extended",
                                    max_id=str(max_id - 1),
                                    since_id=since_id)
    return new_tweets


def add_new_tweets_to_dataset(tweets, dataset):
    for tweet in tweets:
        if "retweeted_status" in tweet._json:
            clean = clean_data(tweet._json['retweeted_status']['full_text'])
        else:
            clean = clean_data(tweet._json['full_text'])
        if clean.startswith("rt"):
            clean = clean[3:]
        if clean not in dataset:
            dataset.add(clean)


def get_twitter_keys():
    keys = []
    if os.path.isfile(TWITTER_ACCESS_PATH):
        with open(TWITTER_ACCESS_PATH, "r") as file:
            keys = file.readlines()
            keys = [k.replace("\n", "") for k in keys]
    else:
        keys.append(input("Enter customer key"))
        keys.append(input("Enter customer secret"))
        keys.append(input("Enter access token"))
        keys.append(input("Enter access token secret"))
    return keys


def save_dataset(topic):
    tweets = request_tweets_from_twitter(topic, request_number=500)
    filename = os.path.join(DATA_DIR, "topics", topic.replace(" ", "_"))
    with open(filename, "w+") as file:
        json.dump(list(tweets), file)


def save_results(results, filename):
    directory = os.path.join(DATA_DIR, "results", f"study_{study_number}")
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(os.path.join(directory, filename), "w+") as file:
        json.dump(results, file)
