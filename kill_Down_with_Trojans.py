import numpy as np
import scipy


def load_input_file(file_name):
    with open(file_name, 'r') as file:
        n, H = map(int, file.readline().split())
        tile_types = np.zeros((n, n), dtype=int)
        tile_values = np.zeros((n, n), dtype=int)

        for i in range(n * n):
            if i == 0:
                continue  # the initial tile is zero type with zero value
            x, y, t, v = map(int, file.readline().split())
            tile_types[x][y] = t
            tile_values[x][y] = v

    return n, H, tile_types, tile_values


def print_tile_data(tile_types, tile_values):
    print("Tile Types:")
    print(tile_types)
    print("\nTile Values:")
    print(tile_values)


def DP(n, H, tile_types, tile_values):
    # TODO
    # Placeholder function - implement your logic here
    # Your code to check whether it is possible to reach the bottom-right
    # corner without running out of HP should go here.
    # You should use dynamic programming to solve the problem.
    # Return True if possible, False otherwise.

    # By defualt we return False
    # TODO you should change this

    memo = np.empty(shape=(n, n, 2, 2))
    for i in range(n):
        for j in range(n):
            for k in range(2):
                for l in range(2):
                    memo[i][j][k][l] = np.nan
    
    res = DP_helper(n, tile_types, tile_values, 0, 0, False, False, memo)
    print('\nMemo Table:\n')
    for row in memo:
        print(row)
    
    if res > H:
        return 0
    else:
        return 1

