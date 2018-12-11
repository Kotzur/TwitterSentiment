import src.utils as utils
from src.Classifier import Classifier
from src.Classifier import Type

# utils.create_small_dataset()
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
