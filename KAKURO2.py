from copy import deepcopy


def pprint(thing):
    for row in thing:
        print(row)


class Kakuro(object):
    def __init__(self, info):
        self.rules = {y: {x: [] for x in range(info['size'])} for y in range(info['size'])}
        if type(info) is int:
            self.size = info
            self.array = [['' for x in range(info)] for y in range(info)]
        elif type(info) is list:
            self.size = len(info)
            self.array = info

        elif type(info) is dict:
            print('its a dict')
            self.size = info['size']
            self.array = [['' for x in range(self.size)] for y in range(self.size)]
            self.add_rules(info['rules'])
            for position in info['positions']:
                self.update_position(*position)
        self.my_range = range(1, self.size + 1)


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
                    numbers = [n for n in self.my_range if n < comparison_val]
                else:
                    numbers = [n for n in self.my_range if n > comparison_val]
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
        for n in self.my_range:
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
                for n in self.my_range:
                    if n not in row:
                        return False
        return True


kakuro_1 = {
    'size': 5,
    'positions': [
        (1, 1, 4),
        (4, 0, 4),
        (0, 0, 1)
    ],
    'rules': [
        '00<01',
        '01<11',
        '13<14',
        '22>32',
        '32>33',
        '34>44',
        '40>41',
        '43<44'
    ]
}

array = Kakuro(kakuro_1)



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


ans = solve(array)

print('ans..')
print(ans)
