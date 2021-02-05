'''
You're given a two-dimensional array (a matrix) of potentially unequal height
and width containing only 0s and 1s. Each
0 represents land, and each 1 represents part of a
river. A river consists of any number of 1s that are either
horizontally or vertically adjacent (but not diagonally adjacent). The number
of adjacent 1s forming a river determine its size.


Note that a river can twist. In other words, it doesn't have to be a straight
vertical line or a straight horizontal line; it can be L-shaped, for example.

Write a function that returns an array of the sizes of all rivers represented
in the input matrix. The sizes don't need to be in any particular order.

Sample INPUT:
matrix = [
    [1, 0, 0, 1, 0],
    [1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 1, 1, 0],
]

Sample OUTPUT:
[1, 2, 2, 2, 5] The numbers could be ordered differently.

The rivers can be clearly seen here:
[
    [1,  ,  , 1,  ],
    [1,  , 1,  ,  ],
    [ ,  , 1,  , 1],
    [1,  , 1,  , 1],
    [1,  , 1, 1,  ],
]
'''


def riverSizes(matrix):
    marked = set()
    river_lens = []

    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            cur_pos = matrix[r][c]
            if (r, c) not in marked and cur_pos == 1:
                marked.add((r, c))
                cur_len_riv = 1
                stack = [(r, c)]

                while stack:
                    directions = [[0, 1], [1, 0], [-1, 0], [0, -1]]
                    r_stack, c_stack = stack.pop(0)

                    for d in directions:
                        if 0 <= r_stack + d[0] < len(matrix) and \
                                0 <= c_stack + d[1] < len(matrix[r]) \
                                and (r_stack + d[0], c_stack + d[1]) not in marked \
                                and matrix[r_stack + d[0]][c_stack + d[1]] == 1:
                            stack.append((r_stack + d[0], c_stack + d[1]))
                            marked.add((r_stack + d[0], c_stack + d[1]))
                            cur_len_riv += 1
                river_lens.append(cur_len_riv)
    return river_lens


m = [
  [1, 0, 0, 1, 0],
  [1, 0, 1, 0, 0],
  [0, 0, 1, 0, 1],
  [1, 0, 1, 0, 1],
  [1, 0, 1, 1, 0],
]

print(riverSizes(m))
