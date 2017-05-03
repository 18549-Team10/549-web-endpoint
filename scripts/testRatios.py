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

# keg data
# peaks  ratio  success  close
#    10    .01     .284   .539
#     4    .01     .201   .486
