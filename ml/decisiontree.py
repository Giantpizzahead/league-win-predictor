from sklearn.tree import DecisionTreeClassifier

def gen_model(x_train, y_train):
    model = DecisionTreeClassifier(max_depth=6)
    model.fit(x_train, y_train)
    print('Model parameters:', model.get_params())
    return model
