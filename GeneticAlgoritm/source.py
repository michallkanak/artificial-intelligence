import numpy as np
from operator import itemgetter
import random
import time

# time waching
start_time = time.time()

population_size = 100
gen = 100
Px = 0.7
# 0.8 roul # 0.7 tour
Pm = 0.15
# 0.04 roul # 0.1 tour
Tour = 5
repeats_range = 10;

global_best = 0
global_worst = 0
global_mean = 0

file = open("data/had12.dat")
for line in file:
    print(line)

# Wczytaj plik od poczatku
file.seek(0)
length = int(file.readline())

file.readline()
# Wczytaj macierz przeplywow
flow = list()
for x in range(0, length):
    row = list()
    values = file.readline().split()
    for value in values:
        row.append(int(value))
    flow.append(row)
flow = np.matrix(flow)

file.readline()
# Wczytaj macierz odleglosci
distances = list()
for x in range(0, length):
    row = list()
    values = file.readline().split()
    for value in values:
        row.append(int(value))
    distances.append(row)
distances = np.matrix(distances)

# Zamknij plik
file.close()


# Kazdy genotyp jest generowany jako losowa lista bez powtorzen
# od 0 do x (gdzie x to dlugosc chromosomu, parametr length).
def generate_first_pop(population_size, length):
    return [
        [
            0, random.sample(range(0, length), length)
        ]
        for y in range(0, population_size)
    ]


# Funkcja celu - liczenie kosztu - odleglosci
def fitness(permutation, length, flow, distances):
    cost = 0
    for x in range(0, length):
        f1 = permutation[x]
        for y in range(0, length):
            f2 = permutation[y]
            cost += flow.item(x, y) * distances.item(f1, f2)
    return cost


# Sortowanie
def sort(population):
    return sorted(population, key=itemgetter(0))


# Selekcja - metoda turniejowa
def tournament_selection(population, tour):
    new_population = list()
    while len(new_population) < population_size:
        random_indexes = random.sample(range(0, population_size), tour)
        choices = list()
        for index in random_indexes:
            choices.append(population[index])
        choices = sort(choices)
        new_population.append(choices[0])
    return new_population


# Selekcja - metoda ruletki
def roulette_selection(population, population_size):
    new_pop = list()
    total_fit = 1
    scores = list()
    for item in population:
        scores.append(item[0])
        total_fit += item[0]
    worst = scores[np.argmax(scores)]
    normalized_scores = list()
    calc_scores = list()
    for x in range(0, population_size):
        temp = (worst - scores[x] + 1) / (total_fit + 1)
        normalized_scores.append([temp, population[x]])
        calc_scores.append(temp)
    normalized_scores = sort(normalized_scores)
    sorted_scores = sorted(calc_scores, key=float)
    sum = np.sum(sorted_scores)
    for _ in range(0, population_size - 1):
        random_numb = random.uniform(0, sum)
        if random_numb < sorted_scores[0]:
            new_pop.append(normalized_scores[0][1])
            continue
        count = 1
        count_sum = sorted_scores[0]
        while random_numb > count_sum:
            count_sum += sorted_scores[count]
            count += 1
        new_pop.append(normalized_scores[count - 1][1])
    new_pop.append(normalized_scores[np.argmax(calc_scores)][1])
    return new_pop


# Wyliczanie kosztu dla wszystkich genotypow z populacji
def evaluation(population, population_size, length, flow, distances):
    new_population = list()
    for x in range(0, population_size):
        cost = fitness(population[x][1], length, flow, distances)
        # dolaczamy koszt na poczatek danej populacji - by nie potwarzac procesu
        new_population.append([cost, population[x][1]])
    return new_population


# Krzyzowanie - na podstawie pradopodobienstwa krzyzowania dokonujemy standardowego przestawienia genow
# dla wczesniej wybranych losowo
# okreslajac punkt ciecia w sposob pseudolosowym przed przypisaniem zmian naprawaimy geny
def crossover(population, px, population_size, length):
    pairs = list()
    for x in range(0, int(population_size / 2)):
        parent1 = int(random.random() * population_size)
        parent2 = int(random.random() * population_size)
        probability = random.random()
        pairs.append([probability, parent1, parent2])
    for pair in pairs:
        if pair[0] > px:
            continue
        index = int(random.random() * (length - 2) + 1)
        population[pair[1]][1] = repair(population[pair[1]][1][:index] + population[pair[2]][1][index:], length)
        population[pair[2]][1] = repair(population[pair[2]][1][:index] + population[pair[1]][1][index:], length)
    return population


# naprawiamy uszkodzone geny poprzez sprawdzenie powtorzen i oznaczenie ich
# a nastepnie dodanie nieuzywanych jeszcze liczb
def repair(permutation, length):
    used = list()
    for x in range(0, length):
        if permutation[x] in used:
            permutation[x] = -1
            continue
        used.append(permutation[x])
    not_used = list()
    for x in range(0, length):
        if x not in used:
            not_used.append(x)
    not_used_index = 0
    for x in range(0, length):
        if permutation[x] == -1:
            permutation[x] = not_used[not_used_index]
            not_used_index += 1
    return permutation


# Mutacja - poprzez zamiane miejscami polega na wylosowaniu 2 roznych genow (2 roznych liczb w wektorze)
# oraz zamianie ich miejscami.
def mutation(population, Pm, population_size, length):
    for x in range(0, population_size):
        prob = random.random()
        if prob > Pm:
            continue
        indexes = random.sample(range(0, length), 2)
        temp = population[x][1][indexes[0]]
        population[x][1][indexes[0]] = population[x][1][indexes[1]]
        population[x][1][indexes[1]] = temp
    return population

# TESTY
print("population_size, gen, Px, Pm, Tour, repeats_range | roulette")
print("{}, {}, {}, {}, {}, {}".format(population_size, gen, Px, Pm, Tour, repeats_range))
print("Uruchomienie, Generacja, Najlepszy, Średni, Najgorszy")

for x in range(0, repeats_range):
    population = generate_first_pop(population_size, length)
    population = evaluation(population, population_size, length, flow, distances)
    # Glowna petla programu - odpowiada za:
    # utworzenie wymaganej liczby pokolen, krzyzowanie, mutacje,
    # wyliczanie kosztu dla kazdej populacji
    # okresla kolejnosc wykonywania operacji
    for x2 in range(0, gen):
        population = tournament_selection(population, Tour)
        # population = roulette_selection(population, population_size)
        population = crossover(population, Px, population_size, length)
        population = mutation(population, Pm, population_size, length)
        population = evaluation(population, population_size, length, flow, distances)

        # sortowanie tak by otrzymac najlepsza populacje (z najmniejszym kosztem)
        sort_population = sort(population)
        sum = 0
        for perm in sort_population:
            sum += perm[0]
        mean = int(sum / population_size)
        print("{}, {}, {}, {}, {}".format(x, x2, sort_population[0][0], mean, sort_population[population_size - 1][0]))
        best = sort_population[0]
        worst = sort_population[population_size - 1]
    global_best += best[0]
    global_worst += worst[0]
    global_mean += mean

global_mean = global_mean / repeats_range
global_worst = global_worst / repeats_range
global_best = global_best / repeats_range
print("{}, {}, {}".format(global_best, global_mean, global_worst))
print("\t".join([str(s + 1) for s in best[1]]))
print()
print("Wynik algorytmu: " + str(best[0]))
print("Czas wykonania: ")
print((time.time() - start_time))
