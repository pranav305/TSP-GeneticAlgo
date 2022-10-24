import random as rand
import numpy as np
import matplotlib.pyplot as plt

init_size = 100   # Generation Size
m_rate = 0.4    #Mutation Rate
max_gens = 1000
gen_nums = 0
trunc_cutoff = 0.2

cities = [
	(1, 1), # INITIAL CITY, HAS TO BE FIRST AND LAST
	(30, 3),
	(51, 57),
	(22, 17),
	(24, 42),
	(54, 10),
	(24, 36),
	(19, 25),
	(13, 47),
	(48, 49),
	(21, 19),
	(5, 58),
	(27, 30),
	(3, 41),
	(25, 16),
	(44, 42),
	(38, 45),
	(39, 15),
	(17, 10),
	(12, 46),
	(30, 8),
	(20, 4),
	(22, 42),
	(4, 22),
	(51, 7),
	(35, 16),
	(43, 8),
	(9, 9),
	(13, 37),
	(2, 60),
	(39, 18),
	(1, 1)
]

class DNA:
	def __init__(self, size = len(cities), chromo = []):
		self.chromo = chromo
		self.size = size
		self.elite = False

	def reset(self):
		self.chromo = []

	def calc_fitness(self):
		distance = 0
		for n in range(len(self.chromo)-1):
			distance += np.sqrt( (self.chromo[n][0] - self.chromo[n+1][0])**2 + (self.chromo[n][1] - self.chromo[n+1][1])**2)
		# self.fitness = ( (1/distance) * (1/(distance/len(self.chromo))) ) * 10**6
		self.fitness = 1/distance
		return self.fitness
	
	def random_init(self):
		self.reset()
		shuffled = cities[1:-1]
		rand.shuffle(shuffled)
		self.chromo.append(tuple((1,1)))
		self.chromo.extend(shuffled)
		self.chromo.append(tuple((1,1)))
		
	
	def mutate(self, rate):
		if rand.randrange(1) < rate:
			s1 = rand.randint(1,len(self.chromo) -2)
			s2 = rand.randint(1,len(self.chromo) -2)
			#! SWAP TWO CITIES !#
			self.chromo[s1], self.chromo[s2] = self.chromo[s2], self.chromo[s1]
		if rand.randrange(1) < rate:
			#! REVERSE ORDER OF A SLICE !#
			slice = self.chromo[s1:s2]
			self.chromo[s1:s2] == slice[::-1]
			


class Population:
	def __init__(self, size = init_size, generation = []):
		self.size = size
		self.generation = generation

	def select(self):
		pool = sorted(self.generation, key=lambda x: x.calc_fitness(), reverse=True)
		return rand.choices(
			population=pool[:int(trunc_cutoff*len(pool))],
			k=2
		)

	def best(self):
		highest = -1
		which = None
		for i in self.generation:
			i.calc_fitness()
			if i.fitness > highest:
				highest = i.fitness
				which = i
				i.elite = True
			else:
				continue
		return highest, which

	def random_population(self):
		for i in range(self.size):
			myDNA = DNA()
			myDNA.random_init()
			self.generation.append(myDNA)

def splitXY(data):
	x = []
	y = []
	for i in data:
		x.append(i[0])
	
	for i in data:
		y.append(i[1])

	return x,y

def crossover(a, b):
	point_a = rand.randint(1,len(a.chromo)-2)
	point_b = rand.randint(point_a,len(a.chromo)-1)
	offspring_ab = []
	offspring_ba = []
	a_slice = a.chromo[point_a:point_b]
	b_slice = b.chromo[point_a:point_b]
	
	while len(offspring_ab) != len(a.chromo)-len(a_slice):
		for i in a.chromo:
			if i not in b_slice:
				offspring_ab.append(i)
	
	while len(offspring_ba) != len(b.chromo)-len(b_slice):
		for i in b.chromo:
			if i not in a_slice:
				offspring_ba.append(i)
		
	offspring_ab[point_a:point_a] = b_slice
	offspring_ba[point_a:point_a] = a_slice

	return (offspring_ab, offspring_ba)


myPop = Population(init_size)
myPop.random_population()

while gen_nums != max_gens:
	new_gen = []
	for i in range(int(init_size/2)):
		p1, p2 = myPop.select()
		oa, ob = crossover(p1,p2)
		oa = DNA(chromo=oa)
		ob = DNA(chromo=ob)  
		new_gen.extend((oa,ob))
	
	myPop.generation = [i for i in new_gen]
	for i in range(len(myPop.generation)):
		myPop.generation[i].calc_fitness()
	
	x, y = myPop.best()
	y = y.chromo
	
	for i in myPop.generation:
		if not i.elite:
			i.mutate(m_rate)
	
	gen_nums += 1
	
	a,b = splitXY(y)
	plt.plot(a,b, 'b--')
	plt.scatter(a,b, color='red')
	plt.title(f"Generation: {gen_nums}")
	plt.draw()
	# plt.savefig(f'gif/gen{gen_nums}.png')
	plt.pause(0.001)
	plt.clf()
	
	print(f"{str(gen_nums)} \t {str(x)}")