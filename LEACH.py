import math
import random
import time
import matplotlib.pyplot as plt
from helperFunctions import *
from parameters import *
from Packet import Packet

class Visualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 6))

    def drawNodesCurrentRound(self, nodes):
        self.ax.clear()
        colors = ['m', 'c', 'r', 'g', 'b']
        self.ax.plot(SINK_LOCATION[0], SINK_LOCATION[1], 'y.', markersize=20)
        for node in nodes:
            color = (0.7, 0.1, 0.2)
            if node.CH != -1 and node.CH.alive:
                self.ax.plot(node.CH.location[0], node.CH.location[1], 'y.', markersize=15)
                color = colors[node.CH.id % len(colors)]
                if node.alive:
                    self.ax.plot([node.location[0], node.CH.location[0]], [node.location[1], node.CH.location[1]], color=color, marker='.', markersize=random.randint(5, 10))
            if node.alive:
                self.ax.plot(node.location[0], node.location[1], color=color, marker='.', markersize=random.randint(5, 10))
            else:
                self.ax.plot(node.location[0], node.location[1], 'ko', markersize=10)
        
        self.fig.canvas.draw()
        plt.pause(1)


class LEACH:
    def __init__(self, nodes):
        self.P = 0.1
        self.r = 1
        self.nodes = nodes
        self.CHs = {}
        self.pathLossExp = PATH_LOSS_EXPONENT
        
        self.totalEnergyPerRound = {0:0}
        self.deadNodesPerRound = {0:0}
        self.dataTransmitted = {}
        self.packets = []

    def stochasticThresholdAlgorithm(self, n): # r:round n: Node id
        return self.P/(1 - self.P * (self.r%(1/self.P))) 

    def aggregateData(self, dataArray):
        return sum(dataArray)/len(dataArray)

    def findClosestCH(self, node):
        minDistance = math.inf
        selected_cluster = -1
        for ch in self.CHs.keys():
            disToCH = distance(node.location, ch.location)
            if disToCH < minDistance:
                minDistance = disToCH
                selected_cluster = ch
        if selected_cluster != -1:
            self.CHs[selected_cluster].append(node)
            node.CH = selected_cluster

    def setupPhase(self):
        self.CHs = {}
        for node in self.nodes:
            node.role ='N'
            node.CH = -1
            randomNumber = random.random() # uniform distribution between 0 and 1
            T = self.stochasticThresholdAlgorithm(node.id)
            if randomNumber < T and node.roundRemainingToCH == 0:
                node.role = 'CH'
                node.roundRemainingToCH = 1/self.P
                self.CHs[node] = []
            if node.roundRemainingToCH > 0:
                node.roundRemainingToCH -= 1
    

    def steadyStatePhase(self):
        efs = 10*pow(10, -12)
        emp = 0.0013*pow(10, -12)
        self.deadNodesPerRound[self.r] = self.deadNodesPerRound[self.r - 1]
        self.totalEnergyPerRound[self.r] = self.totalEnergyPerRound[self.r - 1]
        self.dataTransmitted[self.r] = 0

        # Maintaining the CHs
        for node in self.nodes:
            if node.role == 'N' and node.alive:
                self.findClosestCH(node)
                
        # Data Transmission
        for ch in self.CHs.keys():
            if ch.alive:
                for node in self.CHs[ch]:
                    if node.alive:
                        # Energy dissipated when nodes send data to CH
                        disToCH = distance(node.location, ch.location)
                        if disToCH >= d0:
                            efs = emp 
                        Etx = EELEC*NUM_BITS + efs*NUM_BITS * math.pow(disToCH, self.pathLossExp)
                        if node.energy > Etx:
                            node.energy -= Etx
                            node.dataTransmitted += NUM_BITS
                            self.totalEnergyPerRound[self.r] += Etx
                            p = Packet(node, ch)
                            self.packets.append(p)
                        else:
                            node.alive = 0
                            self.deadNodesPerRound[self.r] += 1
                            
                    Erx = (EELEC + EDA) * NUM_BITS
                    if ch.energy > Erx:
                        ch.energy -= Erx
                        self.totalEnergyPerRound[self.r] += Erx
                    else:
                        ch.alive = 0
                        self.deadNodesPerRound[self.r] += 1
                        
        for ch in self.CHs.keys():
            if ch.alive:
                disToSink = distance(ch.location, SINK_LOCATION)
                if disToSink >= d0:
                    efs = emp 
                EtxCH = EELEC * NUM_BITS + efs * NUM_BITS * math.pow(disToSink, self.pathLossExp)
                if ch.energy > EtxCH:
                    ch.energy -= EtxCH
                    self.totalEnergyPerRound[self.r] += EtxCH
                    self.dataTransmitted[self.r] += NUM_BITS
                    ch.dataTransmitted += NUM_BITS
                else:
                    ch.alive = 0
                    self.deadNodesPerRound[self.r] += 1

        self.r += 1
        

    def run(self, withVisualization=False):
        if withVisualization:
            v = Visualizer()
        while True:
            self.setupPhase()
            self.steadyStatePhase()
            if withVisualization:
                v.drawNodesCurrentRound(self.nodes)
            if self.deadNodesPerRound[self.r - 1] > NUM_NODES//2:
                break
            
