import numpy as np
import random
from code_generator import *
from graph_generator import solve

def genParallel(o, n):
	operations = getOperations(o)
	costs = np.ones((o))
	tasks = operations.copy().reshape((n,o/n))
	machines = tasks.copy()
	result = {
		'operations': operations,
		'costs':      costs,
		'tasks':      tasks,
		'machines':   machines
	}
	return result

def genSteps(o, n):
	operations = getOperations(o)
	costs = np.ones((o))
	tasks = operations.copy().reshape((n,o/n))
	machines = map(list,tasks+1)
	machines[0].insert(0,0)
	del machines[-1][-1]
	result = {
		'operations': operations,
		'costs':      costs,
		'tasks':      tasks,
		'machines':   machines
	}
	return result

def genStepsExtra(o, n):
	operations = getOperations(o+1)
	costs = np.ones((o+1))

	tasks = np.arange(o).reshape((n,o/n))	
	machines = map(list,tasks+1)
	machines[0].insert(0,0)
	del machines[-1][-1]

	tasks = map(list,tasks)
	tasks[-1].append(o)
	machines[0].append(o)

	result = {
		'operations': operations,
		'costs':      costs,
		'tasks':      tasks,
		'machines':   machines
	}
	return result

def genStepsTasks(m):
	o = m*m
	operations = getOperations(o)
	costs = np.ones((o))
	tasks = operations.copy().reshape((m,m))
	machines = [ np.arange(i, m*m, m) for i in range(m) ]
	result = {
		'operations': operations,
		'costs':      costs,
		'tasks':      tasks,
		'machines':   machines
	}
	return result

def genTrivial(o):
	operations = getOperations(o)
	costs = np.ones((o))
	tasks = [operations.copy()]
	machines = tasks
	result = {
		'operations': operations,
		'costs':      costs,
		'tasks':      tasks,
		'machines':   machines
	}
	return result


def main():
	o, n = 12, 4

	data = genParallel(o, n)
	filename = exportToFile(data, 'data/parallel.npy')
	mc = data['costs'].reshape(data['machines'].shape)
	expected = np.max(np.sum(mc, axis=1))
	print 'expected T for parallel:', expected
	print 'result:', solve(filename)

	data = genSteps(o, n)
	filename = exportToFile(data, 'data/steps.npy')
	mc = [ sum(data['costs'][machine]) for machine in data['machines'] ]
	expected = max(mc)
	print 'expected T for steps:', expected
	print 'result:', solve(filename)

	data = genStepsExtra(o, n)
	filename = exportToFile(data, 'data/stepsExtra.npy')
	expected = np.sum(data['costs'])
	print 'expected T for stepsExtra:', expected
	print 'result:', solve(filename)

	m = 5
	data = genStepsTasks(m)
	filename = exportToFile(data, 'data/stepsTasks.npy')
	mc = [ sum(data['costs'][machine]) for machine in data['machines'] ]
	expected = max(mc)
	print 'expected T for stepsTasks:', expected
	print 'result:', solve(filename)

	data = genTrivial(o)
	filename = exportToFile(data, 'data/trivial.npy')
	expected = len(data['operations'])
	print 'expected T for trivial:', expected
	print 'result:', solve(filename)

main()