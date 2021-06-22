import os
from random import random,randint, sample
from operator import itemgetter


# Simple [Binary] Evolutionary Algorithm		
def sea(numb_generations,size_pop, size_cromo, prob_mut,prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func,universe,sets):
    # inicialize population: indiv = (cromo,fit)
    populacao = gera_pop(size_pop,size_cromo)
    # evaluate population
    populacao = [(indiv[0], fitness_func(universe,sets,indiv[0])) for indiv in populacao]
    for i in range(numb_generations):
        # sparents selection
        mate_pool = sel_parents(populacao)
	# Variation
	# ------ Crossover
        progenitores = []
        for i in  range(0,size_pop-1,2):
            indiv_1= mate_pool[i]
            indiv_2 = mate_pool[i+1]
            filhos = recombination(indiv_1,indiv_2, prob_cross)
            progenitores.extend(filhos) 
        # ------ Mutation
        descendentes = []
        for indiv,fit in progenitores:
            novo_indiv = mutation(indiv,prob_mut)
            descendentes.append((novo_indiv,fitness_func(universe,sets,novo_indiv)))
        # New population
        populacao = sel_survivors(populacao,descendentes)
        # Evaluate the new population
        populacao = [(indiv[0], fitness_func(universe,sets,indiv[0])) for indiv in populacao]     
    return best_pop(populacao)

def best_pop(populacao):
    populacao.sort(key=itemgetter(1),reverse=False)
    return populacao[0]

# Initialize population
def gera_pop(size_pop,size_cromo):
    return [(gera_indiv(size_cromo),0) for i in range(size_pop)]

def gera_indiv(size_cromo):
    # random initialization
    indiv = [randint(0,1) for i in range(size_cromo)]
    return indiv

# Variation operators: Binary mutation	    
def muta_bin(indiv,prob_muta):
    # Mutation by gene
    cromo = indiv[:]
    for i in range(len(indiv)):
        cromo[i] = muta_bin_gene(cromo[i],prob_muta)
    return cromo

def muta_bin_gene(gene, prob_muta):
    g = gene
    value = random()
    if value < prob_muta:
        g ^= 1
    return g

# Variation Operators :Crossover
def one_point_cross(indiv_1, indiv_2,prob_cross):
	value = random()
	if value < prob_cross:
	    cromo_1 = indiv_1[0]
	    cromo_2 = indiv_2[0]
	    pos = randint(0,len(cromo_1))
	    f1 = cromo_1[0:pos] + cromo_2[pos:]
	    f2 = cromo_2[0:pos] + cromo_1[pos:]
	    return ((f1,0),(f2,0))
	else:
	    return (indiv_1,indiv_2)

# Parents Selection: tournament
def tour_sel(t_size):
    def tournament(pop):
        size_pop= len(pop)
        mate_pool = []
        for i in range(size_pop):
            winner = one_tour(pop,t_size)
            mate_pool.append(winner)
        return mate_pool
    return tournament

def one_tour(population,size):
    """Minimization Problem. Deterministic"""
    pool = sample(population, size)
    pool.sort(key=itemgetter(1), reverse=False)
    return pool[0]

# Survivals Selection: elitism
def sel_survivors_elite(elite):
    def elitism(parents,offspring):
        size = len(parents)
        comp_elite = int(size* elite)
        offspring.sort(key=itemgetter(1), reverse=False)
        parents.sort(key=itemgetter(1), reverse=False)
        new_population = parents[:comp_elite] + offspring[:size - comp_elite]
        return new_population
    return elitism

#receives the genotype and the sets and returns the phenotype solution
def geno2pheno(genotype,sets):
    phenotype = []
    i=0
    while i<len(genotype):
        if(genotype[i]==1):
            phenotype.append(sets[i])
        i+=1
    return phenotype

#fitness function
def fitness(universe,sets,solution):
    alfa = 1
    beta = 0.2
    gama = 0.2
    i=0
    pheno = geno2pheno(solution,sets)
    result = universe
    while i<len(pheno):
        result = [x for x in result if x not in pheno[i]]
        i+=1
    missing = len(result)

    overlap = 0
    i=0
    while i<len(pheno)-1:
        j=i+1
        while j<len(pheno):
            overlap += len(set(pheno[i]) & set(pheno[j]))
            j+=1
        i+=1
    i=0

    setSize = len(pheno)

    fitnessValue = alfa*missing + beta*overlap + gama*setSize
    return fitnessValue

def displayResult(solution):
    genotype = solution[0]
    fitnessScore = solution[1]
    phenotype = geno2pheno(genotype,sets)
    print("Universe Size: %d" % (len(universe)))
    print("Fitness: %f" % (fitnessScore))
    print("Sets used:")
    i=0
    while i<len(phenotype):
        print(phenotype[i])
        i+=1



def readFile(filename):
    script_dir = os.path.dirname(__file__)
    rel_path = os.path.join("set_covering_data",filename)
    abs_file_path = os.path.join(script_dir, rel_path)
    f = open(abs_file_path, 'r')
    lines = f.readlines()
    
    setNum = lines[0].split()[0]
    sets = []
    universe = list(map(str,range(1, int(lines[0].split()[1])+1)))
    i=2
    while i<len(lines):
        size = int(lines[i])
        sets.append(lines[i+1].split())
        i = i+2
    f.close()
    return universe,sets

if __name__ == '__main__':
    filename = "a_5_10.txt"
    num_generations = 100
    size_pop = 10
    prob_mut = 0.01
    prob_cross = 0.9
    tour_size = 3
    elitism = 0.02
    
    universe, sets = readFile(filename)
    size_crom = len(sets)

    best = sea(num_generations, size_pop,size_crom,prob_mut,prob_cross,tour_sel(tour_size),one_point_cross,muta_bin,sel_survivors_elite(elitism), fitness,universe,sets)
    displayResult(best)

    
