import os
import shutil
import sys
from random import sample

EXT = [".jpg", ".png"]

# remember no '/' at the end of each param!
inp_path = sys.argv[1]
out_path = sys.argv[2]


# A is blur folder
# B is sharp folder

def main():
    file_list = [f for f in os.listdir(inp_path + '/A') if f.endswith(tuple(EXT))]
    test_list = sample(file_list, int(0.1 * len(file_list)))
    for filename in test_list:
        shutil.move(inp_path + '/A/' + filename, out_path + '/A/' + filename)
        shutil.move(inp_path + '/B/' + filename, out_path + '/B/' + filename)


if __name__ == '__main__':
    sys.exit(main())
