import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item)) # priority == distance, small number is good
        self._index += 1

    def pop(self):
        if len(self._queue) == 1:
            self._index = 0
        return heapq.heappop(self._queue)[-1]

    def isEmpty(self):
        return not len(self._queue)


class AdjacencyList(object):

    def __init__(self):
        # node's name is device_name.
        self._adjList = {}

    def addGraph(self, **graph):
        self._adjList = graph

    def addEdge(self, xVertex, yVertex):
        # check if vertex is already present
        # Unauthorized and Undirected
        xVertex = str(xVertex)
        yVertex = str(yVertex)
        if xVertex in self._adjList.keys() and yVertex in self._adjList.keys():
            if yVertex not in self._adjList[xVertex] and xVertex not in self._adjList[yVertex]:
                self._adjList[xVertex].append(yVertex)
                self._adjList[yVertex].append(xVertex)
        elif xVertex in self._adjList.keys():
            self._adjList[xVertex].append(yVertex)
            self._adjList[yVertex] = [xVertex]
        elif yVertex in self._adjList.keys():
            self._adjList[yVertex].append(xVertex)
            self._adjList[xVertex] = [yVertex]
        else:
            self._adjList[xVertex] = [yVertex]
            self._adjList[yVertex] = [xVertex]

    def printList(self):
        for i in self._adjList:
            print(str(i), '->', '[' + ', '.join([str(j) for j in self._adjList[i]]) + ']')

    def printAllNode(self):
        return [k for k in self._adjList.keys()]

    def dijkstra(self, src):
        self._srcToAll = {}

        inf = float('inf')
        allNodes = self.printAllNode()

        for node in allNodes:
            self._srcToAll[node] = [node, inf] # from src to node, node: (the previous hop, distance)
        self._srcToAll[src] = [src, 0]

        Q = PriorityQueue()
        Q.push(src, 0)

        while not Q.isEmpty():
            mineNode = Q.pop()
            curDist = self._srcToAll[mineNode][1]
            for adjNode in self._adjList[mineNode]:
                new_dist = curDist + 1
                if new_dist < self._srcToAll[adjNode][1]:
                    if self._srcToAll[adjNode][1] == inf:
                        Q.push(adjNode, new_dist)
                    self._srcToAll[adjNode][0] = mineNode
                    self._srcToAll[adjNode][1] = new_dist

    def multipath(self, src):
        self._srcToAll = {}

        inf = float('inf')
        allNodes = self.printAllNode()

        # initialize information(previous hop and distance) of source node to other nodes.
        # previous hop is from source node to this node's previous hop.
        # distance is from source node to this node's distance
        for node in allNodes:
            self._srcToAll[node] = [node, inf] # from src to node, node: (the previous hop, distance)
        self._srcToAll[src] = [src, 0]

        # push source node to initialize queue and mine its adjnodes.
        Q = PriorityQueue()
        Q.push(src, 0)

        while not Q.isEmpty():
            mineNode = Q.pop()
            curDist = self._srcToAll[mineNode][1]
            for adjNode in self._adjList[mineNode]:
                new_dist = curDist + 1
                if new_dist < self._srcToAll[adjNode][1]:
                    # if it is new, then push it
                    if self._srcToAll[adjNode][1] == inf:
                        Q.push(adjNode, new_dist)
                    self._srcToAll[adjNode][0] = mineNode
                    self._srcToAll[adjNode][1] = new_dist

    def showPath(self, src, dst, mode='multipath'):
        self._path = []

        if self._path and self._srcToAll[src][1] == 0:
            path = self._path
            return path

        if mode == 'multipath':
            self.multipath(src)
        else:
            self.dijkstra(src)
            mid = dst
            while self._srcToAll[mid][1] != 0:
                self._path.append(mid)
                mid = self._srcToAll[mid][0]
            self._path.append(src)
            self._path.reverse()
            path = self._path
            return path





if __name__ == '__main__':
    aj = AdjacencyList()
    aj.addEdge('a', 'b')
    aj.addEdge('c', 'b')
    aj.addEdge('c', 'd')
    aj.addEdge('e', 'd')
    aj.addEdge('e', 'a')
    aj.addEdge('e', 'f')
    aj.addEdge('d', 'f')
    # aj.addGraph(a=['b','c'])
    aj.printList()
    path = aj.showPath('c', 'f')
    print(path)
