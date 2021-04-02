import random


class Jeu:

    def __init__(self):
        self.target = [random.randint(1, 8) for i in range(4)]
        self.previous_guesses = [] #[[candidats], [scores]]

    def jouer(self, guess, display=False):
        self.previous_guesses.append([guess, self.score(self.compare(self.target, guess))])
        if display:
            self.display_game()
        return self.compare(self.target, guess)

    def score(self, pm):
        return (3*pm[0]+pm[1])

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
        return (abs(previous_guess[1]-self.score(self.compare(previous_guess[0], current_guess))))

    def fitness(self, current_guess):
        fit = 0
        for previous_guess in self.previous_guesses:
            fit += self.evaluation(current_guess, previous_guess)
        return fit

    def display_game(self):
        print('T : {}'.format(self.target))
        print('--------------')
        i = 1
        for guess in self.previous_guesses:
            (p, m) = self.compare(self.target, guess[0])
            print('{} : {}, p={} m={}, score={}, fitness last move={}'.format(i, guess[0], p, m, guess[1], self.fitness(guess[0])))
            i +=1
