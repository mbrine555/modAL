"""
Uncertainty measures for the active learning models.
"""

import numpy as np
from scipy.stats import entropy


def classifier_uncertainty(classifier, samples, **predict_proba_kwargs):
    """
    Classification uncertainty of the classifier for the provided samples

    Parameters
    ----------
    classifier: sklearn classifier object, for instance sklearn.ensemble.RandomForestClassifier
        The classifier for which the uncertainty is to be measured

    samples: numpy.ndarray of shape (n_samples, n_features)
        The samples for which the uncertainty of classification is to be measured

    **predict_proba_kwargs: keyword arguments
        Keyword arguments to be passed for the predict_proba method of the classifier

    Returns
    -------
    uncertainty: numpy.ndarray of shape (n_samples, 1)
        Classifier uncertainty, which is 1 - P(prediction is correct)

    """
    # calculate uncertainty for each point provided
    classwise_uncertainty = classifier.predict_proba(samples, **predict_proba_kwargs)

    # for each point, select the maximum uncertainty
    uncertainty = 1 - np.max(classwise_uncertainty, axis=1)
    return uncertainty


def classifier_margin(classifier, samples, **predict_proba_kwargs):
    """
    Classification margin uncertainty of the classifier for the provided samples
    This uncertainty measure takes the first and second most likely predictions
    and takes the difference of their probabilities, which is the margin

    Parameters
    ----------
    classifier: sklearn classifier object, for instance sklearn.ensemble.RandomForestClassifier
        The classifier for which the uncertainty is to be measured

    samples: numpy.ndarray of shape (n_samples, n_features)
        The samples for which the uncertainty of classification is to be measured

    **predict_proba_kwargs: keyword arguments
        Keyword arguments to be passed for the predict_proba method of the classifier

    Returns
    -------
    margin: numpy.ndarray of shape (n_samples, 1)
        Margin uncertainty, which is the difference of the probabilities of first
        and second most likely predictions

    """
    classwise_uncertainty = classifier.predict_proba(samples, **predict_proba_kwargs)

    if classwise_uncertainty.shape[1] == 1:
        return np.zeros(shape=(classwise_uncertainty.shape[0],))

    part = np.partition(-classwise_uncertainty, 1, axis=1)
    margin = -part[:, 0] + part[:, 1]

    return margin


def classifier_entropy(classifier, samples, **predict_proba_kwargs):
    """
    Entropy of predictions of the for the provided samples

    Parameters
    ----------
    classifier: sklearn classifier object, for instance sklearn.ensemble.RandomForestClassifier
        The classifier for which the prediction entropy is to be measured

    samples: numpy.ndarray of shape (n_samples, n_features)
        The samples for which the prediction entropy is to be measured

    **predict_proba_kwargs: keyword arguments
        Keyword arguments to be passed for the predict_proba method of the classifier

    Returns
    -------
    entr: numpy.ndarray of shape (n_samples, 1)
        Entropy of the class probabilities

    """
    classwise_uncertainty = classifier.predict_proba(samples, **predict_proba_kwargs)

    entr = np.zeros(shape=(samples.shape[0],))

    for unc_idx, unc in enumerate(classwise_uncertainty):
        entr[unc_idx] = entropy(unc)

    return entr
