#######################################################
#
#    Feng XU developped in Hackseq
#      @UBC, Vancouver
#      Random Forest classifier
#      Usage: python random_forest.py <input file> <fai file> <meta_label file>
#      Usage example:python random_forest_final.py bam_folder infant_gut_microbiome_PacBio.fasta.fai infant_metadata.txt

from sklearn.ensemble import RandomForestClassifier
import sys
import os
ob_li=os.listdir(sys.argv[1])

# Number of cores to use to perform parallel fitting of the forest model
n_jobs = -1  #use all the core on the machine

# Load the dataset
infile2=open(sys.argv[2])
two=infile2.readlines()
X=[]   #features
y=[]   #targets
infile3=open(sys.argv[3])
three=infile3.readlines()
label={}
for line3 in three:
    lin3=line3.split("\t")
    label[lin3[4]]=lin3[11]

for obj in ob_li:
    infile1=open("./bam_folder/"+obj)
    srr_id=obj.split(".")
    y.append(srr_id[0])
    l_r_d={}
    for line2 in two:
        lin2=line2.split("\t")
        l_r_d[lin2[0]]=0

    one=infile1.readlines()
    for line1 in one:
        lin1=line1.split()
        if lin1[0] in l_r_d.keys():
            l_r_d[lin1[0]]=lin1[2]
    value_l=[]
    for k in l_r_d.keys():
        value_l.append(l_r_d[k])

    X.append(value_l)
        
    

##data=infile.readlines()
##X = data.images.reshape((len(data.images), -1))
##y = data.target

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
