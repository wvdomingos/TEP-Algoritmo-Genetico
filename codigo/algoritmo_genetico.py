# -*- coding: utf-8 -*-

# Programa em Python para gerar a frase de destino, começando a partir
# de frase aleatória usando algoritmo genético
# Referencia: https://www.geeksforgeeks.org/genetic-algorithms/

import random

# Número de indivíduos em cada geração
POPULATION_SIZE = 100

# Genes válidos
GENES = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890, .-;:_!"#%&/()=?@${[]}'''

# Frase de destino a ser gerada
TARGET = "Eu nao sou um robo!"


class Individual(object):
    ''' 
    Classe representando indivíduo na população
    '''

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.cal_fitness()

    @classmethod
    def mutated_genes(self):
        ''' 
        Criar genes aleatórios para mutação
        '''
        global GENES
        gene = random.choice(GENES)
        return gene

    @classmethod
    def create_gnome(self):
        ''' 
        Criar cromossomo ou frase de genes
        '''
        global TARGET
        gnome_len = len(TARGET)
        return [self.mutated_genes() for _ in range(gnome_len)]

    def mate(self, par2):
        ''' 
        Realizar acasalamento e produzir novos descendentes
        '''

        # cromossomo para descendentes
        child_chromosome = []
        for gp1, gp2 in zip(self.chromosome, par2.chromosome):

            # random probability
            prob = random.random()

            # if prob is less than 0.45, insert gene
            # from parent 1
            if prob < 0.45:
                child_chromosome.append(gp1)

            # if prob is between 0.45 and 0.90, insert
            # gene from parent 2
            elif prob < 0.90:
                child_chromosome.append(gp2)

            # otherwise insert random gene(mutate),
            # for maintaining diversity
            else:
                child_chromosome.append(self.mutated_genes())

        # criar novos Indivíduos (descendentes) usando
        # cromossomo gerado para o descendente
        return Individual(child_chromosome)

    def cal_fitness(self):
        ''' 
        Calcula a pontuação de fittness, é o número de 
        caracteres da frase que diferem da 
        frase de destino.
        '''
        global TARGET
        fitness = 0
        for gs, gt in zip(self.chromosome, TARGET):
            if gs != gt:
                fitness += 1
        return fitness

# Driver code


def main():
    global POPULATION_SIZE

    # Geração corrente
    generation = 1

    found = False
    population = []

    # Cria a população Inicial
    for _ in range(POPULATION_SIZE):
        gnome = Individual.create_gnome()
        population.append(Individual(gnome))

    while not found:

        # classificar a população em ordem crescente de pontuação de aptidão
        population = sorted(population, key=lambda x: x.fitness)

        # se o indivíduo com menor pontuação de aptidão ou seja.
        # 0 então sabemos que chegamos ao alvo
        # e sai do loop
        if population[0].fitness <= 0:
            found = True
            break

        # Caso contrário, gerar novos descendentes para a nova geração
        new_generation = []

        # Perform Elitism, que significa 10% da população mais apta
        # vai para a próxima geração
        s = int((10*POPULATION_SIZE)/100)
        new_generation.extend(population[:s])

        # De 50% da população mais apta, Indivíduos
        # vai acasalar para produzir descendentes
        s = int((90*POPULATION_SIZE)/100)
        for _ in range(s):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            child = parent1.mate(parent2)
            new_generation.append(child)

        population = new_generation

        print("Geração: {}\tFrase: {}\tAvaliação: {}".
              format(generation,
                     "".join(population[0].chromosome),
                     population[0].fitness))

        generation += 1

    print("Geração: {}\tFrase: {}\tAvaliação: {}".
          format(generation,
                 "".join(population[0].chromosome),
                 population[0].fitness))


if __name__ == '__main__':
    main()
