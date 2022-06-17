import joblib

print('Loading model...')
preprocess, model = joblib.load('model.gz').values()
print('Model loaded!\n')


def predict(x):
    x = [x]
    for p in preprocess:
        x = p.transform(x)
    y = 1 - model.predict_proba(x)[0][0]
    return y


def gen_and_predict(x, players):
    for i in range(10):
        x += players[i]
    return predict(x)
