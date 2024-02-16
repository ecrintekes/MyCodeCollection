import nltk
import random
from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB
from nltk.classify import ClassifierI
from statistics import mode


class VoteClassifier(ClassifierI):
    def _init_(self, classifiers):
        self.classifiers = classifiers

    def classify(self, features):
        votes = []
        for currentclassifier in self.classifiers:
            vote = currentclassifier.classify(features)
            votes.append(vote)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for currentclassifier in self._classifiers:
            vote = currentclassifier.classify(features)
            votes.append(vote)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf


documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)

all_words = []
for w in movie_reviews.words():
    all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)
word_features = list(all_words.keys())[:3000]


def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features


featuresets = [(find_features(rev), category) for (rev, category) in documents]
training_set = featuresets[:1900]
testing_set = featuresets[1900:]

classifier = nltk.NaiveBayesClassifier.train(training_set)

print("Naive Bayes Doğruluk Oranı:", (nltk.classify.accuracy(classifier, testing_set)) * 100)

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MultinomialNB Doğruluk Oranı:", (nltk.classify.accuracy(MNB_classifier, testing_set)) * 100)

voted_classifier = VoteClassifier([classifier, MNB_classifier])

print("Birleşik Sınıflandırıcı Doğruluk Oranı:", (nltk.classify.accuracy(voted_classifier, testing_set)) * 100)