def DP_helper(n, tile_types, tile_values, x, y, protect, mult, memo):
    
    if x == (n - 1) and y == (n - 1):
        if tile_types[x][y] == 0:
            if protect:
                return 0
            else:
                return tile_values[x][y]
        else:
            return 0
        
    elif not np.isnan(memo[x][y][int(protect)][int(mult)]):
        return memo[x][y][int(protect)][int(mult)]
    
    elif x == (n - 1): # AT BOTTOM-MOST POINT
        if tile_types[x][y] == 0: # DAMAGE
            if protect:
                use_right = DP_helper(n, tile_types, tile_values, x, y + 1, not protect, mult, memo)
                dont_use_right = tile_values[x][y] + DP_helper(n, tile_types, tile_values, x, y + 1, protect, mult, memo)
                memo[x][y][int(protect)][int(mult)] = min(use_right, dont_use_right)
            else:
                right = tile_values[x][y] + DP_helper(n, tile_types, tile_values, x, y + 1, protect, mult, memo)
                memo[x][y][int(protect)][int(mult)] = right
        elif tile_types[x][y] == 1: # HEAL
            if mult:
                use_right = (tile_values[x][y] * -2) + DP_helper(n, tile_types, tile_values, x, y + 1, protect, not mult, memo)
                dont_use_right = (tile_values[x][y] * -1) + DP_helper(n, tile_types, tile_values, x, y + 1, protect, mult, memo)
                memo[x][y][int(protect)][int(mult)] = min(use_right, dont_use_right)
            else:
                right = (tile_values[x][y] * -1) + DP_helper(n, tile_types, tile_values, x, y + 1, protect, mult, memo)
                memo[x][y][int(protect)][int(mult)] = right
        elif tile_types[x][y] == 2: # PROTECTION
            right = DP_helper(n, tile_types, tile_values, x, y + 1, True, mult, memo)
            memo[x][y][int(protect)][int(mult)] = right
        elif tile_types[x][y] == 3: # MULTIPLIER
            right = DP_helper(n, tile_types, tile_values, x, y + 1, protect, True, memo)
            memo[x][y][int(protect)][int(mult)] = right
        
        return memo[x][y][int(protect)][int(mult)]



    elif y == (n - 1): # AT RIGHTMOST POINT
        if tile_types[x][y] == 0: # DAMAGE
            if protect:
                use_down = DP_helper(n, tile_types, tile_values, x + 1, y, not protect, mult, memo)
                dont_use_down = tile_values[x][y] + DP_helper(n, tile_types, tile_values, x + 1, y, protect, mult, memo)
                memo[x][y][int(protect)][int(mult)] = min(use_down, dont_use_down)
            else:
                down = tile_values[x][y] + DP_helper(n, tile_types, tile_values, x + 1, y, protect, mult, memo)
                memo[x][y][int(protect)][int(mult)] = down
        elif tile_types[x][y] == 1: # HEAL
            if mult:
                use_down = (tile_values[x][y] * -2) + DP_helper(n, tile_types, tile_values, x + 1, y, protect, not mult, memo)
                dont_use_down = (tile_values[x][y] * -1) + DP_helper(n, tile_types, tile_values, x + 1, y, protect, mult, memo)
                memo[x][y][int(protect)][int(mult)] = min(use_down, dont_use_down)
            else:
                down = (tile_values[x][y] * -1) + DP_helper(n, tile_types, tile_values, x + 1, y, protect, mult, memo)
                memo[x][y][int(protect)][int(mult)] = down
        elif tile_types[x][y] == 2: # PROTECTION
            down = DP_helper(n, tile_types, tile_values, x + 1, y, True, mult, memo)
            memo[x][y][int(protect)][int(mult)] = down
        elif tile_types[x][y] == 3: # MULTIPLIER
            down = DP_helper(n, tile_types, tile_values, x + 1, y, protect, True, memo)
            memo[x][y][int(protect)][int(mult)] = down

        return memo[x][y][int(protect)][int(mult)]
    


    else:
        if tile_types[x][y] == 0: # DAMAGE
            if protect:
                use_right = DP_helper(n, tile_types, tile_values, x, y + 1, not protect, mult, memo)
                dont_use_right = tile_values[x][y] + DP_helper(n, tile_types, tile_values, x, y + 1, protect, mult, memo)
                use_down = DP_helper(n, tile_types, tile_values, x + 1, y, not protect, mult, memo)
                dont_use_down = tile_values[x][y] + DP_helper(n, tile_types, tile_values, x + 1, y, protect, mult, memo)
                memo[x][y][int(protect)][int(mult)] = min(use_right, dont_use_right, use_down, dont_use_down)
            else:
                right = tile_values[x][y] + DP_helper(n, tile_types, tile_values, x, y + 1, protect, mult, memo)
                down = tile_values[x][y] + DP_helper(n, tile_types, tile_values, x + 1, y, protect, mult, memo)
                memo[x][y][int(protect)][int(mult)] = min(right, down)
        elif tile_types[x][y] == 1: # HEAL
            if mult:
                use_right = (tile_values[x][y] * -2) + DP_helper(n, tile_types, tile_values, x, y + 1, protect, not mult, memo)
                dont_use_right = (tile_values[x][y] * -1) + DP_helper(n, tile_types, tile_values, x, y + 1, protect, mult, memo)
                use_down = (tile_values[x][y] * -2) + DP_helper(n, tile_types, tile_values, x + 1, y, protect, not mult, memo)
                dont_use_down = (tile_values[x][y] * -1) + DP_helper(n, tile_types, tile_values, x + 1, y, protect, mult, memo)
                memo[x][y][int(protect)][int(mult)] = min(use_right, dont_use_right, use_down, dont_use_down)
            else:
                right = (tile_values[x][y] * -1) + DP_helper(n, tile_types, tile_values, x, y + 1, protect, mult, memo)
                down = (tile_values[x][y] * -1) + DP_helper(n, tile_types, tile_values, x + 1, y, protect, mult, memo)
                memo[x][y][int(protect)][int(mult)] = min(right, down)
        elif tile_types[x][y] == 2: # PROTECTION
            right = DP_helper(n, tile_types, tile_values, x, y + 1, True, mult, memo)
            down = DP_helper(n, tile_types, tile_values, x + 1, y, True, mult, memo)
            memo[x][y][int(protect)][int(mult)] = min(right, down)
        elif tile_types[x][y] == 3: # MULTIPLIER
            right = DP_helper(n, tile_types, tile_values, x, y + 1, protect, True, memo)
            down = DP_helper(n, tile_types, tile_values, x + 1, y, protect, True, memo)
            memo[x][y][int(protect)][int(mult)] = min(right, down)

        return memo[x][y][int(protect)][int(mult)]



def write_output_file(output_file_name, result):
    with open(output_file_name, 'w') as file:
        file.write(str(int(result)))


def main(input_file_name):
    n, H, tile_types, tile_values = load_input_file(input_file_name)
    print_tile_data(tile_types, tile_values)
    result = DP(n, H, tile_types, tile_values)
    print("Result: " + str(result))
    output_file_name = input_file_name.replace(".txt", "_out.txt")
    write_output_file(output_file_name, result)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python kill_Down_with_Trojans.py a_file_name.txt")
    else:
        main(sys.argv[1])
