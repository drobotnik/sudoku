from itertools import product, permutations
from copy import copy
from collections import Counter

"""
https://arxiv.org/pdf/1305.1010.pdf
"""


def pprint(iterable):
    for _ in iterable:
        print(_)


def check(secret, guess):
    # TODO get rid of this turning a copy into a list
    # TODO look at using Counter() to replace this logic
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
    def __init__(self, secret, num_colours=6, num_pegs=4, strategy=1, duplicates=True):
        if not duplicates:
            assert num_pegs <= num_colours
        self.strategy = strategy
        self.secret = secret
        self.possible_opts = product(range(num_colours), repeat=num_pegs) if duplicates else permutations(range(num_colours), num_pegs)
        self.num_colours = num_colours
        self.num_pegs = num_pegs
        self.guesses = []
        if strategy == 1:
            self.remaining_opts = list(product(range(num_colours), repeat=num_pegs))
            self.possible_opts = list(product(range(num_colours), repeat=num_pegs))
            self.knuth_key = lambda test_guess: max(Counter(check(code, test_guess) for code in self.remaining_opts).values())

    def make_guess(self, guess):
        response = self.secret.give_guess_response(guess)
        self.guesses += [(guess, response)]
        print('Making guess: {}, Response: {}'.format(guess, response))
        return guess, response

    def test_possibility(self, possibility):
        for wrong_guess, wrong_result in self.guesses:
            hypothetical_result = check(possibility, wrong_guess)
            if hypothetical_result != wrong_result:
                return False
        return True

    def get_next_guess(self):
        if self.strategy == 0:
            next_guess = next(self.possible_opts)
            while not self.test_possibility(next_guess):
                next_guess = next(self.possible_opts)

        elif self.strategy == 1:
            last_guess, last_response = self.guesses[-1]
            filtered_codes = []  # c for c in codes if check(guess, c) == feedback]
            for c in self.remaining_opts:  # for each remaining possible code
                if check(c, last_guess) == last_response:  # Does that code match what we learnt from the last guess?
                    filtered_codes += [c]  # If so, add it to the list of remaining possible codes
            self.remaining_opts = filtered_codes  # Set codes to only be the remaining possibilities

            if len(self.remaining_opts) == 1:
                next_guess = self.remaining_opts[0]
            else:
                next_guess = min(self.possible_opts, key=self.knuth_key)  # Find the code which would give you the most unambiguous response in the worst case
        else:
            next_guess = next(self.possible_opts)

        return next_guess


    def run(self):
        chosen_guess = [int(x >= self.num_pegs / 2) for x in range(self.num_pegs)]
        option, response = self.make_guess(chosen_guess)
        while True:
            if response == (self.num_pegs, 0):
                return option
            chosen_guess = self.get_next_guess()
            option, response = self.make_guess(chosen_guess)


class Secret(object):
    def __init__(self, secret, num_colours=6, num_pegs=4, duplicates=True):
        assert max(secret) < num_colours, "Peg selected too high"
        assert min(secret) >= 0, "Peg selected below 0"
        assert len(secret) == num_pegs, "Not enough colours picked"
        if not duplicates:
            assert len(secret) == len(set(secret)), "There are duplicated numbers when duplicates are set to false"
        self.secret = secret

    def give_guess_response(self, guess):
        return check(self.secret, guess)


strategies = {
    'naive': 0,
    'knuth': 1,
    'brute_force': 2
}


def single_test(code, num_colours=6, num_pegs=4, strategy=0, duplicates=True):
    s = Secret(code, num_colours=num_colours, num_pegs=num_pegs, duplicates=duplicates)
    m = Mastermind(s, num_colours=num_colours, num_pegs=num_pegs, strategy=strategy, duplicates=duplicates)
    m.run()
    # pprint(m.guesses)
    print("Num Guesses: {}".format(len(m.guesses)))


single_test([5, 1, 0, 3], num_colours=6, num_pegs=4, strategy=2)


def test_all_combinations(colours=6, pegs=4, duplicates=True):
    all_secrets = product(range(colours), repeat=pegs) if duplicates else permutations(range(colours), pegs)
    guess_count = []
    for test_secret in all_secrets:
        s = Secret(test_secret)
        m = Mastermind(s, colours, pegs, 0, duplicates)
        m.run()
        num_guesses = len(m.guesses)
        guess_count += [num_guesses]

    dist = Counter(guess_count)
    # av = 0
    # for x, y in dist.items():
    #     av += x * y
    # av = av / sum(dist.values())
    # print('Average: {}'.format(av))

    return dist


# test_all_combinations(pegs=4, duplicates=True)


ALL_CODES = list(product(range(6), repeat=4))


def knuth(secret):
    """Run Knuth's 5-guess algorithm on the given secret."""
    assert(secret in ALL_CODES)
    codes = ALL_CODES  # Instantiate codes to be all possible codes
    key = lambda test_guess: max(Counter(check(code, test_guess) for code in codes).values())
    """
    Key explanation:
    For your test code
    check that to all the remaining possible secrets
    see how many of the same type of responses you would get for that code against all possible secrets.
    The higher the number, the worse it is as that will be more ambiguous.
    This is because it could be many different secrets which would give you that response from check() given that code.
    Find the highest value from these occurances (worst case).
    That is the score for that code.
    ie. If you got that response, how many different secrets would have given you that code
    """
    guess = (0, 0, 1, 1)
    guess_count = 0
    while True:
        feedback = check(secret, guess)
        guess_count += 1
        print("Guess {}: feedback {}".format(guess, feedback))
        if guess == secret:
            return guess_count

        filtered_codes = [] # c for c in codes if check(guess, c) == feedback]
        for c in codes:  # for each remaining possible code
            if check(c, guess) == feedback: # Does that code match what we learnt from the last guess?
                filtered_codes += [c]  # If so, add it to the list of remaining possible codes
        codes = filtered_codes  # Set codes to only be the remaining possibilities

        if len(codes) == 1:
            guess = codes[0]
        else:
            guess = min(ALL_CODES, key=key)  # Find the code which would give you the most unambiguous response in the worst case


# print(knuth((0, 0, 0, 0)))
#
# results = []
# for secret in product(range(6), repeat=4):
#     count = knuth(secret)
#     print(count)
#     results += [count]
#
# print(Counter(results))
