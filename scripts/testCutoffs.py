import test

def testCutoffs(numTrials = 100):
    tested = set()
    bestCutoff, bestScore, allCutoffs = None, None, []
    for cutoff in range(1000,10000):
        score = test.test(numTrials,halfDiff=cutoff)
        allCutoffs.append(score)
        if bestScore == None or score > bestScore:
            bestCutoff, bestScore = ratio, score
    return bestCutoff, bestScore, allCutoffs