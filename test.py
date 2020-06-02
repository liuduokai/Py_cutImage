import os
import re

if __name__ == '__main__':
    inputDir = "./input"
    files = os.listdir(inputDir)
    for file in files:
        filetype = file[(re.search('.', file).span()[1] + 1):len(file)]
        print(filetype)
