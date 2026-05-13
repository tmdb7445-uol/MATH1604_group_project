"""
data_analysis_M3.py
-------------------
This module is to analyse the collated quiz answers from my Team Member 2.
Mainly, it has 2 functions;
  1. generate_means_sequence: this function will calculate the mean of each question of 100 questions
  2. visualize_data : this function function will plot the data as a graph.
  
Author: Ahmad Nidhal Bin ZAIDI
Module: MATH1604 Modelling for Big Data
"""

import matplotlib.pyplot as plt

def _parse_collated_file(collated_answers_path):
    """
    The collated answers file will be read and it will return eveyone's answer as a list.
    
    Read a collated answers file and return a list of answer sequences.

    The collated file contains one respondent's answers per line (100
    space-separated integers: 1–4, or 0 for unanswered). Respondents
    are separated by a line containing a single asterisk '*'.

    Parameters
    ----------
    collated_answers_path : str
        Path to the collated_answers.txt file produced by Team Member 2.

    Returns
    -------
    list of list of int
        A list where each element is a list of 100 integers representing
        one respondent's answer sequence.

    Raises
    ------
    FileNotFoundError
        If the file at collated_answers_path does not exist.
    ValueError
        If a data line does not contain exactly 100 integers.
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
    Compute the mean answer value for each of the 100 quiz questions.

    For every question position (1 to 100), this function collects all
    respondents' answers from the collated file and calculates the
    arithmetic mean, excluding any unanswered entries (represented by 0).

    Parameters
    ----------
    collated_answers_path : str
        Path to the collated_answers.txt file produced by Team Member 2.
        Each non-separator line must contain exactly 100 space-separated
        integers (values 1–4 for an answer, 0 for unanswered).

    Returns
    -------
    list of float
        A list of 100 floats. Each float is the mean answer value for
        that question across all respondents (zeros excluded).
        If every respondent left a question unanswered, the mean for
        that question is recorded as 0.0.

    Raises
    ------
    FileNotFoundError
        If the file at collated_answers_path does not exist.
    ValueError
        If any data line does not contain exactly 100 integers.

    Examples
    --------
    >>> means = generate_means_sequence("output/collated_answers.txt")
    >>> print(means[:5])   # first five question means
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
    Visualise answer data from the collated answers file.

    Depending on the value of n, one of two plots is produced:

    - n = 1 : Scatter plot of the mean answer value for each question
              (question number on the x-axis, mean value on the y-axis).
    - n = 2 : Line plot showing every individual respondent's answer
              sequence as a separate line, all overlaid on the same axes
              (question number 1–100 on the x-axis, answer value 1–4
              on the y-axis).

    If n is neither 1 nor 2, an error message is printed and no plot
    is produced.

    Parameters
    ----------
    collated_answers_path : str
        Path to the collated_answers.txt file produced by Team Member 2.
    n : int
        Plot type selector.
        1 → scatter plot of means.
        2 → line plot of all individual respondent sequences.

    Returns
    -------
    None
        Displays the plot using matplotlib and does not return a value.

    Raises
    ------
    FileNotFoundError
        If the file at collated_answers_path does not exist.
    ValueError
        If any data line does not contain exactly 100 integers.

    Examples
    --------
    >>> visualize_data("output/collated_answers.txt", 1)
    # Shows a scatter plot of mean answers per question

    >>> visualize_data("output/collated_answers.txt", 2)
    # Shows overlapping line plots for every respondent

    >>> visualize_data("output/collated_answers.txt", 5)
    Error: n must be 1 (scatter plot) or 2 (line plot). Got: 5
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
