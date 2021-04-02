import math
import os
import random


def main():
    target = [random.randint(1, 8) for i in range(4)]
    previous_guesses = []
    found = False
    while not found:
        current_guess = get_guess(previous_guesses)
        if current_guess == target:
            found = True
        previous_guesses.append([current_guess, score(compare(target, current_guess))])


def get_guess(previous_guesses):

    # (ALGO GENETIQUE )

    best_candidate = [1, 1, 1, 1]
    return best_candidate


def compare(target, current_guess):
    p = m = i = 0
    for value in current_guess:
        match = False
        if value == target[i]:
            p += 1
            match = True
        i += 1
        for target_value in target:
            if target_value == value and not match:
                m += 1
                break
    return(p, m)


def score(pm):
    return (2*pm[0]+pm[1])


def evaluation(current_guess, previous_guess):
    return (abs(previous_guess[1]-score(compare(previous_guess[0], current_guess))))


def fitness(current_guess, previous_guesses):
    fit = 0
    for previous_guess in previous_guesses:
        fit += evaluation(current_guess, previous_guess)
    return (fit)


if __name__ == "__main__":
    main()
