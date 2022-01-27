from FiniteAutomata import FiniteAutomata
from collections import defaultdict
import numpy as np

def weight_diff(fa_a, fa_b, eta, lam):
    sym_diff = fa_a.symetrical_difference(fa_b)

    if not sym_diff[0].is_empty():
        weight_a_sub_b = weight(sym_diff[0], eta, lam)
    else:
       weight_a_sub_b = 0

    if not sym_diff[1].is_empty():
        weight_b_sub_a = weight(sym_diff[1], eta, lam)
    else:
       weight_b_sub_a = 0

    return weight_a_sub_b, weight_b_sub_a, (weight_a_sub_b + weight_b_sub_a)

def weight(dfa, eta, lam):
    weight = __explicit_solution(dfa, lam) 
    weight += __weight_with_matrix(dfa, eta, lam) 
    weight -= __weight_with_matrix(dfa, 0, lam, eta + 1) 

    return weight
    
def __explicit_solution(dfa, lam):
    w_one_trans = lam/len(FiniteAutomata.get_alphabet()) 
    LGS = []    #todo englischen Namen f�r LGS und klein schreiben
    sol_vec = []

    for q in range(dfa.get_number_of_states()):
        #bestimmung der linken seite des LGS
        slice = []
        number_of_letters = defaultdict(int)
        for (p,_ ) in dfa.get_all_succesors_with_letter(q):
            number_of_letters[p] += 1

        for p in range(dfa.get_number_of_states()):
            if p == q:
                slice.append(number_of_letters[p] * w_one_trans -1)
            else:
                slice.append(number_of_letters[p] * w_one_trans)

        LGS.append(slice)
            
        #bestimmung der rechten seite des LGS
        if q in dfa.get_finals():
            sol_vec.append(- (1 - lam))
        else:
            sol_vec.append(0)

    #l�sen des Gleichungsystem
    LGS = np.array(LGS)
    sol_vec = np.array(sol_vec)
    res = np.linalg.solve(LGS, sol_vec)

    #R�ckgabe des wertes des einzeigen Startzustandes
    #todo �berpr�fen ob wirklich der kleinste
    return res[min(dfa.get_initials())]

def __weight_with_matrix(dfa, constans_part, decay_rate, x = 0): 
    # bestimmt Gewicht eines DFAs mittels der matrizen Methode
    # constans_part (in Ausarbeitung eta) ist der Wert bis zu dem die wörter konstant bewertet werden.
    # x gibt an bis zur welcher Wortlänge im exponentiellen Teil bestimmt werden soll. Default x = 0, damit wird der exponentiell zefallende Teil nicht berechnet
    matrix = Matrix(dfa)
    size_of_alpabet = len(FiniteAutomata.get_alphabet())
    weight = 0
    weight_ex_part = 0

    #Anzahl der Wörter die maximal im konstanten Teil liegen
    max_words_in_constans_part = (1-size_of_alpabet**(constans_part + 1))/(1-size_of_alpabet)
    
    #Anteil des konstanten teils
    sum_weigt_constans_part = 1 - decay_rate**(constans_part + 1)
   
   #gewicht eines einzelen wortes im konstanten teil
    weigth_of_one_word_c_p = sum_weigt_constans_part/max_words_in_constans_part

    #überprüfen auf leeres Wort
    if not dfa.get_initials().isdisjoint(dfa.get_finals()):
        weight += weigth_of_one_word_c_p

    #konstanter teil
    for i in range(1, constans_part+1):
        words_of_this_lenght = round(matrix.get_share(i) * (size_of_alpabet**i))
        weight += weigth_of_one_word_c_p * words_of_this_lenght
    
    #exponentiell zerfallender Teil
    for i in range(constans_part+1,  x):
        weight_ex_part += matrix.get_share(i)  * (decay_rate**(i+1))

    #gewicht durch den Grenzwert der Summe teilen (Geometrische Reihe)
    weight_ex_part = weight_ex_part * ((1-decay_rate)/(decay_rate))
    
    #beide gewichte zusammenrechnen
    weight += weight_ex_part
    return weight


class Matrix:
	
	def __init__(self, Nfa):
		#Konstruktor
		self.nfa = Nfa
		self.dimension = Nfa.get_number_of_states()
		self.size_of_alpabet = len(FiniteAutomata.get_alphabet())
		self.matrixs = {}
		self.__initial_matrix()


	def __initial_matrix(self):
		#erstellen der initialen Matrix 
		matrix = []
		for i in range(self.dimension):
			number_of_letters = defaultdict(int)
			this_dimension = []

			for (j, _) in self.nfa.get_all_succesors_with_letter(i):
				number_of_letters[j] +=1

			for j in range(self.dimension):
				this_dimension.append(number_of_letters[j]/self.size_of_alpabet)

			matrix.append(this_dimension)
		self.matrixs[1] = np.array(matrix)


	def get_matrix(self, i):
		#Gibt die Maxtrix für eine bestimmte Wortlänge zurück
		if i in self.matrixs.keys():
			return self.matrixs[i]

		elif i-1 in self.matrixs.keys():
			before = self.matrixs[i-1]
			first = self.matrixs[1]
			
			new_matrix = np.matmul(before, first)
			self.matrixs[i] = new_matrix
			return new_matrix

		else:
			#könnte man auch noch in durch die 2-adische Zerlegung bestimmen. Aktuell aber noch nicht nötig. Da dieser Zweig aktuell nie betreten wird.
			self.get_matrix(i-1)
			

	def get_share(self, i):
		#gibt den Anteil der Wörter zu Worlänge i die durch die Sprache akzeptiert werden zu allen möglichen Wörtern zu dieser Wortlänge
		if i < 1:
			return 0
		
		matrix = self.get_matrix(i)
		share = 0

		for initial in self.nfa.get_initials():
			for final in self.nfa.get_finals():
				share += matrix[initial][final]

		return share
	