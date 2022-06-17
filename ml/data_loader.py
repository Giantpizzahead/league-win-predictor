import os
import pickle
import random
from constants import *
import scipy.io
from sklearn.utils import shuffle

x_train = []
y_train = []
x_test = []
y_test = []
# This is an inexact estimate!
test_size = 0.15

print('Loading training examples...')
num_entries = len([name for name in os.listdir(input_folder) if os.path.isfile(input_folder + '/' + name)])
to_process = num_entries
train_batches = 0
random.seed(6456)
for entry in os.scandir(input_folder):
    name = entry.name
    with open(f'{input_folder}/{name}', 'rb') as fin:
        curr_input = pickle.load(fin)
    with open(f'{output_folder}/{name}', 'rb') as fin:
        curr_output = pickle.load(fin)
    # curr_input = curr_input[:1]
    # curr_output = curr_output[:1]
    if random.random() < test_size:
        x_test += curr_input
        y_test += curr_output
    else:
        x_train += curr_input
        y_train += curr_output
        train_batches += 1
    to_process -= 1
    if to_process % 100 == 0:
        print(f'To process: {to_process}')
x_train, y_train = shuffle(x_train, y_train, random_state=1338)
x_test, y_test = shuffle(x_test, y_test, random_state=1339)

print('\nSaving loaded examples...')
with open(f'{ml_data_folder}/x_train.pkl', 'wb') as fout:
    pickle.dump(x_train, fout)
with open(f'{ml_data_folder}/y_train.pkl', 'wb') as fout:
    pickle.dump(y_train, fout)
with open(f'{ml_data_folder}/x_test.pkl', 'wb') as fout:
    pickle.dump(x_test, fout)
with open(f'{ml_data_folder}/y_test.pkl', 'wb') as fout:
    pickle.dump(y_test, fout)

print('\nGenerating Matlab matrices...')
scipy.io.savemat(f'{ml_data_folder}/train.mat', dict(x=x_train, y=y_train))
scipy.io.savemat(f'{ml_data_folder}/test.mat', dict(x=x_test, y=y_test))

print('Complete!')
print(f'{train_batches} training batches, {len(x_train)} training examples')
print(f'{num_entries - train_batches} test batches, {len(x_test)} test examples')
