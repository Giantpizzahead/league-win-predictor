import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier

def gen_model(x_train, y_train):
    model = MLPClassifier(hidden_layer_sizes=(3, 2), activation='logistic', solver='adam', max_iter=500, tol=0.00001, verbose=True, alpha=0.5, random_state=987, n_iter_no_change=50)
    model.fit(x_train, y_train)
    # plt.plot(model.loss_curve_)
    # plt.plot(model.validation_scores_)
    plt.show()
    return model
