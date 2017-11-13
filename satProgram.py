import random
import glob
import os
from timeit import default_timer as timer
import matplotlib.pyplot as plot
import numpy as np

# Creates population of random solutions based on size of variables and
# mates population by 20% and adds children, then mutates 3% of the population
# to potentially reach solution faster and eliminates population by certain
# percentage based on its current size
def genAlg(var, arr):

	# initialize variables
	wipeout = var * 50
	cost = []
	pop = []
	nums = range(-1, 0) + range(1, 2)
	best = 0

	# initial population creation
	for i in range(0, var * 10):

		sol = []

		for j in range(1, var + 1):

			rand = random.choice(nums)
			sol.append(j * (rand * -1))

		pop.append(sol)

	# generations
	for k in range(0, 10):

		cost = []

		# get mating percentage (20%)
		repopCount = int(len(pop) * .2)

		# mate population
		for l in range(0, repopCount):

			# pick two random parents
			p1 = random.choice(pop)
			p2 = random.choice(pop)

			pos = random.randint(0, len(p1))

			# create children based on random position
			c1 = p1[:pos] + p2[pos:]
			c2 = p2[:pos] + p1[pos:]

			# add children to population
			pop.append(c1)
			pop.append(c2)

		# get mutation percentage (3%)
		mutateCount = int(len(pop) * .03)

		for m in range(0, mutateCount):

			# pick individual to mutate
			mutateP = random.choice(pop)

			# pick random variable to change
			mutatePos = random.randint(0, len(mutateP) - 1)

			# flip random variable
			mutateP[mutatePos] = mutateP[mutatePos] * -1

		# check cost/solution
		for n in range(0, len(pop)):

			answer = True
			satisfied = []

			# check entire array for each member of population
			for o in range(0, len(arr)):

				if(arr[o][0] != pop[n][abs(arr[o][0]) - 1]):

		 			if(arr[o][1] != pop[n][abs(arr[o][1]) - 1]):

		 				if(arr[o][2] != pop[n][abs(arr[o][2]) - 1]):

		 					answer = False

		 				else:

		 					satisfied.append(arr[o])
		 			else:

		 				satisfied.append(arr[o])
		 		else:

		 			satisfied.append(arr[o])

		 	# if solution is found return it
		 	if(answer):

		 		#print "found satisfiable solution", pop[n]
				return -1

			# if no solution append total cost to list parallel with pop
		 	cost.append(len(satisfied))

		# eliminate population
		if len(pop) > wipeout:

			# if pop gets too high keep top 20%
			wipePercent = int(len(pop) * .8)

		else:

			# regularly keep top 80% of pop
			wipePercent = int(len(pop) * .2)

		# go through pop and eliminate weakest pop costs
		for p in range(0, wipePercent):

			index = cost.index(min(cost))
			pop.pop(index)
			cost.pop(index)

	# no solution was found return best solution
	best = max(cost)
	return best

# generates a random solution and tests its validity, if not satisfiable
# it will either pick a random value to flip or pick the best one based on
# its level of presence within the unsatisfied clauses
def walkSAT(arr, prob, flips, var):

	# initialize values
	pres = [0] * var
	answer = True
	nums = range(-1, 0) + range(1, 2)
	sol = []
	best = 0

	# Get random array of possible satisfying variables
	for j in range(1, var + 1):

		rand = random.choice(nums)
		sol.append(j * (rand * -1))

	# flip values for entire flip count and see if flip satisfies problem
	for k in range(0, flips):

		answer = True
		satisfied = []
		errArr = []

		# check satisfiability of solution generated
		for l in range(0, len(arr)):

			if(arr[l][0] != sol[abs(arr[l][0]) - 1]):

	 			if(arr[l][1] != sol[abs(arr[l][1]) - 1]):

	 				if(arr[l][2] != sol[abs(arr[l][2]) - 1]):

	 					answer = False
	 					errArr.append(arr[l])

	 				else:

	 					satisfied.append(arr[l])
	 			else:

	 				satisfied.append(arr[l])
	 		else:

	 			satisfied.append(arr[l])

		# if answer is found return it
		if(answer):

			#print "found satisfiable solution", sol
			return -1	

		# save the most satisfiable solution so far
		if len(satisfied) > best:
		
			best = len(satisfied)

 		clause = random.choice(errArr)
 		rand = random.randint(0, 1)

 		# based on probability pick a random value to flip
 		if rand == 0:

 			flip = abs(random.choice(clause))
 			sol[flip - 1] = (-1 * sol[flip - 1])

 		# else find the best value to flip
 		else:

 			pres = [0] * var

 			for k in range(0, len(errArr)):

	 			pres[abs(errArr[k][0]) - 1] += 1
	 			pres[abs(errArr[k][1]) - 1] += 1
	 			pres[abs(errArr[k][2]) - 1] += 1

			flip = pres.index(max(pres)) + 1

			sol[flip - 1] = (-1 * sol[flip - 1])	

	return best	

