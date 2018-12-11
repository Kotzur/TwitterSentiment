import csv
import math
import os
import random
import re

from scipy.stats import binom
import numpy as np


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "..", "data")
SENTIMENT_TWEETS_PATH = os.path.join(DATA_DIR, "sentiment_tweets.csv")
ANONYMOUS_SENTIMENT_TWEETS_PATH = os.path.join(DATA_DIR, "anonymous_sentiment_tweets.csv")
SMALL_DATASET_PATH = os.path.join(DATA_DIR, "small_dataset.csv")
MODEL_PATH = os.path.join(DATA_DIR, "nb_model")
AIRLINE_TWEETS_PATH = os.path.join(DATA_DIR, "airline_tweets.csv")


def accuracy(actual, predictions):
    true_positive_negative = sum(1 if a == b else 0 for a, b in zip(actual, predictions))
    print(f"correct guesses: {true_positive_negative}")
    print(f"total guesses: {len(predictions)}")
    print("Accuracy:", true_positive_negative / len(predictions))


def permutation_test(actual_classes, a_predictions, b_predictions):
    a_correct = []
    b_correct = []
    for i, actual in enumerate(actual_classes):
        if actual == a_predictions[i]:
            a_correct.append(1)
        else:
            a_correct.append(0)
        if actual == b_predictions[i]:
            b_correct.append(1)
        else:
            b_correct.append(0)

    R = 5000    # Monte Carlo sampling constant
    s = 0       # Number of mean differences >= unpermuted mean difference
    D_0 = abs(np.mean(a_correct) - np.mean(b_correct))
    indecies = [i for i in range(0, len(a_correct))]
    for i in range(0, R):
        ind_perm = indecies
        a_perm = a_correct
        b_perm = b_correct
        # choose to permute between none and all elements
        number_of_pairs_permuted = np.random.randint(0, len(a_perm) + 1)
        ind_perm = np.random.choice(ind_perm, number_of_pairs_permuted)
        for index in ind_perm:
            temp = a_perm[index]
            a_perm[index] = b_perm[index]
            b_perm[index] = temp
        D_i = abs(np.mean(a_perm) - np.mean(b_perm))
        s += 1 if D_i >= D_0 else 0
    p = (s+1) / (R + 1)
    print(f"Prob that Null Hypothesis is true for the two models: {p}\n")


def sign_test(actual_classes, a_predictions, b_predictions, features):
    average_sum_p = 0
    for fold in range(0, len(actual_classes)):
        actual = actual_classes[fold]
        a_pred = a_predictions[fold]
        b_pred = b_predictions[fold]

        a_better = sum(1 for i, a in enumerate(actual) if
                       (a == a_pred[i]) and (not a == b_pred[i]))
        b_better = sum(1 for i, a in enumerate(actual) if
                       (a == b_pred[i]) and (not a == a_pred[i]))
        both_same = sum(1 for i, a in enumerate(actual) if (a_pred[i] == b_pred[i]))

        print("NB better: %d" % a_better)
        print("SVM better: %d" % b_better)
        print("Both same: %d" % both_same)

        big_n = 2 * math.ceil(both_same / 2) + a_better + b_better
        k = math.ceil(both_same / 2) + min(a_better, b_better)
        p = 2 * sum(binom(big_n, i) * math.pow(0.5, i) * math.pow(0.5, big_n - i) for i in range(0, k))
        print("The probability for fold %d that the models are the same is %f" % (fold, p*100))
        average_sum_p += p

    average_p = average_sum_p / len(actual_classes)
    print("***")
    print("Average probability across folds that the models with %s are the same is %f" % (features, average_p*100))
    print("***")

    return average_p


def anonymize_sentiment_tweets():
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
                tweet = clean_data(anonymize(tweet))
                writer.writerow({'sentiment': sent, 'tweet': str(tweet)})


def load_anonymized_sentiment_tweets(small=True):
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
        clean_reviews.append([clean_data(anonymize(review)), num_sent])
    return clean_reviews


def round_robin_split(reviews):
    ten_splits = []
    for i in range(10):
        ten_splits.append([reviews[r] for r in range(len(reviews)) if r % 10 == i])
    return ten_splits


def clean_data(text):
    norm_text = text.lower()
    # Replace breaks with spaces
    norm_text = norm_text.replace('<br />', ' ')
    # Pad punctuation with spaces on both sides
    norm_text = re.sub(r"([\.\",\(\)!\?;:])", " \\1 ", norm_text)
    return norm_text


def anonymize(text):
    text = re.sub("(http:[^\s\n\r]+)", "HTTP", text)
    return re.sub("@\w+", "@USERNAME", text)


def tokenize(text):
    return [word for word in text.split()]
