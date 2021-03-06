from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pickle as pkl

from pygcnn.utils import *
from pygcnn.indexing import *
from pygcnn.layers import *

# Load Citeseer graph
X, Y, citeseer_graph = load_citeseer("data/citeseer/citeseer.content", "data/citeseer/citeseer.cites")

train_ids = []
for i in range(7):
	samples = np.where(Y[:,i] == 1.)[0].flatten()
	train_ids.append(np.random.choice(samples, 20))

train_ids = np.concatenate(train_ids, axis=0)
test_ids = np.setdiff1d(np.array(range(Y.shape[0])), train_ids)

# Make Citeseer dataset
citeseer = Dataset('citeseer', X, Y, split=(train_ids, test_ids))

dataset_params = { \

	'dataset': citeseer \

}

graph_params = { \

	'G': citeseer_graph, \
	'depth': 1 \

}

mlp_params = { \

	'batch_size': 10, \
	'n_node_features': 3702, \
	'n_target_features': 6, \
	'signal_time': 16, \
	'index_hidden': 32, \
	'n_layers': 1, \
	'filter_shape': [[16, 64, 3702]], \
	'mlp_hidden': 32, \
	'act_fun': [tf.nn.elu] \

}

def citeseer_loss(true, pred):
	return tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=true, logits=pred))

learning_params = { \

	'cost_function': citeseer_loss, \
	'optimizer': tf.train.AdamOptimizer, \
	'learning_rate': 1e-3, \
	'l2_lambda': 5e-3
	
}

gNet = GraphNetwork('citeseer', dataset_params, graph_params, mlp_params, learning_params, orientation='node')

for i in range(8000):
	gNet.run('train')
	if i % 25 == 0:
		avg_acc = 0
		for j in range(25):
			cost, acc = gNet.run('test')
			avg_acc += acc
		print "\nAverage test accuracy: " + str(avg_acc / 25.0)
