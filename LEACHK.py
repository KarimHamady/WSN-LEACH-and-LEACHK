import math
import random
import matplotlib.pyplot as plt

import numpy as np
from sklearn.cluster import KMeans
from helperFunctions import *
from parameters import *
from Packet import Packet


class Visualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 6))

    def drawNodesCurrentRound(self, nodes):
        self.ax.clear()
        colors = ['m', 'c', 'r', 'g', 'b']
        test = []
        self.ax.plot(SINK_LOCATION[0], SINK_LOCATION[1], 'y.', markersize=20)
        for node in nodes:
            color = (0.7, 0.1, 0.2)
            if node.role == 'CH' and node.alive:
                self.ax.plot(node.location[0], node.location[1], 'y.', markersize=15)
                color = colors[node.id % len(colors)]
                if node.alive:
                    self.ax.plot([node.location[0], node.location[0]], [node.location[1], node.location[1]], color=color, marker='.', markersize=random.randint(5, 10))
            if node.alive:
                self.ax.plot(node.location[0], node.location[1], color=color, marker='.', markersize=random.randint(5, 10))
            else:
                self.ax.plot(node.location[0], node.location[1], 'ko', markersize=10)
        
        print(list(set(test)))
        print("____________________________")
        self.fig.canvas.draw()
        plt.pause(0.0001)


class LEACHK:
    def __init__(self, nodes):
        self.P = 0.1
        self.r = 1
        self.nodes = nodes
        self.CHs = []
        self.dataTransmitted = {}
        self.numberOfOperationalNodes = NUM_NODES
        self.pathLossExp = PATH_LOSS_EXPONENT

        self.totalEnergyPerRound = {0:0}
        self.deadNodesPerRound = {0:0}
        self.packets = []


    def aggregateData(self, dataArray):
        return sum(dataArray)/len(dataArray)
        
    def findClosestCH(self, node):
        minDistance = math.inf
        for ch in self.CHs:
            disToCH = distance(node.location, ch.location)
            if disToCH < minDistance:
                minDistance = disToCH
                node.CH = ch
        node.CH.childNodes.append(node)

    
    def setupPhaseKMeans(self):
        self.CHs = []
        positions = []
        for node in self.nodes:
            if node.alive:
                node.role = 'N'
                positions.append([node.location[0], node.location[1]]) 
        positions = np.array(positions)       
        numClusters = 10
        kmeans = KMeans(n_clusters=numClusters, n_init=10)
        kmeans.fit(positions)
        labels = kmeans.labels_
        centroids = np.zeros((numClusters, 2))
        for i in range(numClusters):
            cluster_points = positions[np.where(labels==i)[0]]
            cluster_mean = np.mean(cluster_points, axis=0)
            distances = np.linalg.norm(cluster_points - cluster_mean, axis=1)
            centroids[i] = cluster_points[np.argmin(distances)]
            nodesInCluster = []
            maxEnergy = 0
            potentialCH = -1
            for node in self.nodes:
                if node.location in cluster_points:
                    disToSink = node.distanceToSink
                    EtxCH = EELEC * NUM_BITS + efs * NUM_BITS * math.pow(disToSink, self.pathLossExp)
                    Erx = (EELEC + EDA) * NUM_BITS
                    nodesInCluster.append(node)
                    if node.alive and (node.energy - EtxCH - Erx) > maxEnergy:
                        maxEnergy = node.energy - EtxCH - Erx
                        potentialCH = node
            if potentialCH == -1:
                n = random.choice(nodesInCluster)
                n.role='CH'
                self.CHs.append(n)
            else:
                potentialCH.role = 'CH'
                self.CHs.append(potentialCH)

        # self.nodes[np.where(positions == centroids[i])[0][0]].role = 'CH'
        # self.CHs.append(self.nodes[np.where(positions == centroids[i])[0][0]])
       

    def steadyStatePhase(self):
        efs = 10*pow(10, -12)
        emp = 0.0013*pow(10, -12)
        self.deadNodesPerRound[self.r] = self.deadNodesPerRound[self.r - 1]
        self.totalEnergyPerRound[self.r] = self.totalEnergyPerRound[self.r - 1]
        self.dataTransmitted[self.r] = 0
        
                
        # Data Transmission
        for ch in self.CHs:
            if ch.alive:
                for node in ch.childNodes:
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
                            self.numberOfOperationalNodes -= 1
                            self.deadNodesPerRound[self.r] += 1
                            
                    Erx = (EELEC + EDA) * NUM_BITS
                    if ch.energy > Erx:
                        ch.energy -= Erx
                        self.totalEnergyPerRound[self.r] += Erx
                    else:
                        ch.alive = 0
                        self.deadNodesPerRound[self.r] += 1
                       
        for ch in self.CHs:
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
                    self.numberOfOperationalNodes -= 1
                    self.deadNodesPerRound[self.r] += 1

        self.r += 1

    def run(self, withVisualization=False):
        if withVisualization:
            v = Visualizer()
        while True:
            self.setupPhaseKMeans()
            self.steadyStatePhase()
            if withVisualization:
                v.drawNodesCurrentRound(self.nodes)
            print(self.r, self.deadNodesPerRound[self.r - 1] )
            if self.deadNodesPerRound[self.r - 1] > NUM_NODES//2:
                break
    
    def drawElbow(self):
        # Define the range of k values to test
        k_values = range(1, 15)
        positions = []
        for node in self.nodes:
            if node.alive:
                node.role = 'N'
                positions.append([node.location[0], node.location[1]]) 
        positions = np.array(positions)
        # Calculate the WCSS for each value of k
        wcss_values = []
        for k in k_values:
            kmeans = KMeans(n_clusters=k)
            kmeans.fit(positions)
            wcss_values.append(kmeans.inertia_)

        # Plot the results
        plt.plot(k_values, wcss_values, 'bx-')
        plt.xlabel('k')
        plt.ylabel('WCSS')
        plt.title('The Elbow Method')
        plt.show()
        plt.pause(2)

        # Find the optimal number of clusters
        diffs = np.diff(wcss_values)
        diff_ratios = diffs / diffs[0:-1]
        k_opt = diff_ratios.argmin() + 2 # Add 2 because of zero-based indexing
        print("Optimal number of clusters:", k_opt)
        