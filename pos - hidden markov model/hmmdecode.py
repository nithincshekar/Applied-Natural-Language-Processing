import sys
import pickle

def TagData(lines):
    with open("hmmmodel.txt") as data_file:    
        data = pickle.load(data_file)
    transition = data["transition"]
    emission = data["emission"]
    wordsSet = set()
    # get the tags
    tags = []
    for key, val in transition.items():
        tags.append(key)

    for key, val in emission.items():
        wordsSet.add(key[:-3])

    # get the data
    for line in lines:
        array = line.strip().split(" ")

        valList = []
        valInit = {}
        valInit[array[0]] = {}
        for tag in tags:
            if str(array[0]) + "/" + str(tag) in emission:
                valInit[array[0]]["qi" + "-" + str(tag)] = emission[str(array[0]) + "/" + str(tag)] * transition["qi"][str(tag)]
            elif str(array[0]) not in wordsSet:
                valInit[array[0]]["qi" + "-" + str(tag)] = transition["qi"][str(tag)]
        valList.append(valInit)

        for i in range(1, len(array)):
            valDict = {}
            valDict[array[i]] = {}
            for tag in tags:
                if str(array[i]) + "/" + str(tag) in emission:
                    for preVal in valList[i-1][array[i-1]]:
                        nTemp = preVal.split('-')[1]
                        valDict[array[i]][nTemp + '-' + tag] = valList[i-1][array[i-1]][preVal] * emission[str(array[i]) + "/" + str(tag)] * transition[str(nTemp)][str(tag)]
                elif str(array[i]) not in wordsSet:
                    for preVal in valList[i-1][array[i-1]]:
                        nTemp = preVal.split('-')[1]
                        valDict[array[i]][nTemp + '-' + tag] = valList[i-1][array[i-1]][preVal] * transition[str(nTemp)][str(tag)]
            valList.append(valDict)

        outPut = None
        link = None
        for i in range(len(valList) - 1, -1, -1):
            maxValKey = max(valList[i][array[i]], key=(valList[i][array[i]]).get)
            if link is None:
                outPut = str(array[i]) + "/" + str(maxValKey.split("-")[1]) + "\n"
                link = maxValKey.split("-")[0]
            else:
                while link not in maxValKey.split("-")[1]:
                    valList[i][array[i]][maxValKey] = float("-inf")
                    maxValKey = max(valList[i][array[i]], key=(valList[i][array[i]]).get)
                outPut = str(array[i]) + "/" + str(maxValKey.split("-")[1]) + " " + outPut
                link = maxValKey.split("-")[0]
        text_file.write(outPut)
    text_file.close()
    return

text_file = open("hmmoutput.txt", "w")
with open(sys.argv[1]) as f:
    lines = f.readlines()
    TagData(lines)