# Genetic algorithm based on Code Bullet's video: tinyurl.com/ycexp53g

import os
import sys
import turtle
import gc

from population import Population
from multiprocessing import Process
from audioPlayer import WavePlayer
from startingPoint import StartingPoint


# Gets file relative runner.py's directory
def get_file(relative_file_path):
    return os.path.join(os.path.dirname(__file__), relative_file_path)


# Sets up the turtle screen
turtle.Screen().setup(width=600, height=600)
turtle.Screen().tracer(0, 0)

# Sets GC threshold to 1000 times its usual to stop gc-induced lag
gc.set_threshold(*[1000 * threshold for threshold in gc.get_threshold()])

# The starting location of the EvolvingTurtles
start = (0, -250)

# Sets up a population of EvolvingTurtles
group = Population(200, *start)

# Sets up and plays the main game audio
main = WavePlayer(get_file('../audio/gameMusic.wav'), True)
main.play()

# Sets up the audio played upon each new generation
new_gen = WavePlayer(get_file('../audio/pop.wav'), False)

# Creates the starting point with the given location and gives it a reference to the population
starting_point = StartingPoint(*start)
starting_point.set_population(group)

# Gives the population a reference to the starting point
group.set_start(starting_point)


# Main loop method (made into method so program could be stopped without force-quitting)
def run_loop():
    screen = turtle.Screen()
    new_gen.play()
    while True:
        # Moves all Turtles
        if group.setup_done:
            group.move()
            if screen.window_height() != 600 or screen.window_width() != 600:
                screen.setup(width=600, height=600)
            
            # If the group is all dead, the next generation is prepared
            if group.all_dead():
                group.calculate_fitness()
                group.natural_selection()
                group.mutate_turtles()
                new_gen.play()
        turtle.Screen().update()


# Forcefully closes the application
def exit_code():
    try:
        sys.exit(0)
    except SystemExit:
        # noinspection PyProtectedMember
        os._exit(0)


# The main process to be run, closes if exception thrown
main_process = Process(target=run_loop)

# noinspection PyBroadException
# Runs the main process until the application is closed
try:
    main_process.run()
except Exception:
    exit_code()
except KeyboardInterrupt:
    exit_code()
