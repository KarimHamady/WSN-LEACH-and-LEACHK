from helperFunctions import distance, propagationDelay

class Packet:
    def __init__(self, sourceNode, destinationNode):
        self.source = sourceNode
        self.propDelay = propagationDelay(distance(sourceNode.location, destinationNode.location)) 
        self.queuingDelay = 0
        self.transmissionDelay = 0 # (NUM_BITS*2)/TRANSMISSION_RATE
        self.endToEndDelay = self.propDelay + self.transmissionDelay + self.queuingDelay
