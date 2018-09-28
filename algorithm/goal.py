import math
import turtle


# Class that represents the goal the EvolvingTurtles are reaching for
class Goal:
    
    # Initializes goal
    def __init__(self, x, y):
        self.start = None
        self.population = None
        self.goal = turtle.Turtle(shape="circle", visible=False)
        self.goal.penup()
        self.goal.speed(0)
        self.goal.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.goal.goto(x, y)
        self.goal.showturtle()
        self.goal.ondrag(self.dragging)
        self.goal.onrelease(self.releasing)
        self.drag_x = 0
        self.drag_y = 0
        self.temp_x = self.goal.xcor()
        self.temp_y = self.goal.ycor()
        
    # Sets start to given start reference
    def set_start(self, start):
        self.start = start
        
    # Sets population to given population reference
    def set_population(self, population):
        self.population = population
    
    # Returns goal coordinates
    def get_goal(self):
        return self.temp_x, self.temp_y

    # Method called upon goal being dragged
    def dragging(self, x, y):
        # Prevents dragging from being called (until dragging is done)
        self.goal.ondrag(None)
        
        # Constrains goal to box made from 30 pixels inwards from screen boundaries
        distance_from_edge = 30
        if 300 - 16 - distance_from_edge < x:
            x = 300 - 16 - distance_from_edge
        if x < -300 + 7 + distance_from_edge:
            x = -300 + 7 + distance_from_edge
        if 300 - 7 - distance_from_edge < y:
            y = 300 - 7 - distance_from_edge
        if y < -300 + 16 + distance_from_edge:
            y = -300 + 16 + distance_from_edge
            
        # The goal is only moved to 50 pixels or greater from start point
        goal_cors = self.start.get_start()
        if not math.hypot(goal_cors[0] - x, goal_cors[1] - y) < 50:
            self.goal.goto(x, y)
            self.drag_x = x
            self.drag_y = y
            
        # Re-adds function to goal dragging so it can be called again
        self.goal.ondrag(self.dragging)

    # Method called upon goal being released
    # noinspection PyUnusedLocal
    def releasing(self, x, y):
        # Prevents releasing from being called (until releasing is done)
        self.goal.onrelease(None)
        
        # Restarts the population if the population has a reference and updates goal coordinates
        if self.population is not None:
            self.population.restart(self.population.size, self.population.original_x, self.population.original_y)
            self.temp_x = self.drag_x
            self.temp_y = self.drag_y

        # Re-adds function to goal releasing so it can be called again
        self.goal.onrelease(self.releasing)
