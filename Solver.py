from Jeu import Jeu
import random
import matplotlib.pyplot as plt
import numpy as np
import math

def random_guess(number = 1):
    '''
    Renvoie n=number combinaisons de jeux DIFFERENTES, dans un tableau
    '''
    tab = []
    for i in range(number):
        while True:
            r = [random.randint(1, 8) for i in range(4)]
            if not (r in tab):
                tab.append(r)
                break
    return tab


def selection_tournament(game, pop, k=2):
    '''
        Effectue un tournoi de taille k, on fait s'affronter k combinaisons, celle avec le meilleur fitness est retournée
    '''
    index = [random.randint(0, len(pop)-1) for _ in range(k-1)]
    selection_index = random.randint(0, len(pop)-1)
    for ix in index:
        if game.fitness(pop[ix]) < game.fitness(pop[selection_index]):
            selection_index = ix
    return pop[selection_index]



def get_min_fitness_guess(game, guesses):
    '''
        Renvoie le coup à jouer avec la fitness minimale, parmis les 'guesses' et sur le jeu 'game'
    '''
    min_fitness = -1
    min = guesses[0]
    for g in guesses:
        fitness = game.fitness(g)
        if min_fitness == -1 or fitness < min_fitness:
            min_fitness = game.fitness(g)
            min = g
    return min

def mutate_guesses(guesses, prob):
    '''
        Parcours chaque gène de chaque guesses contenu dans "guesses" et le modifie avec une probabilité=prob
    '''
    for i in range(len(guesses)):
        for j in range(len(guesses[0])):
            if random.random() < prob:
                guesses[i][j] = random.randint(1, 8)


def crossover_guesses(guess1, guess2, prob):
    '''
        Effectue un crossover (i.e. couper ou non des parents à un point donner et les recombiner pour former un enfant) entre deux guesses
        Renvoie les deux guesses résultants, le crossover a lieu à un endroit aléatoire (et il a lieu avec une proba=prob)
    '''
    c1, c2 = guess1.copy(), guess2.copy()
    if random.random() < prob:
        pt = random.randint(1, len(guess1)-2)
        c1 = guess1[:pt] + guess2[pt:]
        c2 = guess2[:pt] + guess1[pt:]
    return [c1, c2]

def procreate(guesses, crossover_prob, mutation_prob):
    '''
        Fonction gérant la procréation : prend en entrée une population et retourne la générération suivante.
        Procède aux croisements par crossover et aux mutations.
    '''
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

def select_best_geneticly(game, max_iter = 20, initial_pop = 200, selected_pop=60, min_fitness = 0, fitness_incr_step = 5, crossover_prob=0.5, mutation_prob=0.03):
    '''
        Propose le meilleur coup à jouer pour un jeu donné en se basant sur un algo génétique.
    '''
    while True: #boucle tant qu'on a pas trouvé de coup à jouer
        for _ in range(fitness_incr_step): #On tente d'atteindre une fitness = 0 un certain nombre de fois, puis une fitness = 1, etc
            best = None
            guesses = random_guess(number = initial_pop) #Tirage aléatoire de combinaisons différents
            for i in range(max_iter): #On joue au maximum max_iter générations
                selected = [selection_tournament(game, guesses) for _ in range(selected_pop)]
                childs = procreate(selected, crossover_prob, mutation_prob)
                best = get_min_fitness_guess(game, childs)
                if game.fitness(best) <= min_fitness:
                    return best
                
                guesses = childs
        min_fitness += 1 

def play_game(display=False, selected_pop = 60):
    game = Jeu()
    init_guess = [1,2,3,4]
    result = game.jouer(init_guess, display=display)  
    while result != (4, 0):
        result=game.jouer(select_best_geneticly(game, selected_pop=selected_pop), display=display)
    return game.try_counter


if __name__ == '__main__':
    tries = []
    for i in range(500):
        tries.append(play_game(display= False, selected_pop = 60))
    m = np.mean(tries)
    print("Moyenne : ", m )
