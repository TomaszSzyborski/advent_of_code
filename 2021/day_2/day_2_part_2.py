with open("input.txt") as f:
    directions = list(map(lambda s: (s.split()[0], int(s.split()[1])), f.readlines()))

print(directions)

horizontal = 0
depth = 0
aim = 0

for direction in directions:
    way, amount = direction
    if way == 'forward':
        horizontal += amount
        depth += (aim * amount)
    elif way == 'down':
        aim += amount
    elif way == 'up':
        aim -= amount

print(horizontal)
print(depth)
print(aim)
print(horizontal * depth)
