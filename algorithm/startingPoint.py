import math
import turtle


# Class that represents the start the EvolvingTurtles begin at
class StartingPoint:
    
    # Initializes starting point of EvolvingTurtles
    def __init__(self, x, y):
        self.population = None
        self.goal = None
        self.start = turtle.Turtle(shape="circle", visible=False)
        self.start.color("black", "#FF9B00")
        self.start.penup()
        self.start.speed(0)
        self.start.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.start.goto(x, y)
        self.start.ondrag(self.dragging)
        self.start.onrelease(self.releasing)
        self.start.showturtle()
        self.drag_x = 0
        self.drag_y = 0
    
    # Sets the population to the given reference
    def set_population(self, population):
        self.population = population
    
    # Sets the goal to the given reference
    def set_goal(self, goal):
        self.goal = goal
    
    # Returns start coordinates
    def get_start(self):
        return self.start.xcor(), self.start.ycor()
    
    # Method called upon goal being dragged
    def dragging(self, x, y):
        # Prevents dragging from being called (until dragging is done)
        self.start.ondrag(None)
        
        # Constrains start to box made from 30 pixels inwards from screen boundaries
        distance_from_edge = 30
        if 300 - 16 - distance_from_edge < x:
            x = 300 - 16 - distance_from_edge
        if x < -300 + 7 + distance_from_edge:
            x = -300 + 7 + distance_from_edge
        if 300 - 7 - distance_from_edge < y:
            y = 300 - 7 - distance_from_edge
        if y < -300 + 16 + distance_from_edge:
            y = -300 + 16 + distance_from_edge
        
        # The start is only moved to 50 pixels or greater from goal point
        goal_cors = self.goal.get_goal()
        if not math.hypot(goal_cors[0] - x, goal_cors[1] - y) < 50:
            self.start.goto(x, y)
            self.drag_x = x
            self.drag_y = y
        
        # Re-adds function to goal dragging so it can be called again
        self.start.ondrag(self.dragging)
    
    # Method called upon goal being released
    # noinspection PyUnusedLocal
    def releasing(self, x, y):
        # Prevents releasing from being called (until releasing is done)
        self.start.onrelease(None)
        
        # Restarts the population if the population has a reference
        if self.population is not None:
            self.population.restart(self.population.size, self.drag_x, self.drag_y)
        
        # Re-adds function to goal releasing so it can be called again
        self.start.onrelease(self.releasing)
