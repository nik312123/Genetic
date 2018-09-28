import random

from evolvingTurtle import EvolvingTurtle
from goal import Goal


# All of the EvolvingTurtles currently living
class Population:
    goal = None
    
    # Initializes Population with EvolvingTurtles
    def __init__(self, size, x, y):
        self.setup_done = False
        self.start = None
        self.turtles = []
        self.fitness_sum = 0
        self.gen = 1
        self.best_turtle = None
        self.original_x = x
        self.original_y = y
        self.min_step = size
        self.size = size
        self.is_changing = False
        for i in range(size):
            self.turtles.append(EvolvingTurtle(x, y, self))
        self.goal = Goal(0, 275)
        self.setup_done = True
        print(f"Generation {self.gen}")
    
    # Sets start to a reference to the start point and gives the goal start point and population references
    def set_start(self, start):
        self.start = start
        self.start.set_goal(self.goal)
        self.goal.set_start(start)
        self.goal.set_population(self)
    
    # Gets the coordinates of the goal
    def get_goal_cors(self):
        return self.goal.get_goal()
    
    # Moves all living EvolvingTurtles
    def move(self):
        for turtle in self.turtles:
            if not self.is_changing:
                if turtle.brain.step > self.min_step:
                    turtle.die()
                turtle.move()
    
    # Returns true if all of the turtles are dead
    def all_dead(self):
        for turtle in self.turtles:
            if turtle.not_dead() and not turtle.at_goal():
                return False
        return True
    
    # Makes all of the EvolvingTurtles calculate their fitnesses
    def calculate_fitness(self):
        for turtle in self.turtles:
            turtle.calculate_fitness()
    
    # Generates new turtles based on selected parents and re-adds best turtle as a child
    def natural_selection(self):
        # Prepares dictionary for storage of replacements and gets best turtle things ready
        selections = {}
        best_turtle_index = self.get_best_turtle_index()
        best_directions = self.turtles[best_turtle_index].brain.directions
        
        # Gets the total sum of the fitnesses of the turtle and takes selections of parents with proababilities of
        # being chosen related to fitnesses
        self.calculate_fitness_sum()
        for i in range(len(self.turtles)):
            if i != best_turtle_index:
                parent = self.select_parent()
                selections[i] = parent
        
        # Actually replaces old turtles with chosen parents
        for index in selections:
            self.turtles[index].replace_turtle(self.original_x, self.original_y, selections[index].brain.directions[:])
        
        # Sets the best turtle up and adds it
        best_turtle = EvolvingTurtle(self.original_x, self.original_y, self, best_directions[:])
        best_turtle.color("black", "#FFD700")
        self.turtles[best_turtle_index].clear()
        self.turtles[best_turtle_index].hideturtle()
        self.turtles.pop(best_turtle_index)
        self.turtles.append(best_turtle)

        # Increases the generation number
        self.gen += 1
        print(f"Generation {self.gen}")
    
    # Selects a parent using probability with higher fitness making a higher chance of being chosen as a parent
    def select_parent(self):
        parent = random.uniform(0, self.fitness_sum)
        current_sum = 0
        for turt in self.turtles:
            current_sum += turt.get_fitness()
            if current_sum >= parent:
                return turt
        return None
    
    # Calculates the sum of all of the EvolvingTurtle's fitnesses
    def calculate_fitness_sum(self):
        self.fitness_sum = sum(turtle.get_fitness() for turtle in self.turtles)
    
    # Mutates all of the children
    def mutate_turtles(self):
        for i in range(len(self.turtles) - 1):
            self.turtles[i].brain.mutate()
    
    # Gets the index of the turtle with the highest fitness
    # and sets the minimum steps to the number of steps to what the best turtle took
    def get_best_turtle_index(self):
        best_fitness = 0
        best_turtle_index = -1
        for i in range(len(self.turtles)):
            turtle_fitness = self.turtles[i].get_fitness()
            if turtle_fitness > best_fitness:
                best_turtle_index = i
                best_fitness = turtle_fitness
        if self.turtles[best_turtle_index].reached_goal:
            self.min_step = self.turtles[best_turtle_index].brain.step
        return best_turtle_index
    
    # Restarts the Genetic algorithm with the new location of the starting point or goal
    def restart(self, size, x, y):
        self.is_changing = True
        self.fitness_sum = 0
        self.gen = 1
        self.best_turtle = None
        self.original_x = x
        self.original_y = y
        self.min_step = size
        for t in self.turtles:
            t.replace_turtle(x, y, None)
        self.is_changing = False
        print("\nRestarted!")
        print(f"Generation {self.gen}")
