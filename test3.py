# -*- coding: utf-8 -*-
"""
Created on Sat Oct 03 00:35:50 2015

@author: vaibhav
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

from sklearn import datasets
from sklearn.cross_validation import StratifiedKFold
from sklearn.externals.six.moves import xrange
from sklearn.mixture import GMM

from sklearn.svm import LinearSVC
mod = LinearSVC(C=0.01, penalty="l1", dual=False)
X_new = mod.fit_transform(X_train, y_train)
X_new.shape
new = mod.transform(X_test)
 
from sklearn.feature_selection import VarianceThreshold
sel = VarianceThreshold(threshold=0.0001)

r = sel.fit_transform(X_train.todense())
r.shape
k = sel.transform(X_test)


def make_ellipses(gmm, ax):
    for n, color in enumerate('rgb'):
        v, w = np.linalg.eigh(gmm._get_covars()[n][:2, :2])
        u = w[0] / np.linalg.norm(w[0])
        angle = np.arctan2(u[1], u[0])
        angle = 180 * angle / np.pi  # convert to degrees
        v *= 9
        ell = mpl.patches.Ellipse(gmm.means_[n, :2], v[0], v[1],
                                  180 + angle, color=color)
        ell.set_clip_box(ax.bbox)
        ell.set_alpha(0.5)
        ax.add_artist(ell)

iris = datasets.load_iris()

# Break up the dataset into non-overlapping training (75%) and testing
# (25%) sets.
skf = StratifiedKFold(iris.target, n_folds=4)
# Only take the first fold.
train_index, test_index = next(iter(skf))


X_train = iris.data[train_index]
y_train = iris.target[train_index]
X_test = iris.data[test_index]
y_test = iris.target[test_index]

n_classes = len(np.unique(y_train))

# Try GMMs using different types of covariances.
classifiers = dict((covar_type, GMM(n_components=6,
                    covariance_type=covar_type, init_params='wc', n_iter=20))
                   for covar_type in ['spherical', 'diag', 'tied', 'full'])



np.unique(y_train)
classifier0 = GMM(n_components=3,covariance_type='full', init_params='wc', n_iter=20)
classifier0.fit(X_train[y_train==0])   
classifier1 = GMM(n_components=3,covariance_type='full', init_params='wc', n_iter=20)
classifier1.fit(X_train[y_train==1])  
classifier2 = GMM(n_components=3,covariance_type='full', init_params='wc', n_iter=20)
classifier2.fit(X_train[y_train==2])  

z0 = classifier0.predict_proba(X_test)
z1 = classifier1.predict_proba(X_test)
z2 = classifier2.predict_proba(X_test)
s0 = classifier0.score(X_test)
s1 = classifier1.score(X_test)
s2 = classifier2.score(X_test)
import pandas as pd
n = np.vstack((s0,s1,s2))
x = pd.DataFrame(n.T)
p = x.idxmax(axis = 1)
np.mean(y_test==p)
z = classifier.predict_proba(X_train)
classifier.weights_
                
y_train_pred = classifier.predict(X_train)
y_test_pred = classifier.predict(X_test)


n_classifiers = len(classifiers)

plt.figure(figsize=(3 * n_classifiers / 2, 6))
plt.subplots_adjust(bottom=.01, top=0.95, hspace=.15, wspace=.05,
                    left=.01, right=.99)


for index, (name, classifier) in enumerate(classifiers.items()):
    # Since we have class labels for the training data, we can
    # initialize the GMM parameters in a supervised manner.
    classifier.means_ = np.array([X_train[y_train == i].mean(axis=0)
                                  for i in xrange(n_classes)])

    # Train the other parameters using the EM algorithm.
    classifier.fit(X_train)

    h = plt.subplot(2, n_classifiers / 2, index + 1)
    make_ellipses(classifier, h)

    for n, color in enumerate('rgb'):
        data = iris.data[iris.target == n]
        plt.scatter(data[:, 0], data[:, 1], 0.8, color=color,
                    label=iris.target_names[n])
    # Plot the test data with crosses
    for n, color in enumerate('rgb'):
        data = X_test[y_test == n]
        plt.plot(data[:, 0], data[:, 1], 'x', color=color)

    y_train_pred = classifier.predict(X_train)
    train_accuracy = np.mean(y_train_pred.ravel() == y_train.ravel()) * 100
    plt.text(0.05, 0.9, 'Train accuracy: %.1f' % train_accuracy,
             transform=h.transAxes)

    y_test_pred = classifier.predict(X_test)
    test_accuracy = np.mean(y_test_pred.ravel() == y_test.ravel()) * 100
    plt.text(0.05, 0.8, 'Test accuracy: %.1f' % test_accuracy,
             transform=h.transAxes)

    plt.xticks(())
    plt.yticks(())
    plt.title(name)

plt.legend(loc='lower right', prop=dict(size=12))


plt.show()