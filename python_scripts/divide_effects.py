import os
import shutil
import sys
from random import sample

EXT = [".jpg", ".png"]

# remember '/' at the end of each param!
inp_path = sys.argv[1]
out_path = sys.argv[2]
if not os.path.exists(out_path):
    os.makedirs(out_path)


def main():
    file_list = [f for f in os.listdir(inp_path) if f.endswith(tuple(EXT))]
    for i in range(0, 11):
        extract_list = sample(file_list, 200)
        print('\n'.join(extract_list), file=open(out_path + 'chunk' + str(i) + '.txt', 'a'))
        file_list = set(file_list) - set(extract_list)
        for filename in extract_list:
            if not os.path.exists(out_path + str(i)):
                os.makedirs(out_path + str(i))
            shutil.move(inp_path + filename, out_path + str(i) + '/' + filename)


if __name__ == '__main__':
    sys.exit(main())
