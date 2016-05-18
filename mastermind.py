import itertools
from copy import copy


class Mastermind(object):
    def __init__(self, secret, num_colours=6, num_pegs=4, duplicates=True):
        self.secret = secret
        self.possible_opts = itertools.product(range(num_colours), repeat=num_pegs)
        self.num_colours = num_colours
        self.guesses = []

    def make_guess(self, guess):
        response = self.secret.check(guess)
        self.guesses += [(guess, response)]
        return guess, response

    def pseudo(self, possibility):
        for guess, result in self.guesses:
            would_match = self.imagine(possibility, guess)
            if not (would_match == result):
                return False
        self.make_guess(possibility)


    def imagine(self, possibility, guess):
        return possibility == guess



class Secret(object):
    def __init__(self, secret):
        self.secret = secret

    def check(self, guess):
        secret_copy = copy(self.secret)
        zipped_positions = zip(self.secret, guess)
        black_pegs = 0
        for c, g in zipped_positions:
            if c == g:
                black_pegs += 1
        white_pegs = 0
        for peg in guess:
            if peg in secret_copy:
                white_pegs += 1
                secret_copy.remove(peg)
        return black_pegs, white_pegs - black_pegs



s = Secret([0, 1, 2, 3])
m = Mastermind(s)
m.make_guess([0,0,1,1])
m.make_guess([0,0,1,2])

print(m.guesses)

# for guess in m.possible_opts:
#     result = s.check(guess)
#     print(guess, result, result==(4, 0))

# if __name__ == '__main__':
#     import timeit
#     print('Hi')
#     print(timeit.timeit("checker1([0,1,2,3],[0,0,1,2])", setup="from __main__ import checker1"))
#     print(timeit.timeit("checker2([0,1,2,3],[0,0,1,2])", setup="from __main__ import checker2"))