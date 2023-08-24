import math
import random
import time
import matplotlib.pyplot as plt
import numpy as np

from parameters import *
from helperFunctions import *
from LEACH import *
from LEACHK import *
from Node import *
from Packet import * 

def initializeNodes():
    random.seed(123)
    # Random node distribution
    nodes = []
    for node in range(NUM_NODES):
        location = (random.randrange(FIELD_SIZE['x']), random.randrange(FIELD_SIZE['y']))
        nodes.append(Node(node, location))
    return nodes

def main():

    # Run LEACH and LEACHK
    normalLeach = LEACH(initializeNodes())
    normalLeach.run()
    print("Finished LEACH")
    KmeansLeach = LEACHK(initializeNodes())
    KmeansLeach.run()
    print("Finished LEACH-K")

    # KmeansLeach.drawElbow()

    # Dead nodes per round (Network lifetime)
    plt.figure()
    plt.plot(normalLeach.deadNodesPerRound.keys(), normalLeach.deadNodesPerRound.values(), label='Normal LEACH')
    plt.plot(KmeansLeach.deadNodesPerRound.keys(), KmeansLeach.deadNodesPerRound.values(), label='K-means LEACH')
    plt.xlabel('Round')
    plt.ylabel('Number of dead nodes')
    plt.legend()
    plt.show(block=False)

    # Total energy consumption per round
    plt.figure()
    plt.plot(normalLeach.totalEnergyPerRound.keys(), normalLeach.totalEnergyPerRound.values(), label='Normal LEACH')
    plt.plot(KmeansLeach.totalEnergyPerRound.keys(), KmeansLeach.totalEnergyPerRound.values(), label='K-means LEACH')
    plt.xlabel('Round')
    plt.ylabel('Total Energy Consumed')
    plt.legend()
    plt.show(block=False)

main()