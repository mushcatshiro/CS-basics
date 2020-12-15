import random
import math
import os
import itertools
"""
partitioner is excluded as we only initiate same number of reducer as unique key
we will be running sequentially instead of concurrently to stimulate parallelism
removing worker class as it just a representation of M and R

improvements
- utilizing multiprocessing for parallelization
"""


class Master():
    """docstring for Master"""

    def __init__(self):
        self.directory = os.path.join(os.getcwd(), 'gutenberg project.txt')
        self.lineList = []
        self.inputLen = -1  # or 0?
        self.intermediateOutput = []
        self.finalOutput = []

    def split_task(self):
        with open(self.directory, 'r') as rf:
            for line in rf:
                if line != '\n':
                    self.lineList.append(line)
        self.inputLen = len(self.lineList)
        return True

    def run(self):
        # ignoring all state handling
        # only call reducer when all mapper has finished their work
        for inp in self.lineList:
            # call workers
            tmpWorker = Mapper(inp)
            self.intermediateOutput.append(tmpWorker.run())

        shuffle = Partition(self.intermediateOutput, 5)
        self.intermediateOutput = shuffle.run()

        assert len(self.intermediateOutput) == 5
        # shuffle into 5 chuck and initiate 5 reducer

        for chunk in self.intermediateOutput:
            tmpWorker = Reducer(chunk)
            self.finalOutput.append(tmpWorker.run())

        for dic in self.finalOutput:
            print(dict(itertools.islice(dic.items(), 5)))
        return True


class Worker():
    """
    docstring for Worker
    should have better way to pass in name eg. mapper into ack
    """

    def __init__(self):
        self.instanceID = math.floor(random.random() * 100_000)
        self.ack = self.ack()

    def ack(self):
        print(f'running instance {self.instanceID}')
        return True


class Mapper(Worker):
    """docstring for Mapper"""

    def __init__(self, line):
        Worker.__init__(self)
        self.line = line.lower().split(' ')
        self.counter = {}

    def run(self):
        # ignoring the punctuations for efficiency
        for word in self.line:
            if word not in self.counter:
                self.counter[word] = 1
            else:
                self.counter[word] += 1
        print(f'completed mapper instance {self.instanceID}')
        return self.counter

    def ack(self):
        print(f'running mapper instance {self.instanceID}')
        return True


class Reducer(Worker):
    """
    docstring for Reducer
    in this case it should be a indentity funciton
    """

    def __init__(self, finalOutput):
        Worker.__init__(self)
        self.finalOutput = finalOutput

    def run(self):
        self.finalOutput = {k: v for k, v in sorted(self.finalOutput.items(),
                                                    key=lambda item: item[1],
                                                    reverse=True)}
        return self.finalOutput

    def ack(self):
        print(f'running reducer instance {self.instanceID}')
        return True


class Partition(Worker):
    """
    docstring for Partition
    take in a list of dict
    go through each dict and aggregate by key over counts
    for each key call a reducer

    """

    def __init__(self, intermediateOutput, chunkNum):
        Worker.__init__(self)
        self.intermediateOutput = intermediateOutput
        self.chunk = len(self.intermediateOutput) / chunkNum
        self.chunkNum = chunkNum
        self.shuffleOut = []

    def run(self):
        assert type(self.intermediateOutput) == list, 'wrong type'
        for i in range(self.chunkNum):
            start = i * self.chunk
            end = ((i + 1) * self.chunk) - 1
            # print(self.intermediateOutput[int(start): int(end)])
            tmpChunk = self._run(self.intermediateOutput[int(start): int(end)])
            self.shuffleOut.append(tmpChunk)

        return self.shuffleOut

    def _run(self, chunk):
        output = {}
        for dic in chunk:
            for item in dic:
                if item not in output:
                    output[item] = 1
                else:
                    output[item] += 1
        return output

    def ack(self):
        print(f'running Partition instance {self.instanceID}')
        return True


def test():
    master = Master()
    master.split_task()
    master.run()


if __name__ == '__main__':
    test()
