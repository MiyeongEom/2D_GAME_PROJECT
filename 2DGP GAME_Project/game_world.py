# 1 background
# 2 block
# 3 main_hero

objects = [[], [], []]  #2d에선 그리는 순서가 중요함 -> 이중리스트

# 'boy:ball' : [ (boy), (ball1, ball2, ball3, ...)]
collision_group = dict()

def add_object(o, depth):
    objects[depth].append(o)

def add_objects(ol, depth):
    objects[depth] += ol

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o
            return
    raise ValueError('Trying destroy non existing object')

def all_objects():
    for layer in objects:
        for o in layer:
            yield o

def clear():
    for o in all_objects():
        del o
    for layer in objects:
        layer.clear()

def add_collision_group(a, b, group):
    if group not in collision_group:
        print('Add new group ', group)
        collision_group[group] = [    [],     [] ]

    if a: #a가 있으면
        if type(a) == list: #근데 만약 a가 리스트(여러 개)면
            collision_group[group][0] += a
        else: #단일 오브젝트라면
            collision_group[group][0].append(a)

    if b:
        if type(b) == list: #근데 만약 a가 리스트(여러 개)면
            collision_group[group][1] += b
        else: #단일 오브젝트라면
            collision_group[group][1].append(b)


def all_collision_pairs():
    #collison-group이라는 딕셔너리에서 각 리스트로부터 페어를 만들어서 보내준다
    for group, pairs in collision_group.items(): #items() key, value
        for a in pairs[0]:
            for b in pairs[1]:
                yield a, b, group

def remove_collision_object(o):
    for pairs in collision_group.values():
        if o in pairs[0]: pairs[0].remove(o)
        elif o in pairs[1]: pairs[1].remove(o)

def update():
    for game_object in all_objects():
        game_object.update()