import random
import math
import argparse


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

    # setup argument parser
    description = "This program randomly generates Reparatur Anleitungen.\nWeniger Arbeiten, mehr Techsupport!"
    argParser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter,)
    argParser.add_argument("-n", "--count", help="The number of sentences generated.", type=int, default=10)
    args = argParser.parse_args()

    # Clip count argument to usable range
    length = len(sentences)
    numberOfSenctences = args.count
    if numberOfSenctences < 1 or numberOfSenctences > length:
        numberOfSenctences = 10

    # randomly choose indices without repetition
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
