import ast, sys, math

class prettyfloat(float):
    def __repr__(self):
        return "%0.2f" % self

def map(f, it):
    result = []
    for x in it:
        result.append(f(x))
    return result

infeasible = 'Status: inviavel'
unbounded = 'Status: ilimitado'
optimal = 'Status: otimo'
linerules = 4 #linha que inicia as restrições

#SOLUTIONS
def solution(tableau, lines, columns):
	var_solution = [0 for _ in range(0,columns)]
	for i in range(1, len(tableau)):
		for j in range(0, columns):
			if(tableau[i][j] == 1):
				for k in range(0, len(tableau)):
					if tableau[k][j] == 0:
						#print ('basica na posição', j, tableau[i][-1])
						var_solution[j] = round(tableau[i][-1],3)
						print (var_solution)
						break
	return (var_solution)

def solution_unbounded(tableau, ratio, columns, index_column):
	if (ratio == math.inf):
		cert = [0 for _ in range(0, len(tableau[0])-1)] 
		for i in range(1, len(tableau)):
				for j in range(0, len(tableau[0])-1):
					if tableau[i][j] == 1:
						for k in range(0, len(tableau)):
							if tableau[k][j] != 0:
								if tableau[i][index_column] == 0: 
									cert[j] = round((tableau[i][index_column]),5)
								elif tableau[i][index_column] > 0 or tableau[i][index_column] < 0: 
									cert[j] = (-1)*round((tableau[i][index_column]),5)
							cert[index_column] = 1 
					elif tableau[i][index_column] > 0 or tableau[i][index_column] < 0:
						continue
					break
		output_2 = [unbounded,cert]
		print(output_2)
		with open("output.txt","w") as file_2:
			file_2.write('\n'.join(map(str, output_2)))


def solution_infeasible(tableau, _aux):
	for i in range(1, len(tableau)):
		for j in range(0, len(tableau[0])):
			if (tableau[i][j] <= 0):
				break
			if (j == len(tableau[0]) - 1):
				if (tableau[i][j] < 0):
					out_aux = map(prettyfloat, _aux[i])
	output_1 = [infeasible,out_aux]
	print(output_1)
	with open("out.txt","w") as file_1:
		file_1.write('\n'.join(map(str, output_1)))

#PIVOTS
def primal_pivot(tableau, _aux, lines, columns, index_column):
	ratio = math.inf
	index_line = math.inf
	#lower ratio
	for i in range(1, len(tableau)):
		if (tableau[i][index_column] != 0):
			curr = tableau[i][-1] / tableau[i][index_column]
			if (curr < ratio and curr > 0):
				ratio = curr
				index_line = i

	solution_unbounded(tableau, ratio, columns, index_column)

	denominator = tableau[index_line][index_column]
	#divides the line by the temporary value of a divisor calculated above
	for i in range(0, len(tableau[0])):
		tableau[index_line][i] /= denominator
	for i in range(0, lines):
		_aux[index_line][i] /= denominator
	
	change_tableau(tableau, _aux,index_line,index_column)

def dual_pivot(tableau, _aux, lines, index_line):
	ratio = math.inf
	index_column = math.inf

	#lower column ratio
	for i in range(0, len(tableau[0])):
		if (tableau[index_line][i] != 0):
			curr = (tableau[0][i] / (tableau[index_line][i]) * (-1))
			#print (tableau[0][i], tableau[index_line][i]*(-1), curr)
			if (curr < ratio and curr > 0):
				ratio = curr
				index_column = i
	
	solution_infeasible(tableau, _aux)
    
	denominator = tableau[index_line][index_column]
	for i in range(0, len(tableau[0])):
		tableau[index_line][i] /= denominator
	for i in range(0, lines):
		_aux[index_line][i] /= denominator
	change_tableau(tableau, _aux, index_line, index_column)

#OPERATIONS
def matrix_ope(matrix, lines, columns):
	#matrix operations empty 
	_aux = [[] for i in range(len(matrix))]
	for i in range(0, lines):
		#zeros in c
		_aux[0].append(0)
	for i in range(1, len(matrix)):
		for j in range(1, len(matrix)):
			#matrix id 
			if j == i:
				_aux[i].append(1)
			else:
				_aux[i].append(0)
	return _aux

def change_tableau(tableau, _aux, index_line, index_column):
    for i in range (0, len(tableau)):
        temp = tableau[i][index_column]
        if temp != 0 and i != index_line:
            for j in range(0,len(tableau[0])):
                tableau[i][j] -= temp*tableau[index_line][j]
            for j in range(0, len(tableau)-1):
                _aux[i][j] -= temp * _aux[index_line][j]
