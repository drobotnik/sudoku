def pprint(thing):
    for row in thing:
        print(row)


def row_creator(size, sandwich_row=False):
    if sandwich_row:
        block = ['', '']
    else:
        block = [0, '']
    out = []
    for col in range(size - 1):
        out += block
    return out + ['' if sandwich_row else 0]

def array_creator(size):
   out = []
   for row in range(size - 1):
        out += [row_creator(size)]
        out += [row_creator(size, sandwich_row=True)]
   out += [row_creator(size)]
   return out


class Kakuro(object):
    def __init__(self, size):
        self.size = size
        self.array = array_creator(size)

    def __str__(self):
        out = ''
        for _ in self.array:
            out+= str(_) + '\n'
        return out

    def update_position(self,x, y, val):
        self.array[y * 2][x * 2] = val

    def add_rule(self, rule):
        coord_a = rule[0]
        comparison = rule[1]
        coord_b = rule[2]
        zipped = list(zip(coord_a, coord_b))
        return zipped

    def check_rows(self, array):
        for row in array:
            row_ints = sorted([val for val in row if type(val) is int])
            if row_ints:
                if row_ints != list(range(1, self.size + 1)):
                    return False
        return True


    def check_solution(self):
        print('solution')
        normal = self.array
        transposed = list(zip(*normal))
        pprint(normal)
        pprint('**')
        pprint(transposed)
        rows = self.check_rows(normal)
        cols = self.check_rows(transposed)
        return (rows, cols)






array = Kakuro(4)

for x in range(4):
    for y in range(4):
        array.update_position(x, y, y + 1)

rule = [[1, 1],
        '<',
        [1, 2]]

rule2 = [[2, 2],
         '>',
         [3, 2]]swdeda

print(array.check_solution())

