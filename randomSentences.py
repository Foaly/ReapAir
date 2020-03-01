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


def generateIndicesWithoutRepetition(numberOfIndicies, maxIndex):
    """
    A helper function to randomly generator indices without repetition
    between [0, maxIndex].

    :param numberOfIndicies: number of indicies to generate
    :param maxIndex: the highest possible index
    """
    randomIndices = []
    while len(randomIndices) < numberOfIndicies:
        index = round(random.random() * maxIndex)  # TODO: can random become 1.0 ?
        if index not in randomIndices:
            randomIndices.append(index)
    return randomIndices


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

    randomIndices = generateIndicesWithoutRepetition(numberOfSenctences, length - 1)
    lineNumber = 1
    print()
    for index in randomIndices:
        print(str(lineNumber) + ": " + sentences[index])
        lineNumber += 1
    print()


if __name__ == '__main__':
    main()
