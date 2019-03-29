from sentiment_spectrum import SentimentSpectrum
from utils.handle_datasets import load_anonymized_sentiment_tweets
from utils import metrics
from classifier import Classifier, Type


# create_small_dataset()
def compare_between_models():
    tweets = load_anonymized_sentiment_tweets()
    print("Tweets:", tweets[:2])
    classifier = Classifier(unigrams=True, bigrams=True, classifier_type=Type.BOW, tfidf=False)
    act, bow_pred = classifier.ten_fold_cross_validation(tweets)
    print("BOW")
    metrics.accuracy(act, bow_pred)

    classifier = Classifier(unigrams=True, bigrams=True, classifier_type=Type.NB, tfidf=False)
    act, nb_pred = classifier.ten_fold_cross_validation(tweets)
    print("NB")
    metrics.accuracy(act, nb_pred)

    classifier = Classifier(unigrams=True, bigrams=True, classifier_type=Type.SVM, tfidf=False)
    act, svm_pred = classifier.ten_fold_cross_validation(tweets)
    print("SVM")
    metrics.accuracy(act, svm_pred)

    print("BOW and NB")
    metrics.permutation_test(act, bow_pred, nb_pred)

    print("BOW and SVM")
    metrics.permutation_test(act, bow_pred, svm_pred)

    print("NB and SVM")
    metrics.permutation_test(act, nb_pred, svm_pred)


def compare_nb():
    tweets = load_anonymized_sentiment_tweets()
    print("Tfidf")
    print("unigrams")
    Classifier(unigrams=True, bigrams=False, classifier_type=Type.NB).evaulate(tweets)

    print("bigrams")
    Classifier(unigrams=False, bigrams=True, classifier_type=Type.NB).evaulate(tweets)

    print("unigrams and bigrams")
    Classifier(unigrams=True, bigrams=True, classifier_type=Type.NB).evaulate(tweets)


def compare_svm():
    tweets = load_anonymized_sentiment_tweets()
    print("tfidf")
    print("unigram")
    Classifier(unigrams=True, bigrams=False, classifier_type=Type.SVM).evaulate(tweets)

    print("bigrams")
    Classifier(unigrams=False, bigrams=True, classifier_type=Type.SVM).evaulate(tweets)

    print("unigrams and bigrams")
    Classifier(unigrams=True, bigrams=True, classifier_type=Type.SVM).evaulate(tweets)


def perform_card_sort():
    tweets = ["Also today my son needed surgery on his foot. He s insured, but thanks to Obamacare his deductible is $6,000. Before the hospital would begin they asked for all $6,000. They settled for $2,000 cash and a promissory note for the balance.",
              "Major victory: Texas wins Obamacare tax lawsuit and recoups $839 million! Obamacare is unconstituitional, plain and simple. We all know that the feds cannot tax the states, and we're proud to return this illegally collected money to the people of texas.",
              "No doubt Obamacare is better than what existed before. But it leaves intact the profit motive in american health care. So any regulation & prohibitions of abuses are likely to amount to tying down a reavenous beast with bungee cords.",
              "Just stop calling it Obamacare & use the correct name - affordable care act (aka ACA)",
              "Obamacare saves millions of lives! Open your eyes people!",
              "Obama and Obamacare sucks.",
              "The majority of the country doesn't want Medicare for all. We need to improve Obamacare to cover more people.",
              "Maybe if my doctor wasn't forced to use EMR I would be less worried. Obamacare still makes physicians' costs higher.",
              "Republicans want to return America to a simpler time. A time when the poor were found dead in gutters. And the cause of death was a mild infection which could have been easily treated with antibiotics. I don't know what I would do without Obamacare.",
              "Don't forget that you can keep your doctor. Obama was the lyingist president ever. How much are people paying for medical insurance these days, due to Obama the moron. How much was wasted setting up Obamacare? How long did the website not work? etc"]

    spectrum = SentimentSpectrum(build_new=True, svm=True)
    spectrum.create_spectrum(tweets)
    for s in spectrum.spectrum:
        print(s.tweet)
        words = s.word_probs
        sorted_words = [(w, words[w]) for w in sorted(words, key=lambda word: words[word], reverse=True)]
        print("Words: ", sorted_words)
        print("")

if __name__ == "__main__":
    perform_card_sort()
