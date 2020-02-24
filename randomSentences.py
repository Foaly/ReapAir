import random
import math


def parseInput(filename):
    sentences = []

    with open(filename, 'r') as inputFile:
        line = inputFile.readline()
        while line:
            # skip empty lines or comments
            line = line.strip()
            if line and not line.startswith('#'):
                # add to our sentence list
                sentences.append(line)
            # get next line
            line = inputFile.readline()

    return sentences


# Weniger Arbeiten mehr Techsupport!
def main():
    filename = "./Sätze_de.txt"
    sentences = parseInput(filename)

    length = len(sentences)
    numberOfSenctences = 10
    randomIndices = []

    while len(randomIndices) < numberOfSenctences:
        index = math.floor(random.random() * length)
        if index not in randomIndices:
            randomIndices.append(index)

    lineNumber = 1
    print()
    for index in randomIndices:
        print(str(lineNumber) + ": " + sentences[index])
        lineNumber += 1
    print()


if __name__ == '__main__':
    main()
