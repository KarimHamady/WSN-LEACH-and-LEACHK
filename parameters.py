from math import pow, sqrt
# Field Parameters
FIELD_SIZE = {'x': 100, 'y': 100} # Area is 100x100
SINK_LOCATION = (100, 100)
NUM_NODES = 50

# Radio Parameters

# First Order Energy model parameters
E0 = 0.5 # Joule
EELEC = 50*pow(10, -9)
ETX = 50*pow(10, -9)
ERX = 50*pow(10, -9)
efs = 10*pow(10, -12)
emp = 0.0013*pow(10, -12)
EDA = 5*pow(10, -9)
d0 = sqrt(efs/emp)

# Simulation Parametres
NUM_ROUNDS = 200
NUM_BITS = 2000 # bits
TRANSMISSION_RATE = 250 * pow(10, 3)
PACKETS = []
PATH_LOSS_EXPONENT = 4
LAMBDA = TRANSMISSION_RATE/NUM_BITS
MUE = 1/LAMBDA
DROPPED_PACKETS = 0
DEAD_NODES = 0
DEAD_NODES_PER_ROUND = {}
TOTAL_ENERGY = 0

TXPOWER = 10**(-9)
MINIMUM_MESSAGE_ENERGY = 10**(-12)