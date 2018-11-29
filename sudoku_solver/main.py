grid = []

for i in range(3):
    grid.append([3*i + j + 1 for j in range(3)])

print(grid)
print(grid[0])
print([grid[i][0] for i in range(3)])