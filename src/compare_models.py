from handle_datasets import load_anonymized_sentiment_tweets
import metrics
from classifier import Classifier, Type


# create_small_dataset()
def compare_between_models():
    tweets = load_anonymized_sentiment_tweets()
    print("Tweets:", tweets[:2])
    classifier = Classifier(unigrams=True, bigrams=True, classifier_type=Type.BOW).evaulate(tweets)
    act, bow_pred = classifier.ten_fold_cross_validation(tweets)
    print("BOW")
    metrics.accuracy(act, bow_pred)

    classifier = Classifier(unigrams=True, bigrams=True, classifier_type=Type.NB).evaulate(tweets)
    act, nb_pred = classifier.ten_fold_cross_validation(tweets)
    print("NB")
    metrics.accuracy(act, nb_pred)

    classifier = Classifier(unigrams=True, bigrams=True, classifier_type=Type.SVM).evaulate(tweets)
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
    print("unigrams")
    Classifier(unigrams=True, bigrams=False, classifier_type=Type.NB).evaulate(tweets)

    print("bigrams")
    Classifier(unigrams=False, bigrams=True, classifier_type=Type.NB).evaulate(tweets)

    print("unigrams and bigrams")
    Classifier(unigrams=True, bigrams=True, classifier_type=Type.NB).evaulate(tweets)

def compare_svm():
    tweets = load_anonymized_sentiment_tweets()
    print("unigram")
    Classifier(unigrams=True, bigrams=False, classifier_type=Type.SVM).evaulate(tweets)

    print("bigrams")
    Classifier(unigrams=False, bigrams=True, classifier_type=Type.SVM).evaulate(tweets)

    print("unigrams and bigrams")
    Classifier(unigrams=True, bigrams=True, classifier_type=Type.SVM).evaulate(tweets)

if __name__ == "__main__":
    compare_svm()
