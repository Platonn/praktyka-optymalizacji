import numpy as np
import scipy.sparse

from code_generator import *

def genGraphData(costs, tasks, machines):
	edges = {}
	# technological order edges:
	for task in tasks:
		for i in range(len(task)-1):
			edges[task[i], task[i+1]] = costs[task[i+1]]
	# machine chronological order edges:
	for machine in machines:
		for i in range(len(machine)-1):
			edges[machine[i], machine[i+1]] = costs[machine[i+1]]
	indices = np.array(edges.keys(), np.uint32)
	from_o = indices[..., 0]
	to_o = indices[..., 1]
	weights = np.array(edges.values(), np.float32)
	return from_o, to_o, weights

def genSuperGraphData(costs, machines, from_o, to_o, weights):
	o = len(costs)
	m = len(machines)
	e = len(weights)
	super_from_o = np.zeros((e+m)*(m+1), np.uint32)
	super_to_o = np.zeros((e+m)*(m+1), np.uint32)
	super_weights = np.zeros((e+m)*(m+1), np.float32)
	
	bridges_from_o, bridges_to_o, bridges_weights = genSGBridgesData(costs, machines)
	
	for i in range(m+1):
		offset = i*(e+m)
		super_from_o[offset:offset+e] = from_o+(o*i)
		super_to_o[offset:offset+e] = to_o+(o*i)
		super_weights[offset:offset+e] = weights
		if i < m+1:
			super_from_o[offset+e:offset+e+m] = bridges_from_o+(o*i)
			super_to_o[offset+e:offset+e+m] = bridges_to_o+(o*i)
			super_weights[offset+e:offset+e+m] = bridges_weights

	wf_from_o, wf_to_o, wf_weights = genSGWeightsFixData(costs, machines)
	super_from_o[-m:] = wf_from_o
	super_to_o[-m:] = wf_to_o
	super_weights[-m:] = wf_weights

	return super_from_o, super_to_o, super_weights

# edges between i-th and (i+1)-th component
def genSGBridgesData(costs, machines):
	o = len(costs)
	m = len(machines)
	bridges_from_o = np.zeros(m, np.uint32)
	bridges_to_o = np.zeros(m, np.uint32)
	bridges_weights = np.zeros(m, np.float32)
	for i in range(len(machines)):
		bridges_from_o[i] = machines[i][-1]
		bridges_to_o[i] = machines[i][0] + o
		bridges_weights[i] = costs[machines[i][0]]
	return bridges_from_o, bridges_to_o, bridges_weights

# edges to fix 'vertex weight' problem
def genSGWeightsFixData(costs, machines):
	o = len(costs)
	m = len(machines)
	
	index_offset = o*(m+1)
	wf_from_o =  np.arange(m, dtype=np.uint32) + index_offset
	wf_to_o = np.zeros(m, np.uint32)
	wf_weights = np.zeros(m, np.float32)
	for i in range(len(machines)):
		wf_to_o[i] = machines[i][0]
		wf_weights[i] = costs[machines[i][0]]
	return wf_from_o, wf_to_o, wf_weights

def csGraphFromEdges(from_o, to_o, weights, o, m):
	# csr_matrix constructor is adding duplicates together
	N = (m+1)*o+m
	csr = scipy.sparse.csr_matrix((weights, (from_o, to_o)), shape=(N,N))
	return csr

def main():
	data = importFromFile("data/2017-01-06-00-31-56.npy")
	# SPIKE: hard hack - because of wrong save format as np.array
	# >>> data
	# array({ ... }, dtype=object)
	# >>> data[None][0]
	# { ... }
	data = data[None][0]
	fr,to,we = genGraphData(data['costs'], data['tasks'], data['machines'])
	sf, st, sw = genSuperGraphData(data['costs'], data['machines'], fr, to, we)
	csg = csGraphFromEdges(sf, st, sw, len(data['costs']), len(data['machines']))

	print csg
	print csg * -1


main()