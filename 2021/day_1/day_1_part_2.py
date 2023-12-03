with open("input.txt") as f:
    measurements = list(map(int, f.readlines()))

sumz = []
for index in range(0, len(measurements) - 2):
    summa = measurements[index] + measurements[index + 1] + measurements[index + 2]
    sumz.append(summa)

print(sumz)

increased = 0
for index in range(1, len(sumz)):
    if sumz[index] > sumz[index-1]:
        increased += 1

print(increased)