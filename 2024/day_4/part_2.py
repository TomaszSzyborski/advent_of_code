description = """
--- Part Two ---
The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle;
it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. 
One way to achieve that is like this:

M.S
.A.
M.S
Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?

"""


def x_mas_counter(data):
    count = 0
    for i in range(1, len(data) - 1):
        print(f"Searched line {i}: {data[i]}")
        for j in range(1, len(data[i]) - 1):
            diagonal_a = data[i - 1][j - 1] + data[i][j] + data[i + 1][j + 1]
            diagonal_b = data[i + 1][j - 1] + data[i][j] + data[i - 1][j + 1]
            partial_sum = [diagonal_a, diagonal_b, diagonal_a[::-1], diagonal_b[::-1]].count("MAS")
            print([diagonal_a,
                   diagonal_b,
                   diagonal_a[::-1],
                   diagonal_b[::-1],])
            print(f"{partial_sum=}")
            count += partial_sum == 2
    return count


def main():
    with open("input.txt") as f:
        data = f.read().split('\n')
    print(x_mas_counter(data))


if __name__ == '__main__':
    main()
    #5419 too high
    #1868 good