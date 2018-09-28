import random
import math


# Responsible for the directions behind the evolvingTurtle
class Brain:
    
    # Initiates Brain with size number of angles in radians
    def __init__(self, size):
        self.directions = []
        self.step = 0
        for i in range(size):
            self.directions.append(random.uniform(0, 2 * math.pi))

    # Has one percent chance of changing each direction
    def mutate(self):
        for i in range(len(self.directions)):
            if random.uniform(0, 1) <= 0.01:
                self.directions[i] = random.uniform(0, 2 * math.pi)
    
    # Replaces the directions with the given directions and resets the steps
    def replace(self, directions):
        self.step = 0
        self.directions = directions
