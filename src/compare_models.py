import utils
from Classifier import Classifier
from Classifier import Type

# utils.create_small_dataset()
def compare_between_models():
    tweets = utils.load_anonymized_sentiment_tweets()
    print("Tweets:", tweets[:2])
    classifier = Classifier(unigrams=True, bigrams=True, classifier_type=Type.BOW)
    act, bow_pred = classifier.classify(tweets)
    utils.accuracy(act, bow_pred)

    classifier = Classifier(unigrams=True, bigrams=True, classifier_type=Type.NB)
    act, nb_pred = classifier.classify(tweets)
    utils.accuracy(act, nb_pred)

    classifier = Classifier(unigrams=True, bigrams=True, classifier_type=Type.SVM)
    act, svm_pred = classifier.classify(tweets)
    utils.accuracy(act, svm_pred)

    print("BOW and NB")
    utils.permutation_test(act, bow_pred, nb_pred)

    print("BOW and SVM")
    utils.permutation_test(act, bow_pred, svm_pred)

    print("NB and SVM")
    utils.permutation_test(act, nb_pred, svm_pred)

def compare_nb():
    tweets = utils.load_anonymized_sentiment_tweets()
    print("svm")
    classifier = Classifier(unigrams=True, bigrams=True, classifier_type=Type.SVM)
    act, svm_pred = classifier.classify(tweets)
    utils.accuracy(act, svm_pred)

    print("unigrams")
    classifier = Classifier(unigrams=True, bigrams=False, classifier_type=Type.NB)
    act, nb_pred = classifier.classify(tweets)
    utils.accuracy(act, nb_pred)

    print("bigrams")
    classifier = Classifier(unigrams=False, bigrams=True, classifier_type=Type.NB)
    act, nb_pred = classifier.classify(tweets)
    utils.accuracy(act, nb_pred)

    print("unigrams and bigrams")
    classifier = Classifier(unigrams=True, bigrams=True, classifier_type=Type.NB)
    act, nb_pred = classifier.classify(tweets)
    utils.accuracy(act, nb_pred)

if __name__ == "__main__":
    compare_nb()