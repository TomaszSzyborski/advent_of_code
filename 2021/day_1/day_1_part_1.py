with open("input.txt") as f:
    measurements = list(map(int, f.readlines()))

increased = 0
for index in range(1, len(measurements)):
    if measurements[index] > measurements[index-1]:
        increased += 1

print(increased)
