import pandas as pd
import networkx as nx
import pickle as pkl
import scipy.sparse as sp
import numpy as np
import sys

'''
zhoushan
'''
# import edge list and convert to tuple for input
df = pd.read_csv('Hikvision.edgelist.n0', sep='\t', header=None)
edges = tuple(df.values.tolist())

# create graph and input edges
G = nx.Graph()
G.add_edges_from(edges)

# print note# and edge#
print('The number of notes: {0}.'.format(G.number_of_nodes()))
print('The number of edges: {0}.'.format(G.number_of_edges()))

data = pd.read_csv('Attribution-V1.csv')
data = data.drop('id', axis=1)

# for i in data.columns:
#     nx.set_node_attributes(G, data[i].to_dict(), i)

# add label
nx.set_node_attributes(G, data['label'].to_dict(), 'labels')

# output
nx.write_gml(G, path='zs.gml')


'''
cora
'''
# import edge list and convert to tuple for input
df = pd.read_csv('cora.cites', sep='\t', header=None)
edges = tuple(df.values.tolist())

# create graph and input edges
G = nx.Graph()
G.add_edges_from(edges)

# print note# and edge#
print('The number of notes: {0}.'.format(G.number_of_nodes()))
print('The number of edges: {0}.'.format(G.number_of_edges()))

data = pd.read_csv('cora.content', sep='\t', usecols=[0, 1434], header=None, names=['id', 'labels'])

for i in data['id']:
    G.add_node(i, labels=data['labels'][data['id'] == i].item())

nx.write_gml(G, path='cora.gml')

'''
cora noise
'''
# import edge list and convert to tuple for input
df = pd.read_csv('cora.edgelist.n0.8', sep='\t', header=None)
edges = tuple(df.values.tolist())

# create graph and input edges
G = nx.Graph()
G.add_edges_from(edges)

# print note# and edge#
print('The number of notes: {0}.'.format(G.number_of_nodes()))
print('The number of edges: {0}.'.format(G.number_of_edges()))

# add label
def parse_index_file(filename):
    """Parse index file."""
    index = []
    for line in open(filename):
        index.append(int(line.strip()))
    return index

names = ['x', 'y', 'tx', 'ty', 'allx', 'ally', 'graph']
objects = []
for i in range(len(names)):
    with open("hik/data/ind.{}.{}".format('cora', names[i]), 'rb') as f:
        if sys.version_info > (3, 0):
            objects.append(pkl.load(f, encoding='latin1'))
        else:
            objects.append(pkl.load(f))

x, y, tx, ty, allx, ally, graph = tuple(objects)
test_idx_reorder = parse_index_file("hik/data/ind.{}.test.index".format('cora'))
test_idx_range = np.sort(test_idx_reorder)

labels = np.vstack((ally, ty))  # ty不是按照test序号排列的
labels[test_idx_reorder, :] = labels[test_idx_range, :]  # 使得labels ty部分能够正常的按照节点序号排列

label = []  # label on column index
for el in labels:
    if 1 in el:
        label.append(list(el).index(1))  # self.label存储0-n的分类情况
    else:
        label.append(0)

for i in range(len(label)):
    G.add_node(i, labels=label[i])

nx.write_gml(G, path='cora.noise.gml')
