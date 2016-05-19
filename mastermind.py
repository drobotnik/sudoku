from itertools import product, permutations
from copy import copy


def pprint(iterable):
    for _ in iterable:
        print(_)


def check(secret, guess):
    # TODO get rid of this turning a copy into a list
    secret_copy = list(copy(secret))
    zipped_positions = zip(secret, guess)
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


class Mastermind(object):
    def __init__(self, secret, num_colours=6, num_pegs=4, strategy=0, duplicates=True):
        if not duplicates:
            assert num_pegs <= num_colours
        self.strategy = strategy
        self.secret = secret
        self.possible_opts = product(range(num_colours), repeat=num_pegs) if duplicates else permutations(range(num_colours), num_pegs)
        self.num_colours = num_colours
        self.guesses = []
        self.num_pegs = num_pegs

    def make_guess(self, guess):
        response = self.secret.give_guess_response(guess)
        self.guesses += [(guess, response)]
        # print('Making guess: {}, Response: {}'.format(guess, response))
        return guess, response

    def test_possibility(self, possibility):
        for wrong_guess, wrong_result in self.guesses:
            hypothetical_result = check(possibility, wrong_guess)
            # print('old guess: {}, res:{}, poss: {}, hypo:{}'.format(wrong_guess, wrong_result, possibility, hypothetical_result))
            if hypothetical_result != wrong_result:
                return False
        return True

    def get_next_guess(self):
        if self.strategy == 0:
            return next(self.possible_opts)
        else:
            raise Exception("Didn't enter a valid strategy")

    def run(self):
        starting_guess = [int(x >= self.num_pegs / 2) for x in range(self.num_pegs)]
        self.make_guess(starting_guess)
        while True:
            option = self.get_next_guess()
            if self.test_possibility(option):
                _, response = self.make_guess(option)
                if response == (self.num_pegs, 0):
                    return option




class Secret(object):
    def __init__(self, secret):
        self.secret = secret

    def give_guess_response(self, guess):
        return check(self.secret, guess)




strategies = {
    'naive': 0
}


def single_test(code):
    s = Secret(code)
    m = Mastermind(s)
    print(m.run())
    print(len(m.guesses))
    pprint(m.guesses)


def test_all_combinations(colours=6, pegs=4, duplicates=True):
    dist = {}
    all_secrets = product(range(colours), repeat=pegs) if duplicates else permutations(range(colours), pegs)
    for test_secret in all_secrets:
        # print(test_secret)
        s = Secret(test_secret)
        m = Mastermind(s, colours, pegs, 0, duplicates)
        m.run()
        num_guesses = len(m.guesses)
        if num_guesses in dist:
            dist[num_guesses] += 1
        else:
            dist[num_guesses] = 1

    for guess_count, num in dist.items():
        print(guess_count, num)

    return dist


test_all_combinations(duplicates=True)