# generates a random solution and tests its validity, if not satisfiable
# it picks a random value to flip and checks the satisfiability of that
# solution. If the value returned is higher than the original, the random
# array generated is saved and used in the next iteration
def simAnnealing(arr, var):

	neighbor = []
	nums = range(-1, 0) + range(1, 2)
	best = 0

	# try new random answer a certain amount of times
	for i in range(0, var):

		sol = []

		# Get random array of possible satisfying variables
		for j in range(1, var + 1):

			rand = random.choice(nums)
			sol.append(j * (rand * -1))

		# test random solutions a certain amount of times
		for k in range(0, var):

			answer = True
			sat1 = []
			sat2 = []

			# check satisfiability of solution generated
			for l in range(0, len(arr)):

				if(arr[l][0] != sol[abs(arr[l][0]) - 1]):

		 			if(arr[l][1] != sol[abs(arr[l][1]) - 1]):

		 				if(arr[l][2] != sol[abs(arr[l][2]) - 1]):

		 					answer = False

		 				else:

		 					sat1.append(arr[l])
		 			else:

		 				sat1.append(arr[l])
		 		else:

		 			sat1.append(arr[l])

			# if answer is found return it
			if(answer):

				#print "found satisfiable solution", sol
				return -1

			# flip variable at random
			else:

				answer = True

				neighbor = sol

				flip = abs(random.choice(neighbor))
 				neighbor[flip - 1] = (-1 * neighbor[flip - 1])

 				# check satisfiability of neighbor generated
				for m in range(0, len(arr)):

					if(arr[m][0] != neighbor[abs(arr[m][0]) - 1]):

			 			if(arr[m][1] != neighbor[abs(arr[m][1]) - 1]):

			 				if(arr[m][2] != neighbor[abs(arr[m][2]) - 1]):

			 					answer = False

		 					else:

		 						sat2.append(arr[m])
		 				else:

		 					sat2.append(arr[m])
		 			else:

		 				sat2.append(arr[m])

		 		# if neighbor is the answer return it
		 		if(answer):

		 			#print "found satisfiable solution", sol
					return -1

				# if neighbor is better save it and save the value as best
				if len(sat2) > len(sat1):

					sol = neighbor
					best = len(sat2)
	return best

# parses a file given and gets the header of the file and returns the
# lines of data as a list for future usage
def parser(file):

	print file

	with open(file) as f:

		content = f.readlines()

	# clean content and get header
	content = [x.strip('\n') for x in content]

	val = content[0].split()
	content = content[:int(val[3]) + 1]
	i = 0

	for x in content:

		if x[0] is "p":
  
			i += 1
			continue

		else:

			x = x.strip(' 0')
			x = [int(j) for j in x.split()]

			content[i] = x
			i += 1

	# return properly sanitized list with header
	return content

# plots the results from the running of the algorithm entered by the user
def plotResults(points, formulas, title, label):

	yPos = np.arange(len(formulas))

	plot.bar(yPos, points, align = 'center')
	plot.xticks(yPos, formulas)
	plot.ylabel(label)
	plot.title(title)
	plot.show()

def main():

	algsList = []
	averages = []
	times = []

	alg = int(raw_input("Enter number for algorithm to run: 1. Genetic Algorithm 2. Simulated Annealing 3. WalkSAT: "))
	directory = raw_input("Enter directory you would like to test: ")

	if directory == "tests" or directory == "3cnf_100atoms":

		os.chdir(directory)

		# go through each file in directory
		for l in glob.glob("*.cnf"):

			algsList.append(l)

			results = parser(l)
			ret = 0
			total = 0
			average = 0
			time = 0
			timeAv = 0
			timeTot = 0

			head = results[0].split()
			variables = int(head[2])
			clauses = int(head[3])

			# run algorithm based on user input
			if alg == 1:

				title = "Genetic Algorithm"

				for i in range(0, 10):

					start = timer()
					ret = genAlg(variables, results[1:])
					end = timer()

					time = end - start
					timeTot += time

					if ret != -1:

						#print "best found was ", ret
						total += ret

					else:

						#print clauses
						total += clauses

				average = total / 10
				timeAv = timeTot / 10

				averages.append(average)
				times.append(timeAv)

			elif alg == 2:

				title = "Simulated Annealing"

				for j in range(0, 10):

					start = timer()
					ret = simAnnealing(results[1:], variables)
					end = timer()

					time = end - start
					timeTot += time

					if ret != -1:

						#print "best found was ", ret
						total += ret

					else:

						#print clauses
						total += clauses

				average = total / 10
				timeAv = timeTot / 10

				averages.append(average)
				times.append(timeAv)
			
			elif alg == 3:

				title = "WalkSAT"

				for k in range(0, 10):

					start = timer()
					ret = walkSAT(results[1:], .5, 1000, variables)
					end = timer()

					time = end - start
					timeTot += time

					if ret != -1:

						#print "best found was ", ret
						total += ret

					else:

						#print clauses
						total += clauses

				average = total / 10
				timeAv = timeTot / 10

				averages.append(average)
				times.append(timeAv)

		# plot results
		plotResults(averages, algsList, title, "Satisfied Clauses")
		plotResults(times, algsList, title, "CPU Time")

main()