import argparse
from PIL import Image
import random

PIXELS = 800
MAX_VAL = 255

class Grid:
    MOVES = ((1, 0), (0, 1), (-1, 0), (0, -1))

    def __init__(self, size):
        self.size = size
        self.grid = []
        for i in range(size):
            self.grid.append([0] * size)

    def __getitem__(self, dex):
        i, j = dex
        return self.grid[i][j]

    def __setitem__(self, dex, val):
        i, j = dex
        self.grid[i][j] = val

    def on_edge(self, x, y):
        return (x == 0) or (y == 0) or \
            (x == self.size - 1) or (y == self.size - 1)

    def fill(self):
        x, y = self.size // 2, self.size // 2
        self[x, y] += 1
        while not self.on_edge(x, y):
            x, y = self.move(x, y)
            self[x, y] += 1

    def move(self, x, y):
        dx, dy = random.choice(self.MOVES)
        return x + dx, y + dy


def main():
    args = parse_args()
    if args.seed is not None:
        random.seed(args.seed)
    grid = Grid(args.size)
    for i in range(args.walkers):
        grid.fill()
    img = make_image(args, grid)
    if args.outfile:
        save(args, img)
    else:
        show(img)


def make_image(args, grid):
    n = grid.size
    max_val = max(max(row) for row in grid.grid) or 1
    img = Image.new("L", (n, n))
    for i in range(n):
        for j in range(n):
            val = grid[i, j]
            shade = MAX_VAL - MAX_VAL * val // max_val
            img.putpixel((j, i), shade)
    return img.resize((args.pixels, args.pixels), Image.NEAREST)


def save(args, img):
    img.save(args.outfile)


def show(img):
    img.show()


def parse_args():
    parser = argparse.ArgumentParser(description="random walk")
    parser.add_argument("--outfile", type=str, help="output file")
    parser.add_argument("--pixels", type=int, default=PIXELS, help="image size in pixels")
    parser.add_argument("--seed", type=int, help="RNG seed")
    parser.add_argument("--size", type=int, default=101, help="grid size")
    parser.add_argument("--walkers", type=int, default=1, help="number of walkers")
    return parser.parse_args()


if __name__ == "__main__":
    main()
