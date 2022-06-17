from sklearn.linear_model import LogisticRegression

def gen_model(x_train, y_train):
    model = LogisticRegression(C=1, max_iter=1000, verbose=False)
    model.fit(x_train, y_train)
    print('Model parameters:', model.get_params())
    print('Coefficients:', model.coef_)
    print('Intercept:', model.intercept_)
    return model
