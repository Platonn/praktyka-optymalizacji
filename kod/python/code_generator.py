import numpy as np
import random
import time
import datetime


def genParameters():
	n = m = 3  # for simplicity: same number of machines as tasks
	o_per_n = o_per_m = 4  # for simplicity: same number of operations in task as in machine
	o = n * o_per_n
	maxCost = 100
	return (o, n, o_per_n, m, o_per_m, maxCost)


def genData((o, n, o_per_n, m, o_per_m, maxCost)):
	operations = getOperations(o)
	costs = genCosts(operations, maxCost)
	tasks = genSubsequences(operations, n, o_per_n)
	machines = genSubsequences(operations, m, o_per_m)
	result = {
		'operations': operations,
		'costs':      costs,
		'tasks':      tasks,
		'machines':   machines
	}
	return result


def genCosts(operations, maxCost):
	return np.array([random.randint(1, maxCost) for i in operations])


def genSubsequences(operations, num, o_per_num):
	tasks = []
	for i in range(0, num):
		subsequence = sorted(random.sample(operations, o_per_num))
		tasks.append(subsequence)
		operations = [i for i in operations if i not in subsequence]  # tasks - subsequence
	return tasks


def getOperations(o):
	return np.arange(o)


def exportToFile(data, filename=None):
	if filename is None:
		filename = genFilename()
	np.save(filename, data)
	return filename


def importFromFile(filename):
	return np.load(filename)


def genFilename():
	dir = 'data/'
	ext = '.npy'
	timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
	result = dir + timestamp + ext
	return result


def main():
	parameters = genParameters()
	data = genData(parameters)

	filename = exportToFile(data)
	loadedData = importFromFile(filename)
	print loadedData


#main()