import numpy as np
from math import log as ln


class NaiveBayesClassifier:

    def __init__(self, alpha=1.00):
        self.smoothing = alpha

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        self.unique_classes = np.unique(y)
        self.prior_probs = {}
        self.conditional_probs = {}

        all_words = []
        for doc in X:
            words = doc.split()
            all_words.extend(words)

        vocab, word_counts = np.unique(all_words, return_counts=True)
        vocab_size = len(vocab)

        for cls in self.unique_classes:
            class_docs = [X[i] for i in range(len(y)) if y[i] == cls]
            self.prior_probs[cls] = len(class_docs) / len(X)

            self.conditional_probs[cls] = []

            class_words = []
            for doc in class_docs:
                words = doc.split()
                class_words.extend(words)

            class_vocab, class_word_counts = np.unique(class_words, return_counts=True)
            word_freq = np.zeros_like(vocab, dtype=float)
            class_word_count_dict = dict(zip(class_vocab, class_word_counts))

            for i, word in enumerate(vocab):
                word_freq[i] = class_word_count_dict.get(word, 0)

            self.conditional_probs[cls].append(
                dict(zip(vocab, (word_freq + self.smoothing) / (len(class_words) + self.smoothing * vocab_size)))
            )

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        predictions = []
        for doc in X:
            doc_words = doc.split()

            class_scores = []
            for cls in self.unique_classes:
                log_prob = ln(self.prior_probs[cls])
                for word in doc_words:
                    if word in self.conditional_probs[cls][0]:
                        log_prob += ln(self.conditional_probs[cls][0][word])
                class_scores.append(log_prob)

            best_class = self.unique_classes[np.argmax(class_scores)]
            predictions.append(best_class)

        return predictions

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        predicted_labels = self.predict(X_test)
        correct_predictions = sum(1 for i in range(len(y_test)) if predicted_labels[i] == y_test[i])
        accuracy = correct_predictions / len(y_test)
        return accuracy
