#!/usr/bin/env python
import sys
import warnings

from prompt_solution_crew.crew import PromptSolutionCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run(inputs):
    """
    Run the crew with the provided inputs.
    """
    inputs = {
        'user_setup': 'AI Agents'
    }
    
    return PromptSolutionCrew().crew().kickoff(inputs=inputs)

def train(inputs, n_iterations, filename):
    """
    Train the crew for a given number of iterations.
    """
    try:
        return PromptSolutionCrew().crew().train(n_iterations=n_iterations, filename=filename, inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay(task_id):
    """
    Replay the crew execution from a specific task.
    """
    try:
        return PromptSolutionCrew().crew().replay(task_id=task_id)
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test(inputs, n_iterations, openai_model_name):
    """
    Test the crew execution and returns the results.
    """
    try:
        return PromptSolutionCrew().crew().test(n_iterations=n_iterations, openai_model_name=openai_model_name, inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
