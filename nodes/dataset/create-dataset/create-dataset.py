import json
import pandas
import os
import sys

dir = os.path.split(os.path.abspath(__file__))[0]
conf = dir + '\\config_' + sys.argv[1] + '.json'
config = json.load(open(conf, 'r'))
os.remove(conf)

df = pandas.read_csv(config['path'], header=None)

r, c = df.shape

if config['shuffle']:
	df = df.sample(frac=1, random_state=config['seed'])

x_train = df.iloc[: int(r * config['trainingPartition']), config['input']]
y_train = df.iloc[: int(r * config['trainingPartition']), config['output']]

x_test = df.iloc[int(r * config['trainingPartition']) :, config['input']]
y_test = df.iloc[int(r * config['trainingPartition']) :, config['output']]

x_train[c - 1] = y_train
x_test[c - 1] = y_test

if not os.path.isdir(config['save']):
	os.makedirs(config['save'], exist_ok=True)

out_train = open(config['save'] + '\\train.json', 'w')
out_test = open(config['save'] + '\\test.json', 'w')

out_train.write(json.dumps(x_train.values.tolist()))
out_test.write(json.dumps(x_test.values.tolist()))

out_train.close()
out_test.close()

print('Dataset created.')