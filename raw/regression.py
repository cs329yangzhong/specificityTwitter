import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from scipy.stats import spearmanr
from sklearn.svm import SVR, LinearSVR
from sklearn import metrics
from sklearn.model_selection import cross_validate, GridSearchCV
from sklearn.metrics import classification_report
'''
df_train = pd.read_csv("testForAllFeatures_Check_label_BC.csv", skip_blank_lines=True)
df_test = pd.read_csv("testForAllFeatures_testSet_BC.csv", skip_blank_lines=True)

X_train = df_train.iloc[:, 4:10]

y_train = df_train.iloc[:, 3]

X_test_a = df_test.iloc[:, 4:10]
# print(X_test.head())
y_test_a = df_test.iloc[:, 2]
# For validate, Choose the first 200 examples of Weijen's data.
X_test = X_test_a[:200]
y_test = y_test_a[:200]
y_train_svr = df_train.iloc[:, 2]
print(y_test)'''

############## Base Lines for embeddings.
# X_train = df_train.iloc[:,10:]
# y_train = df_train.iloc[:,3]
# print(X_train.head())
# X_test_a = df_test.iloc[:,11:]

# y_test_a = df_test.iloc[:,3]
# X_test = X_test_a[:200]
# y_test = y_test_a[:200]
##################### logistic Regression. newton_CG is the best.
def testLogistic(X_train, y_train, X_test, y_test):
    best_C = 0
    best_mae = 1
    Clist = []
    maeList = []
    best_pred = []
    for C in np.arange(0.034, 0.35, 0.1):
        logreg = LogisticRegression(solver="newton-cg", max_iter=500, multi_class="multinomial", C=C)
        logreg.fit(X_train, y_train)
        y_predict = logreg.predict(X_test)
        mae = np.mean([abs(y_predict[i] - list(y_test)[i]) for i in range(len(y_predict))])
        Clist.append(C)
        maeList.append(mae)
        if mae < best_mae:
            best_C = C
            best_mae = mae
            best_param = logreg.get_params()
            best_pred = y_predict
    return y_predict




# logreg = LogisticRegression(solver= "newton-cg", max_iter=200, multi_class= "multinomial")
# logreg.fit(X_train, y_train)
# y_predict = logreg.predict(X_test)
# print("By using newton-cg solver" )
# print("spearman Correlation is: " , spearmanr(y_predict, list(y_test)))
# Mae = np.mean([abs(y_predict[i] - list(y_test)[i]) for i in range(len(y_predict))])
# print("MAE is ", Mae)
# print()

def testLinear():
    # Linear Regression.
    linearReg = LinearRegression()
    linearReg.fit(X_train, y_train)
    y_predict_linear = linearReg.predict(X_test)
    print("By using LinearRegression")
    print(spearmanr(y_predict_linear, list(y_test)))
    print(linearReg.get_params())
    Mae = np.mean([abs(y_predict_linear[i] - list(y_test)[i]) for i in range(len(y_predict_linear))])
    print("Mae for LinearRegression is: ", Mae)


def testRBFSVR(X_train, y_train_svr, X_test, y_test=False, C=0.1, gamma=0.1):
    # SVR trained to tune hyper-parameter.
    regr = SVR(kernel="rbf", C=C, gamma=gamma)
    regr.fit(X_train, y_train_svr)
    y_predict = regr.predict(X_test)
    try:
        mae = np.mean([abs(y_predict[i] - list(y_test)[i]) for i in range(len(y_predict))])
    except TypeError:
        mae = 0
    return mae, y_predict


###### Test for best hyper-parameter.
# 	svr_rbf = SVR(kernel='rbf', C=6.1, gamma=0.01)
# # For regression, use accurate score as training data.
# 	y_rbf = svr_rbf.fit(X_train, y_train_svr).predict(X_test)
# 	print("Mae for rbf svr", np.mean([abs(y_rbf[i] - list(y_test)[i]) for i in range(len(y_rbf))]))


def testPOLYSVR():
    # best_C = 0
    # best_mae = 1
    # Clist = []
    # maeList = []
    # for C in np.arange(0.1,100,1):
    # 	regr = SVR(kernel= "poly", C= C,degree=2)
    # 	regr.fit(X_train, y_train_svr)
    # 	y_predict = regr.predict(X_test)
    # 	mae = np.mean([abs(y_predict[i] - list(y_test)[i]) for i in range(len(y_predict))])
    # 	Clist.append(C)
    # 	maeList.append(mae)
    # 	if mae < best_mae:
    # 		best_C = C
    # 		best_mae = mae
    # 		best_param = regr.get_params()
    # 	# print("Mae for linearSVR with C%f"%C, np.mean([abs(y_predict[i] - list(y_test)[i]) for i in range(len(y_predict))]))
    # print("for best_mae is ",best_mae, "at C = ",best_C)
    # plt.plot(Clist,maeList)
    # plt.show()

    svr_poly = SVR(kernel='poly', C=1e3, degree=2)
    y_poly = svr_poly.fit(X_train, y_train_svr).predict(X_test)
    print("Mae for Poly svr", np.mean([abs(y_poly[i] - list(y_test)[i]) for i in range(len(y_predict))]))


def testLinearSVR(X_train, y_train_svr, X_test, y_test, c, n=None):
    # Try linear SVR.
    regr = LinearSVR(random_state=0, C=c)
    regr.fit(X_train, y_train_svr)
    y_predict = regr.predict(X_test)
    mae = np.mean([abs(y_predict[i] - list(y_test)[i]) for i in range(len(y_predict))])
    return mae, y_predict


def get_5_mae(predicted, test):
    for i in test:
        pass


if __name__ == '__main__':
    testRBFSVR()
