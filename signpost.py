def pprint(cont):
    for _ in cont:
        print(_)


class Cell(object):
    def __init__(self, position, direction, value=0):
        self.position = position
        self.direction = direction
        self.value = value
        self.pointed_by = set()
        self.point_at = set()

    def __str__(self):
        out = "{}".format(self.value or self.direction)
        return out


class Map(object):
    def __init__(self, size):
        self.size = size



map = 'dr1,d,dl,dl,d,dr,13u,d,r,u,l,dl,ur,ur,ul,16f'

pos = []
for x in range(4):
    for y in range(4):
        pos += [(x, y)]

map_pos = zip(pos, map.split(','))

pprint(map_pos)


print(8//10)