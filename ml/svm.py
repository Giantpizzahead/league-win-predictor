from sklearn import svm

def gen_model(x_train, y_train):
    model = svm.SVC(probability=True, C=1, verbose=True)
    model.fit(x_train, y_train)
    print('Model parameters:', model.get_params())
    return model
