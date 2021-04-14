import random


class Jeu:

    def __init__(self):
        self.target = [random.randint(1, 8) for i in range(4)]
        self.previous_guesses = [] #[[candidats], [scores]]
        self.try_counter = 0

    def jouer(self, guess, display=False):
        (p, m) = self.compare(self.target, guess)
        self.try_counter += 1
        if display:
            print('{} : p={} m={}, score={}, fitness last move={}'.format(guess, p, m, self.score((p, m)), self.fitness(guess)))
            if (p, m) == (4, 0):
                print('Target {}, en {} essais'.format(self.target, self.try_counter))
        self.previous_guesses.append([guess, self.score((p, m))])
        return (p, m)

    def score(self, pm):
        return (10*pm[0]+5*pm[1])

    def compare(self, target, guess):
        p = m = i = 0
        for value in target: #pour chaque case
            match = False
            if value == guess[i]: #on a bonne pos + bonne couleur ?
                p += 1
                match = True
            if not match: #si non, on a cette couleur ailleurs ?
                for guess_value in guess:
                    if guess_value == value:
                        m += 1
                        break
            i += 1
        return(p, m)

    def evaluation(self, current_guess, previous_guess):
        #abs(score_vraie_solution-score(comp(target=prev_guess, guess= current_guess)))
        return (abs(previous_guess[1]-self.score(self.compare(current_guess, previous_guess[0]))))

    def fitness(self, current_guess):
        fit = 0
        for previous_guess in self.previous_guesses:
            fit += self.evaluation(current_guess, previous_guess)
        #fit += 2 * 4 * (len(self.previous_guesses)-1)
        return fit


