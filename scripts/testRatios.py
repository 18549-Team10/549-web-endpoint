import test

def frange(start, stop, step):
    out = []
    i = start
    while i < stop: 
        out.append(i)
        i += step
    return out

def testRatios(numTrials = 100):
    tested = set()
    bestRatio, bestScore, allRatios = None, None, []
    # for ratio in frange(.001,2,.001):
    #     score = test.test(numTrials,ratio)
    #     allRatios.append(score)
    #     if bestScore == None or score > bestScore:
    #         bestRatio, bestScore = ratio, score
    for ratio in range(70,120):
        score = test.test(numTrials,ratio = ratio)
        allRatios.append(score)
        if bestScore == None or score > bestScore:
            bestRatio, bestScore = ratio, score
    return bestRatio, bestScore, allRatios

def testSamplePeakModifications(numTrials = 100):
    bestModifications, bestScore, allResults = None, None, []
    for add in frange(0, 1.5, .1):
        for mult in frange(.5, 1.5, .1):
            score = test.test(numTrials, ratio = 1, magMult = mult, magAdd = add)
            if bestScore == None or score > bestScore:
                bestModifications, bestScore = (add, mult), score
            allResults.append(((add, mult), score))
    return bestModifications, bestScore, allResults

# keg data
# peaks  ratio  success  close
#    10    .01     .284   .539
#     4    .01     .201   .486
