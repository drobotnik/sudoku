from copy import deepcopy, copy
from string import ascii_uppercase


def pprint(thing):
    for row in thing:
        print(row)


class Kakuro2(object):
    def __init__(self, info):
        self.size = info['size']
        self.number_range = list(str(num) for num in range(1, self.size + 1))
        self.letter_range = ascii_uppercase[:self.size]
        self.array = {}
        self.rules = {}
        for number in self.number_range:
            for letter in self.letter_range:
                self.array[letter + number] = ''.join((str(num) for num in self.number_range))
                self.rules[letter + number] = []
        self.add_rules(info['rules'])
        self.update_positions(info['positions'])

    def __str__(self):
        out = ''
        for letter in self.letter_range:
            for number in self.number_range:
                val = self.array[letter + number]
                out += val.ljust(self.size) + '|'
            out += '\n'
        return out

    def update_position(self, position, value):
        print('updating position: {}, val: {}, current ops: {}'.format(position, value, self.array[position]))
        # update row and col
        print('removing options')
        for cell in self.array:
            right_row = cell[0] == position[0]
            right_column = cell[1] == position[1]
            if right_row or right_column:
                self.remove_option(cell, value)
        # update position
        print('setting value of {} to be {}'.format(position, value))
        self.array[position] = value
        # update rules
        print('about to check rules for {}'.format(position))
        self.check_rules(position)
        print(self)

        return True

    def update_positions(self, info):
        for pos, val in info:
            print('**** Jeronimo MOFO! Update: {} ****'.format((pos, val)))
            self.update_position(pos, val)

    def remove_option(self, position, option):
        new_possibilities = ''
        current_possibilites = self.array[position]

        #print('removing options. Position {}, Option {}, current poss {}'.format(position, option, current_possibilites))
        for num in current_possibilites:
            if num != option:
                new_possibilities += num
        if (len(new_possibilities) == 1):
            self.update_position(position, new_possibilities)
        else:
            self.array[position] = new_possibilities

    def check_rules(self, position):
        print('check rules pos:{}, original poss:{}'.format(position, self.array[position]))
        rules = self.rules[position]
        print('rules for {}:'.format(position))
        for n, (relation, place) in enumerate(rules):
            current_options = self.array[place]
            comparison_value = self.array[position]
            print('rule {} - pos:{}, comp:{}, rel:{}, place:{}'.format(n, position, comparison_value, relation, place))

            if relation == '<':
                filter_func = lambda x: comparison_value < x
            elif relation == '>':
                filter_func = lambda x: comparison_value > x
            else:
                continue
            new_opts = filter(filter_func, current_options)
            new_opts_string = ''.join(new_opts)
            if (len(new_opts_string) == 1) and (len(current_options) != 1):
                self.update_position(place, new_opts_string)
            elif not len(new_opts_string):
                raise Exception('No valid values found for {}'.format(place))
            else:
                self.array[place] = new_opts_string
        return True

    def add_rule(self, rule):
        greater_than = '>'
        less_than = '<'
        if type(rule) == list:
            a, comp, b = rule
            if comp == greater_than:
                self.rules[a] += [[greater_than, b]]
                self.rules[b] += [[less_than, a]]
            else:
                self.rules[a] += [[less_than, b]]
                self.rules[b] += [[greater_than, a]]
        else:
            rule = [rule[:2], rule[2], rule[3:]]
            self.add_rule(rule)

    def add_rules(self, rules_list):
        for rule in rules_list:
            self.add_rule(rule)


class Kakuro(object):
    def __init__(self, info):
        self.size = info['size']
        self.array = [['' for x in range(self.size)] for y in range(self.size)]
        self.rules = {y: {x: [] for x in range(info['size'])} for y in range(info['size'])}
        self.add_rules(info['rules'])
        for position in info['positions']:
            self.update_position(*position)
        self.number_range = range(1, self.size + 1)

    def __str__(self):
        out = ''
        for _ in self.array:
            out += str(_) + '\n'
        return out

    def update_position(self, y, x, val):
        self.array[y][x] = val

    def add_rule(self, rule):
        greater_than = '>'
        less_than = '<'
        if type(rule) == list:
            a, comp, b = rule
            if comp == greater_than:
                self.rules[a[0]][a[1]] += [[greater_than, b]]
                self.rules[b[0]][b[1]] += [[less_than, a]]
            else:
                self.rules[a[0]][a[1]] += [[less_than, b]]
                self.rules[b[0]][b[1]] += [[greater_than, a]]
        else:
            rule = [[int(rule[0]), int(rule[1])], rule[2], [int(rule[3]), int(rule[4])]]
            self.add_rule(rule)

    def add_rules(self, rules_list):
        for rule in rules_list:
            self.add_rule(rule)

    def check_rule(self, position):
        y, x = position
        impossibles = set()
        position_rules = self.rules[y][x]
        for comparison, [comparison_y, comparison_x] in position_rules:
            comparison_val = self.array[comparison_y][comparison_x]
            if comparison_val:
                if comparison == '>':
                    numbers = [n for n in self.number_range if n < comparison_val]
                else:
                    numbers = [n for n in self.number_range if n > comparison_val]
                impossibles.update(numbers)

        return impossibles

    def get_horizontal_and_vertical(self, position):
        y, x = position
        horizontal_row = self.array[y]
        vertical_column = list(list(zip(*self.array))[x])
        return horizontal_row, vertical_column

    def get_options(self, position):
        row, col = self.get_horizontal_and_vertical(position)
        impossibles = set()
        used = set(row + col)
        impossibles.update(used)
        rule_limits = self.check_rule(position)
        impossibles.update(rule_limits)
        options = []
        for n in self.number_range:
            if n not in impossibles:
                options += [n]
        return options

    def prioritise_options(self):
        all_options = self.get_all_options()
        my_key = lambda x: len(x[1])
        return sorted(all_options, key=my_key)

    def get_all_options(self):
        all_options = []
        for y in range(self.size):
            for x in range(self.size):
                if not self.array[y][x]:
                    options = self.get_options([y, x])
                    if options:
                        all_options += [[[y, x], options]]
        return all_options

    def complete(self):
        normal = self.array
        transposed = list(zip(*normal))
        for view in [normal, transposed]:
            for row in view:
                for n in self.number_range:
                    if n not in row:
                        return False
        return True


kakuro_1 = {'size': 5,
            'positions': [
                (1, 1, 4),
                (4, 0, 4),
                (0, 0, 1)],
            'rules': [
                '00<01',
                '01<11',
                '13<14',
                '22>32',
                '32>33',
                '34>44',
                '40>41',
                '43<44']}

kakuro2_1 = {
    'size': 4,
    'positions': [
        ('A1', '1'),
        ('A2', '3')
    ],
    'rules': [
        'A2<A3',
        'A2>B2',
        'B2>B3',
        'B1<C1'
    ]
}

array = Kakuro2(kakuro2_1)

# print('**')
print('***')
# for key, val in array.array.items():
#     print(key, val)
print(array)


def solve(my_array):
    print(my_array)
    checked_opts = my_array.prioritise_options()
    if my_array.complete():
        return my_array
    elif checked_opts:
        position, options = checked_opts[0]
        for option in options:
            guess = position + [option]
            new_array = deepcopy(my_array)
            new_array.update_position(*guess)
            possible = solve(deepcopy(new_array))
            if possible is not None:
                return possible

# ans = solve(array)



