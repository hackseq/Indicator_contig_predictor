#######################################################
#
#    Feng XU developped in Hackseq
#      @UBC, Vancouver
#      Random Forest classifier
#      Usage: python random_forest.py <input file>
#      Usage example:

from sklearn.ensemble import RandomForestClassifier
import sys

# Number of cores to use to perform parallel fitting of the forest model
n_jobs = -1  #use all the core on the machine

# Load the dataset
infile=open(sys.argv[1])
data=infile.readlines()
X = data.images.reshape((len(data.images), -1))
y = data.target

# Build a forest and compute the pixel importances
print("Fitting ExtraTreesClassifier on faces data with %d cores..." % n_jobs)
t0 = time()
forest = RandomForestClassifier(n_estimators=1000,
                              max_features=128,
                              n_jobs=n_jobs,
                              random_state=0)

forest.fit(X, y)
print("done in %0.3fs" % (time() - t0))
importances = forest.feature_importances_
importances = importances.reshape(data.images[0].shape)

print("The mean squared predict error is", mean_squared_error(y_test, est.predict(X_test)) )

#In case we have test data
#forest.score(X_test, y_test)
