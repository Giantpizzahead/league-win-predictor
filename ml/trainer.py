import joblib
import pickle
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.decomposition import PCA
from constants import *
import numpy as np
import decisiontree, logisticreg, neuralnet, svm

print('Loading training data...')

with open(f'{ml_data_folder}/x_train.pkl', 'rb') as fin:
    x_train = pickle.load(fin)
with open(f'{ml_data_folder}/y_train.pkl', 'rb') as fin:
    y_train = pickle.load(fin)
with open(f'{ml_data_folder}/x_test.pkl', 'rb') as fin:
    x_test = pickle.load(fin)
with open(f'{ml_data_folder}/y_test.pkl', 'rb') as fin:
    y_test = pickle.load(fin)

y_train = [v[0] for v in y_train]
y_test = [v[0] for v in y_test]
x_train_orig = x_train
x_test_orig = x_test

# Move some test examples over for early stopping
'''
num_to_move = len(x_train) // 9
x_train = np.concatenate((x_train, x_test[:num_to_move]))
y_train = np.concatenate((y_train, y_test[:num_to_move]))
x_train_orig = np.concatenate((x_train_orig, x_test_orig[num_to_move:]))
x_test = x_test[num_to_move:]
y_test = y_test[num_to_move:]
x_test_orig = x_test_orig[num_to_move:]
'''

# Generate some possibly helpful features
for t in x_train + x_test:
    pass
    '''
    # Sum of each type of skill?
    for i in range(8):
        blue = sum(t[-80+i:-40+i:8])
        red = sum(t[-40+i::8])
        t.append(blue)
        t.append(red)
    # Biased damage type?
    blue = (abs(sum(t[-74:-34:8]) - 2.5) / 2.5) ** 3
    red = (abs(sum(t[-34::8]) - 2.5) / 2.5) ** 3
    t.append(blue)
    t.append(red)
    '''

print('Done!')
print(f'# training examples: {len(x_train)}')
print(f'# test examples: {len(x_test)}')
print(f'# of inputs: {len(x_train[0])}')

# Feature scaling (preprocessing)
poly = preprocessing.PolynomialFeatures(degree=1).fit(x_train)
x_train = poly.transform(x_train)
x_test = poly.transform(x_test)
scaler = preprocessing.StandardScaler().fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

# Principal component analysis
'''
pca = PCA(n_components=0.95, random_state=696)
pca.fit(x_train)
x_train = pca.transform(x_train)
print(f"PCA: # of inputs reduced from {len(x_test[0])} to {len(x_train[0])}")
print(f"% of variance conserved: {sum(pca.explained_variance_ratio_ * 100)}")
x_test = pca.transform(x_test)
'''

# Generate model
model = logisticreg.gen_model(x_train, y_train)

score_train = model.score(x_train, y_train)
score_test = model.score(x_test, y_test)
print(f'Training set score: {score_train}')
print(f'Test set score: {score_test}')
for i in range(1):
    print(f'Test #{i+1}: {x_test_orig[i]}')

# Save model and preprocessing to file
print('Saving model...')
joblib.dump({'preprocess': [poly, scaler], 'model': model}, 'model.gz')

# Visualize predictions
# x_test_orig = np.concatenate((x_train_orig, x_test_orig))
# x_test = np.concatenate((x_train, x_test))
# y_test = np.concatenate((y_train, y_test))
predictions = model.predict(x_test)
probabilities = [v[0] for v in model.predict_proba(x_test)]
N = len(x_test)

fig, axs = plt.subplots(2, 2)
x = []
y = []
colors = [[], [], []]
alpha = []
for i in range(N):
    t = x_test_orig[i]
    blue = sum(t[19:44:5])
    red = sum(t[44:69:5])
    y.append(blue-red)
    game_time = t[0] / 60
    x.append(game_time)
    colors[0].append('g' if predictions[i] == y_test[i] else 'r')
    colors[1].append('b' if predictions[i] else 'r')
    colors[2].append('b' if y_test[i] else 'r')
    alpha.append(abs(probabilities[i]-0.5)*1.5+0.25)
