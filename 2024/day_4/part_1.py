description = """
--- Day 4: Ceres Search ---
"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:


..X...
.SAMX.
.A..A.
XMAS.S
.X....
The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
Take a look at the little Elf's word search. How many times does XMAS appear?
"""


def xmas_counter(data: [str]) -> int:
    """Returns the number of times XMAS appears in data."""
    count = 0
    for i in range(len(data)):
        print(f"Searched line {i}: {data[i]}")
        for j in range(len(data[i])):
            forwards = backwards = upper_right = upper_left = up = down = lower_right = lower_left = ""
            print(f"Searched index {i}, {j}")
            if j+4 < len(data[i]):
                forwards = data[i][j:j + 4]
            if j-3 >= 0 and j+1 < len(data[i]):
                backwards = data[i][j-3:j+1][::-1]
            if i-3 >= 0 and j+3 < len(data[i]):
                upper_right = data[i][j] + data[i -1][j + 1] + data[i - 2][j + 2] + data[i - 3][j + 3]
            if i-1 >= 0 and j-3>=0:
                upper_left = data[i][j] + data[i - 1][j - 1] + data[i - 2][j - 2] + data[i - 3][j - 3]
            if i-3 >= 0:
                up = data[i][j] + data[i - 1][j] + data[i - 2][j] + data[i - 3][j]
            if i+3 < len(data):
                down = data[i][j] + data[i + 1][j] + data[i + 2][j] + data[i + 3][j]
            if j+3 < len(data[i]) and i+3 < len(data):
                lower_right = data[i][j] + data[i + 1][j + 1] + data[i +  2][j + 2] + data[i +  3][j + 3]
            if j-3 >= 0 and i+3 < len(data):
                lower_left = data[i][j] + data[i + 1][j - 1] + data[i +  2][j - 2] + data[i +  3][j - 3]

            print([f"{forwards=}",
                   f"{backwards=}",
                   f"{upper_right=}",
                   f"{upper_left=}",
                   f"{up=}",
                   f"{down=}",
                   f"{lower_right=}",
                   f"{lower_left=}",
                  ])
            counted = [forwards, backwards, upper_right, upper_left, up, down, lower_right, lower_left].count("XMAS")
            count += counted

            print(count)
    return count


if __name__ == '__main__':
    with open("input.txt", "r") as file:
        data = file.read().split("\n")

    print(f"{xmas_counter(data)=}")

# 1131 too low
# 2343 2nd attempt too low
