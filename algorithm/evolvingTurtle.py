import math

from turtle import Turtle
from brain import Brain


# Class that represent the evolving turtles in the generation
class EvolvingTurtle(Turtle):
    
    # Initializes the EvolvingTurtle
    def __init__(self, x, y, population, directions=None):
        # Initializes turtle (The color #324F17 is the EvolvingTurtle's green color)
        Turtle.__init__(self, shape="square", visible=False)
        self.color("black", "#608341")
        self.penup()
        self.goto(x, y)
        
        # A turtle is dead if it is finished with the number of steps it can do or it touches a wall
        self.dead = False
        
        # False until it gets to the coordinates of the goal
        self.reached_goal = False
        
        # Creates velocity and acceleration vectors
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        
        # Creates EvolvingTurtle's brain
        self.brain = Brain(400)
        
        # If the EvolvingTurtle is given directions, the typical brain directions will be replaced
        if directions is not None:
            self.brain.directions = directions
        
        # Sets speed to max
        self.speed(0)
        
        # The evolving turtle's fitness (ability to survive)
        self.fitness = 0
        
        # The distance the evolving turtle is to the goal by death (starts at 500)
        self.distance_to_goal = 500
        
        # Sets the population to the given population reference
        self.population = population
        
        # Shows the EvolvingTurtle
        self.showturtle()
    
    # Moves the EvolvingTurtle according to the directions given by the brain
    def move(self):
        # Gets distance between goal and EvolvingTurtle
        cors = self.population.get_goal_cors()
        self.distance_to_goal = math.hypot(cors[0] - self.xcor(), cors[1] - self.ycor())
        
        if not self.dead and not self.reached_goal:
            # If the directions aren't up, get the next acceleration direction and go to the next step
            if len(self.brain.directions) > self.brain.step:
                direction = self.brain.directions[self.brain.step]
                self.acceleration = [math.cos(direction), math.sin(direction)]
                self.brain.step += 1
            # If the brain's steps are done, the EvolvingTurtle is unable to move
            else:
                self.die()
            
            # Increases velocity by acceleration
            self.velocity[0] += self.acceleration[0]
            self.velocity[1] += self.acceleration[1]
            
            # If the magnitude of the velocity is greater than five, keep the same direction.
            # However, decrease the magnitude to five
            magnitude = math.hypot(self.velocity[0], self.velocity[1])
            if magnitude > 5:
                self.velocity = [val * 5 / magnitude for val in self.velocity]
            
            # Sets the position to the position plus the velocity after checking whether it is in bounds.
            # If it isn't in bounds, it is dead.
            x = self.xcor() + self.velocity[0]
            y = self.ycor() + self.velocity[1]
            if 300 - 21 < x:
                x = 300 - 21
                self.die()
            if x < -300 + 12:
                x = -300 + 12
                self.die()
            if 300 - 12 < y:
                y = 300 - 12
                self.die()
            if y < -300 + 21:
                y = -300 + 21
                self.die()
            self.goto(x, y)
        
        # If the goal has been reached, the reached_goal var is set to true, and the turtle is turned blue
        if self.distance_to_goal < 5:
            self.reached_goal = True
            self.color('black', 'blue')
    
    # Returns true if the EvolvingTurtle should be able to move
    def not_dead(self):
        return not self.dead
    
    # Returns true if the EvolvingTurtle has reached the goal
    def at_goal(self):
        return self.reached_goal
    
    # Sets dead to true and changes color of turtle from green to red
    def die(self):
        self.dead = True
        self.color("black", "red")
    
    # Calculates the fitness value of the EvolvingTurtle
    def calculate_fitness(self):
        if self.reached_goal:
            self.fitness = 1 / 16 + 1000 / (self.brain.step * 2)
        else:
            self.fitness = 1 / self.distance_to_goal ** 2
    
    # Returns the fitness of the EvolvingTurtle
    def get_fitness(self):
        return self.fitness
    
    # Sets up current turtle with new values to save memory
    def replace_turtle(self, x, y, directions):
        self.hideturtle()
        self.color("black", "#608341")
        self.goto(x, y)
        self.dead = False
        self.reached_goal = False
        self.velocity = [0, 0]
        if directions is not None:
            self.brain.replace(directions)
        else:
            self.brain = Brain(400)
        self.showturtle()
