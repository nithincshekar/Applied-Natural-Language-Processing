import sys
import pickle

def TransitionProbability(lines):
    outerDict = {}
    outerDict["qi"] = {}
    for line in lines:
        array = line.split(" ")

        # for the first item
        firstItem = array[0].split("/")
        firstItem = firstItem[len(firstItem)-1]
        if firstItem not in outerDict["qi"]:
            outerDict["qi"][firstItem] = 1
        else:
            outerDict["qi"][firstItem] = outerDict["qi"][firstItem] + 1

        # for rest of the items
        for i in range(len(array)):

            # if last item, break
            if (i+1) == len(array):
                break

            # first item
            val1 = array[i].split("/")
            val1 = val1[len(val1)-1]

            # second item
            val2 = array[i+1].strip().split("/")
            val2 = val2[len(val2)-1]

            # add values to the dictionary
            if val1 not in outerDict:
                outerDict[val1] = {}
                outerDict[val1][val2] = 1
            elif val2 not in outerDict[val1]:
                outerDict[val1][val2] = 1
            else:
                outerDict[val1][val2] = outerDict[val1][val2] + 1
    return outerDict

def EmissionProbability(lines):
    keyDict = {}
    tagDict = {}
    transTagDict = {}
    for line in lines:
        array = line.strip().split(" ")
        for i in range(0,len(array)):
            if array[i] in keyDict:
                keyDict[array[i]] = keyDict[array[i]] + 1
            else:
                keyDict[array[i]] = 1
            splt = array[i].split("/")
            splt = splt[len(splt)-1]
            if splt in tagDict:
                tagDict[splt] = tagDict[splt] + 1
                transTagDict[splt] = tagDict[splt]
                if (i + 1) == len(array):
                    transTagDict[splt] = transTagDict[splt] - 1
            else:
                tagDict[splt] = 1
                transTagDict[splt] = tagDict[splt]
                if (i + 1) == len(array):
                    transTagDict[splt] = transTagDict[splt] - 1

    return keyDict,tagDict,transTagDict

with open(sys.argv[1]) as f:
    lines = f.readlines()
    keyDict,tagDict,transTagDict = EmissionProbability(lines)
    outerDict = TransitionProbability(lines)

with open("hmmmodel.txt", 'w') as w:
    emiDump = {}
    traDump = {}
    outerProb = {}

    tags = set()
    for key, val in outerDict.items():
        tags.add(key)
    length = len(tags)

    # emission
    for key, val in keyDict.items():
        tag = key.split("/")
        tag = tag[len(tag)-1]
        eProb = float(keyDict[key]) / float(tagDict[tag])
        emiDump[key] = eProb

    # transition
    for key, val in outerDict.items():
        if key is not "qi":
            traDump[key] = {}
            for ikey, ival in val.items():
                traDump[key][ikey] = float(ival + 1) / float(transTagDict[key] + length)
        else:
            traDump["qi"] = {}
            for ikey, ival in val.items():
                traDump["qi"][ikey] = float(ival + 1) / float(len(lines) + length)

    # for tags not seen in the training data
    for key, val in outerDict.items():
        for itm in tags:
            if itm not in outerDict[key]:
                if key is "qi":
                    traDump["qi"][itm] = float(1) / float(len(lines) + length)
                else:
                    traDump[key][itm] = float(1) / float(transTagDict[key] + length)


    outerProb["transition"] = traDump
    outerProb["emission"] = emiDump
    pickle.dump(outerProb, w)