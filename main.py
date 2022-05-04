from manager import Manager, pygame
import argparse
from vars import WIDTH, X_PADDING

parser = argparse.ArgumentParser(description = "Sorting Algorithms")
parser.add_argument("-f","--fps",type = int, required=False, help = "Specify fps", choices = range(1, 334), metavar = "[1-333]", default = 0)
parser.add_argument("-c","--count",type = int, required=False, help = "Specify number of data", choices = range(2, WIDTH - 2 * X_PADDING + 1), metavar = f"[{2}-{WIDTH - 2 * X_PADDING}]", default = 0)
parser.add_argument("-m",'--muted', default=True, action=argparse.BooleanOptionalAction, help = "True for muting")

args = parser.parse_args()

if __name__ == "__main__":
    manager = Manager(args.count or 400, args.fps, args.muted)
    manager.run()

    pygame.quit()
