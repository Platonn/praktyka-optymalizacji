import numpy as np
import random
from code_generator import *

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
	print 'expected T for parallel:', o/n


	data = genSteps(o, n)
	filename = exportToFile(data, 'data/steps.npy')
	print 'expected T for steps:', o/n+1

	data = genStepsExtra(o, n)
	filename = exportToFile(data, 'data/stepsExtra.npy')
	print 'expected T for stepsExtra:', o+1

	m = 5
	data = genStepsTasks(m)
	filename = exportToFile(data, 'data/stepsTasks.npy')
	print 'expected T for stepsTasks:', m

	data = genTrivial(o)
	filename = exportToFile(data, 'data/trivial.npy')
	print 'expected T for trivial:', o

main()