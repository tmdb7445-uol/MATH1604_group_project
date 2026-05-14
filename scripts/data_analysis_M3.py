"""
data_analysis_M3.py
-------------------
This module is to analyse the collated quiz answers from my Team Member 2.
Mainly, it has 2 functions;
  1. generate_means_sequence: this function will calculate the mean of each question of 100 questions
  2. visualize_data : this function will plot the data as a graph.
  
Author: Ahmad Nidhal Bin ZAIDI
Module: MATH1604 Modelling for Big Data
"""

import matplotlib.pyplot as plt

def _parse_collated_file(collated_answers_path):
    """
    The collated answers file will be read and
    it will return eveyone's answer as a list.
    
    Each line of 100 integers is representing a 
    list of a student answer in a 100 questions set.
    
    The answer for each students will be represented as 
    numbers from 1 - 4, and 0 for unanswered questions.
    
    Also, the repondents liss of 100 integers are separated by the asterisk symbol "*" 
    so that it can be easily differentiate.

    Parameters
    ----------
    collated_answers_path : str
      This is the file path to connect to the big 'collated_answer.txt' 
      file that my Team Member 2 has created.

    Returns
    -------
    list of list of int
        A list where each element is a list of 100 integers representing
        one respondent's answer sequence.

    Raises
    ------
    FileNotFoundError
      This triggers if the collated_answer_path file is not found.
    ValueError
        A safety precaution to ensure every single line has exactly 100 numbers.
    """
    all_sequences = []

    with open(collated_answers_path, "r") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()

            if line == "*" or line == "":
                continue

            tokens = line.split()

            if len(tokens) != 100:
                raise ValueError(
                    f"Line {line_number} has {len(tokens)} values, "
                    f"but 100 were expected."
                )

            answers = [int(token) for token in tokens]
            all_sequences.append(answers)

    return all_sequences

def generate_means_sequence(collated_answers_path):
    """
    The average answer of every single one of the 100 questions set 
    by all students will be calculated.

    From question 1-100, it will gather up everyone's answer. Then, we
    filter out any 0]s first because it means that student skipped those
    questions. Once the 0's are gone, the arithmetic means will be figured.

    Parameters
    ----------
    collated_answers_path : str
        The file path to the main text file where all the data of students'
        answers are stored together.
        
    Returns
    -------
    list of float
        The output will be a list of 100 float.
        Each number should be ranging between 0.0 and 4.0.
        If there is any chance everyone skips the question, it will just be 0.0.

    Raises
    ------
    FileNotFoundError
        It will triggers if the path I gave before does not exist.
    ValueError
        It will trigger is there any student's line which does not have 100 numbers.

    Examples
    --------
    >>> means = generate_means_sequence("output/collated_answers.txt")
    >>> print(means[:5])   # which indicates first five question means
    [2.3, 1.8, 3.1, 2.7, 1.5]
    """
    all_sequences = _parse_collated_file(collated_answers_path)

    means = []

    for question_index in range(100):
        valid_answers = [
            seq[question_index]
            for seq in all_sequences
            if seq[question_index] != 0
        ]

        if len(valid_answers) == 0:
            means.append(0.0)
        else:
            mean_value = sum(valid_answers) / len(valid_answers)
            means.append(mean_value)

    return means

def visualize_data(collated_answers_path, n):
    """
    The answer data will be plotted in 2 different ways to find the quiz master
    hidden pattern;

    Depending on the value of n, one of two plots is produced:

    - n = 1 : Scatter plot of the mean answer value for each question
              (question number on the x-axis, mean value on the y-axis).
    - n = 2 : Line plot showing every individual respondent's answer
              sequence as a separate line, all overlaid on the same axes
              (question number 1–100 on the x-axis, answer value 1–4
              on the y-axis).

    If the n value is neither 1 nor 2, an error message will appeared and 
    no plot will be produced
    
    Parameters
    ----------
    collated_answers_path : str
        The file path to the main text file where all the data of students'
        answers are stored together
        
    n : int
        This is the type of plot selector
        1 is for scatter plot of means of each questions.
        2 is for a line plot of all individual respondent sequences.

    Returns
    -------
    None
        This functions will only displays the output graph and
        will not sreturn any values.

    Raises
    ------
    FileNotFoundError
        It will triggers if the path I gave before does not exist.
    ValueError
        It will trigger is there any student's line which does not have 100 numbers.

    Examples
    --------
    >>> visualize_data("output/collated_answers.txt", 1)
    # this will create a scatter plot of means for each question from 1 - 100

    >>> visualize_data("output/collated_answers.txt", 2)
    # This will produce line plots for every respondents

    >>> visualize_data("output/collated_answers.txt", 5)
    # it will produce an error because n must be 1 (scatter plot) or 2 (line plot).
    """

    if n not in (1, 2):
        print(f"Error: n must be 1 (scatter plot) or 2 (line plot). Got: {n}")
        return   

    all_sequences = _parse_collated_file(collated_answers_path)

    question_numbers = list(range(1, 101))

    if n == 1:
        means = generate_means_sequence(collated_answers_path)

        plt.figure(figsize=(14, 5))
        plt.scatter(question_numbers, means, color="steelblue", s=30)

        plt.title("Mean Answer Value per Question (Scatter Plot)")
        plt.xlabel("Question Number")
        plt.ylabel("Mean Answer Value")
        plt.xticks(range(1, 101, 5))
        plt.yticks([1, 1.5, 2, 2.5, 3, 3.5, 4])
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()

    elif n == 2:
        plt.figure(figsize=(14, 5))

        for respondent_index, answers in enumerate(all_sequences):
            plt.plot(
                question_numbers,
                answers,
                alpha=0.3,
                linewidth=0.8,
                label=f"Respondent {respondent_index + 1}"
            )

        plt.title("Individual Answer Sequences (Line Plot, All Respondents)")
        plt.xlabel("Question Number")
        plt.ylabel("Answer Value (1–4, 0 = unanswered)")
        plt.xticks(range(1, 101, 5))
        plt.yticks([0, 1, 2, 3, 4])
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()
