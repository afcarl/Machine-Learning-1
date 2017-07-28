#!/usr/bin/python

'''

This file generates an sv model.

'''

from flask import current_app
from brain.database.dataset import Collection
from brain.cache.hset import Hset
from brain.cache.model import Model
from sklearn import svm, preprocessing
import json
from log.logger import Logger


def generate(model, kernel_type, collection, payload, list_error):
    '''

    This method generates an sv (i.e. svm, or svr) model using feature data,
    retrieved from the database. The generated model, is then stored within the
    NoSQL datastore.

    @grouped_features, a matrix of observations, where each nested vector,
        or python list, is a collection of features within the containing
        observation.
    @encoded_labels, observation labels (dependent variable labels),
        encoded into a unique integer representation.

    '''

    # local variables
    sorted_labels = False
    label_encoder = preprocessing.LabelEncoder()
    list_model_type = current_app.config.get('MODEL_TYPE')
    collection_adjusted = collection.lower().replace(' ', '_')
    cursor = Collection()

    # get datasets
    datasets = cursor.query(
        collection_adjusted,
        'aggregate',
        payload
    )

    # restructure dataset into arrays
    observation_labels = []
    grouped_features = []

    for dataset in datasets['result']:
        for observation in dataset['dataset']:
            observation_labels.append(observation['dependent-variable'])
            indep_variables = observation['independent-variables']

            for features in indep_variables:
                sorted_features = [v for k, v in sorted(features.items())]
                grouped_features.append(sorted_features)

                if not sorted_labels:
                    sorted_labels = [k for k, v in sorted(features.items())]

    # generate svm model
    if model == list_model_type[0]:
        # convert observation labels to a unique integer representation
        label_encoder = preprocessing.LabelEncoder()
        label_encoder.fit(observation_labels)
        encoded_labels = label_encoder.transform(observation_labels)

        # create model
        clf = svm.SVC(kernel=kernel_type, probability=True)

        # cache encoded labels
        Model(label_encoder).cache(model + '_labels', collection_adjusted)

        # fit model
        clf.fit(grouped_features, encoded_labels)

    # generate svr model
    elif model == list_model_type[1]:
        logger = Logger(__name__, 'error', 'error')
        logger.log('/brain/session/model.py, kernel_type: ' + repr(kernel_type))
        logger.log('/brain/session/model.py, model: ' + repr(model))
        logger.log('/brain/session/model.py, collection_adjusted: ' + repr(collection_adjusted))
        logger.log('/brain/session/model.py, list_error: ' + repr(list_error))

        # create model
        clf = svm.SVR(kernel=kernel_type)

        # fit model
        clf.fit(grouped_features, observation_labels)
        logger.log('/brain/session/model.py, clf: ' + repr(clf))

        # compute, and cache coefficient of determination
        r2 = clf.score(grouped_features, observation_labels)
        logger.log('/brain/session/model.py, r2: ' + repr(r2))
        Hset().cache(
            model + '_r2',
            collection_adjusted,
            r2
        )

    # cache model
    Model(clf).cache(model + '_model', collection_adjusted)

    # cache feature labels, with respect to given collection
    Hset().cache(
        model + '_feature_labels',
        collection,
        json.dumps(sorted_labels)
    )

    # return error(s) if exists
    return {'error': list_error}
