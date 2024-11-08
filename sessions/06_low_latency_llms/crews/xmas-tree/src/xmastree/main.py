#!/usr/bin/env python
import sys
from xmastree.crew import TalkersCrew

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

# declare inputs here
def_inputs = {
    'topic': 'ASCII Art Christmas Tree',
    'code_task': 'Create a python function that generates an ASCII art of a Christmas tree'
}

def run():
    """
    Run the crew.
    """
    TalkersCrew().crew().kickoff(inputs=def_inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    try:
        TalkersCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=def_inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        TalkersCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    try:
        TalkersCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=def_inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
