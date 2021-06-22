def fitness(universe,sets,solution):
    alfa = 1
    beta = 0.2
    gama = 0.2
    i=0
    pheno = geno2pheno(solution,sets)
    result = universe
    while i<len(pheno):
        resultTemp = []
        for x in result:
            if x not in pheno[i]
                resultTemp.append(x)
        result = resultTemp
        i+=1
    missing = len(result)
    overlap = 0
    i=0
    while i<len(pheno)-1:
        j=i+1
        while j<len(pheno):
            setTemp = set(pheno[i]) & set(pheno[j])
            overlap += len(setTemp)
            j+=1
        i+=1
    i=0
    setSize = len(pheno)
    fitnessValue = alfa*missing + beta*overlap + gama*setSize
    return fitnessValue
