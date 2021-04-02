from Jeu import Jeu


if __name__ == '__main__':
    jeu = Jeu()
    result = (0, 0)
    while result != (4, 0):
        guess = [0, 0, 0, 0]
        for i in range(4):
            print('case', i+1, '?')
            guess[i] = int(input())
        result = jeu.jouer(guess, display=True)
