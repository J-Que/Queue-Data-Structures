import os
import time
import random
import pydot
from PIL import Image
import queue

class job:
    def __init__(self, number, urgency):
        self.number = number
        self.urgency = urgency
    
    # define how two job objects are equal
    def __eq__(self, other):
        return self.urgency == other.urgency
    
    # define how two objects behave with the less the comparator
    def __lt__(self, other):
        return self.urgency < other.urgency

class priority_queue:
    def __init__(self): self.q = []

    def add(self, item):
        self.q.append(item)
        k = len(self.q)
        while k // 2 > 0:
            if self.q[k - 1] > self.q[k//2 - 1]: self.q[k - 1], self.q[k//2 - 1] = self.q[k//2 - 1], self.q[k - 1]
            k//=2

    def min_index(self, k):
        if k*2 + 3 > len(self.q): return k*2 + 1
        elif self.q[k*2 + 1] > self.q[k*2 + 2]: return k*2 + 1
        else: return k*2 + 2
    
    def drop(self):
        self.q[0] = self.q[len(self.q) - 1]
        self.q.pop()
        k = 0
        while k*2 + 1 < len(self.q):
            mi = self.min_index(k)
            if self.q[k] < self.q[mi]: self.q[k], self.q[mi] = self.q[mi], self.q[k]
            k=mi
        
def create_jobs(n): return [job(i, random.randrange(0, 100)) for i in range(n)]

def traverse(q, k, graph):
    if k*2 <= len(q):
        parent = 'Job ' + str(q[k - 1].number) + '\nUrgency: '+ str(q[k - 1].urgency)
        child = 'Job ' + str(q[k*2 - 1].number) + '\nUrgency: '+ str(q[k*2 - 1].urgency)
        edge = pydot.Edge(parent, child)
        graph.add_edge(edge)
        graph = traverse(q, k*2, graph)

        if k*2 + 1 <=len(q):
            child = 'Job ' + str(q[k*2].number) + '\nUrgency: '+ str(q[k*2].urgency)
            edge = pydot.Edge(parent, child)
            graph.add_edge(edge)
            graph = traverse(q, k*2 + 1, graph)

        return graph

    else: return graph
 
def plot(q, q_shape):
    graph = pydot.Dot(graph_type='graph')
    if q_shape == 'line':
        parent = 'Job ' + str(q[0].number) + '\nUrgency: '+ str(q[0].urgency)
        
        for i in q[1:]:
            child = 'Job ' + str(i.number) + '\nUrgency: '+ str(i.urgency)
            edge = pydot.Edge(parent, child)
            graph.add_edge(edge)
            parent = 'Job ' + str(i.number) + '\nUrgency: '+ str(i.urgency)

    if q_shape == 'heap': graph = traverse(q, 1, graph)
    path = os.path.dirname(__file__) + '/queue.png'
    graph.write_png(path)
    Image.open(path).show()

def method1(jobs):
    start, q = time.time(), priority_queue()
    for i in jobs: q.add(i)
    addTime, start = time.time() - start, time.time()
    while len(q.q) != 0: q.drop()
    return addTime, time.time() - start, 'Prioriy Queue Structure'

def method2(jobs):
    start, q = time.time(), []
    for i in jobs:
        q.append(i)
        q.sort()
    
    addTime, start = time.time() - start, time.time()
    while len(q) != 0: q.pop(0)
    return addTime, time.time() - start, 'List Structure'

def method3(jobs):
    start, q = time.time(), queue.PriorityQueue()
    for i in jobs: q.put(i)
    addTime, start = time.time() - start, time.time()
    while not q.empty() != 0: q.get()
    return addTime, time.time() - start, 'Priority Queue from library'

def compare(method):
    addTimes, dropTimes, n = 0, 0, 2000
    for i in range(10):
        time1, time2, method_name = method(create_jobs(n))
        addTimes, dropTimes = addTimes + time1, dropTimes + time2
    print(f'%50s' % method_name + ' ........................................ Avg. Time Adding: {:.3}     Avg Time Dropping: {:.3}'.format(float(addTimes/n), float(dropTimes/n)))

def main():
    print('\nFirst, a set of 7 random job objects are created. Here the jobs contains a job number and an urgency level between 0 and 100 which is used as the priorty attribute.')
    
    jobs = create_jobs(7)
    plot(jobs, 'line')
    
    print('\nNext a priorty queue is initalized and the jobs are added. The queue then priortizes the jobs by its urgency level in non-increasing order.')
    
    q = priority_queue()
    for i in jobs: q.add(i)
    plot(q.q, 'heap')

    print('\nThe first job in the queue is dropped, and the queue is rearranged to have the job with the next highest urgency first in the queue.')
    
    q.drop()
    plot(q.q, 'heap')
    
    print('\nThis method is compared to 2 other methods, one using lists instead of priority queues, and a second using a priority queue object from the queue library.')
    
    print('2,000 random jobs are added individually through each method and then drop one by one, This is done 10 times to get the average times. \n')
    
    compare(method1)
    compare(method2)
    compare(method3)

if __name__ == '__main__': #main()
    graph = pydot.Dot(graph_type='digraph')
    
    root = pydot.Node('x1')

    node_0 = pydot.Node('x2')
    edge_0 = pydot.Edge(root, node_0)
    edge_0.set_label(' 0')

    node_1 = pydot.Node('x2')
    edge_1 = pydot.Edge(root, node_1)
    edge_1.set_label(' 1')

    
    
    graph.add_edge(edge_0)


    path = os.path.dirname(__file__) + '/tree.png'
    graph.write_png(path)
    Image.open(path).show()