s = 8

'''
axs[0, 0].set_xlabel("Game time (minutes)")
axs[0, 0].set_ylabel("Kill diff")
axs[0, 0].set_title('Correct vs Wrong Predictions')
axs[0, 0].scatter(x, y, c=colors[0], s=s, alpha=alpha)
'''

axs[1, 0].set_xlabel("Game time (minutes)")
axs[1, 0].set_ylabel("Kill diff")
axs[1, 0].set_title('Predictions')
axs[1, 0].scatter(x, y, c=colors[1], s=s, alpha=alpha)

'''
axs[1, 1].set_xlabel("Game time (minutes)")
axs[1, 1].set_ylabel("Kill diff")
axs[1, 1].set_title('Actual')
axs[1, 1].scatter(x, y, c=colors[2], s=s)
'''

# Visualize percentage correct at each time
num_correct = {}
for i in range(N):
    t = x_test_orig[i]
    game_time = round(t[0] / 60)
    if not game_time in num_correct:
        num_correct[game_time] = [0, 0]
    if predictions[i] == y_test[i]:
        num_correct[game_time][0] += 1
    num_correct[game_time][1] += 1
num_correct = dict(sorted(num_correct.items()))
x = []
y = []
for t, v in num_correct.items():
    x.append(t)
    y.append(v[0] / v[1])

axs[0, 1].set_xlabel("Game time (minutes)")
axs[0, 1].set_ylabel("% correct")
axs[0, 1].set_title("Correct Predictions vs. Game Time")
axs[0, 1].set_ylim([0, 1])
axs[0, 1].bar(x, y, color='g')

# Visualize percentage correct at each confidence level
confidence = [[0, 0] for _ in range(101)]
for i in range(N):
    v = round(probabilities[i] * 100)
    if predictions[i] == y_test[i]:
        confidence[v][0] += 1
    confidence[v][1] += 1
x = [i for i in range(101)]
y = [0 if confidence[i][1] == 0 else confidence[i][0] / confidence[i][1] for i in range(101)]

axs[1, 1].set_xlabel("% confidence")
axs[1, 1].set_ylabel("% correct")
axs[1, 1].set_title("Correct Predictions vs. Confidence")
axs[1, 1].set_ylim([0, 1])
axs[1, 1].bar(x, y, color='g')

# Visualize percentage guessed at each confidence
confidence = [0 for _ in range(101)]
for i in range(N):
    v = round(probabilities[i] * 100)
    confidence[v] += 1
x = [i for i in range(101)]
y = [confidence[i] for i in range(101)]

axs[0, 0].set_xlabel("Predicted win %")
axs[0, 0].set_ylabel("# predictions")
axs[0, 0].set_title("# of Predictions vs. Predicted Win %")
axs[0, 0].bar(x, y, color='g')

# Random variable testing
'''
x = []
y = []
color = []
alpha = []
for i in range(N):
    t = x_test_orig[i]
    blue = sum(t[-75:-35:8])
    red = sum(t[-35::8])
    x.append(blue)
    y.append(red)
    color.append('b' if y_test[i] else 'r')
    # alpha.append(abs(probabilities[i]-0.5)*1.5+0.25)
s = 8
axs[0, 1].set_xlabel("Blue damage type")
axs[0, 1].set_ylabel("Red damage type")
axs[0, 1].set_title("Damage Type vs. Winner")
axs[0, 1].scatter(x, y, s=s, color=color)
'''

plt.show()

'''
wrong_prob = []
for i in range(N):
    if y_test[i] != predictions[i]:
        wrong_prob.append(probabilities[i][0])
wrong_prob = sorted(wrong_prob)
print(wrong_prob)

for i in range(len(x_test)):
    if y_test[i] != predictions[i]:
        print(f'Wrong: {x_test[i]} predicted {predictions[i]} when the answer was {y_test[i]}\n')
'''
