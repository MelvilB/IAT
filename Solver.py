from Jeu import Jeu
import random
import matplotlib.pyplot as plt
import numpy as np
import math

def random_guess(number = 1):
    tab = []
    for i in range(number):
        while True:
            r = [random.randint(1, 8) for i in range(4)]
            if not (r in tab):
                tab.append(r)
                break
    return tab

def play_multiple_guess(game, guesses):
    res = []
    for g in guesses:
        res.append(game.jouer(g))
    return res

def solution_index(results):
    i = 0
    for r in results:
        if r == (4, 0):
            return i
        i+=1
    return -1

def sort_by_fitness(game, guesses):
    t = []
    for g in guesses:
        t.append([game.fitness(g), g])
    s = sorted(t, key=lambda l:l[0], reverse = False)
    sg = []
    for g in s:
        sg.append(g[1])
    return sg

def selection_tournament(game, pop, k=2):
	# first random selection
    index = [random.randint(0, len(pop)-1) for _ in range(k-1)]
    selection_ix = random.randint(0, len(pop)-1)
    for ix in index:
    # check if better (e.g. perform a tournament)
        if game.fitness(pop[ix]) < game.fitness(pop[selection_ix]):
            selection_ix = ix
    return pop.pop(selection_ix)



def get_min_fitness_guess(game, guesses):
    min_fitness = -1
    min = guesses[0]
    for g in guesses:
        fitness = game.fitness(g)
        if min_fitness == -1 or fitness < min_fitness:
            min_fitness = game.fitness(g)
            min = g
    return min

def mutate_guesses(guesses, prob):
    for i in range(len(guesses)):
        for j in range(len(guesses[0])):
            if random.random() < prob:
                guesses[i][j] = random.randint(1, 8)


def crossover_guesses(guess1, guess2, prob):
	# children are copies of parents by default
	c1, c2 = guess1.copy(), guess2.copy()
	# check for recombination
	if random.random() < prob:
		# select crossover point that is not on the end of the string
		pt = random.randint(1, len(guess1)-2)
		# perform crossover
		c1 = guess1[:pt] + guess2[pt:]
		c2 = guess2[:pt] + guess1[pt:]
	return [c1, c2]

def procreate(guesses, crossover_prob, mutation_prob):
    next_gen = []
    while len(guesses) >1:
        parent1 = random.choice(guesses)
        guesses.remove(parent1)
        parent2 = random.choice(guesses)
        guesses.remove(parent2)
        childs =  crossover_guesses(parent1, parent2, crossover_prob)
        mutate_guesses(childs, mutation_prob)
        next_gen.append(childs[0])
        next_gen.append(childs[1])
    if len(guesses) == 1:
        next_gen.append(guesses[0])
    return next_gen

def select_best_geneticly(game, max_iter = 20, initial_pop = 100, selected_pop=60, min_fitness = 0.5, fitness_incr_step = 5, crossover_prob=0.5, mutation_prob=0.03):
    
    while True:
        for _ in range(fitness_incr_step):
            best = None
            guesses = random_guess(number = initial_pop)
            for i in range(max_iter):
                #guesses = sort_by_fitness(game, guesses)
                #guesses = guesses[:selected_pop]
                best = get_min_fitness_guess(game, guesses)
                guesses = [selection_tournament(game, guesses) for _ in range(selected_pop)]
                guesses.append(best)
                guesses = procreate(guesses, crossover_prob, mutation_prob)
                best = get_min_fitness_guess(game, guesses)
                if game.fitness(best) <= min_fitness:
                    return best
        min_fitness += 1

def play_game(max_iter = 20, initial_pop = 80, selected_pop=25, min_fitness = 12, crossover_prob=0.5, mutation_prob=0.03):
    game = Jeu()
    init_guess = [1,2,3,4]
    result = game.jouer(init_guess, display=True)  
    while result != (4, 0):
        result=game.jouer(select_best_geneticly(game), display=True)
    return game.try_counter


if __name__ == '__main__':
    tries = []
    for i in range(500):
        tries.append(play_game())
    print("Moyenne : ",np.mean(tries))
    plt.hist(tries, bins=20)
    plt.show()
