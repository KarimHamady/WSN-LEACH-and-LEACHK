import random
from parameters import TXPOWER, E0, SINK_LOCATION
from helperFunctions import distance


class Node:
    def __init__(self, id, location):
        # Cluster related
        self.role = 'N'
        self.CH = -1 # -1 doesn't belong to any
        self.distanceToCH = -1 # Still no cluster head
        self.roundRemainingToCH = 0
        self.childNodes = []

        # Power related
        self.txPower = TXPOWER
        self.threshold = 10
        self.energy = E0

        # Node related
        self.id = id
        self.alive = 1

        # Location Related
        self.location = location
        self.distanceToSink = distance(self.location, SINK_LOCATION)

        # Throughput related
        self.dataTransmitted = 0
        self.roundsToSink = -1