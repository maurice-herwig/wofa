from FiniteAutomata import FiniteAutomata
from WeightFiniteAutomata import weight_diff, weight

FiniteAutomata.set_alphabet({'a', 'b'})
#todo ordentliche Beispiel automaten heraussuchen....


fa_0 = FiniteAutomata({0},[(0, 'a',1)], {1})
print(fa_0)
fa_1 = FiniteAutomata({0},[(0, 'a',1),(1, 'a',0)], {1})
print(fa_1)

res = fa_0.symetrical_difference(fa_1)
print(res[0])
print(res[1])

eta = fa_0.get_length_of_longest_run() + 1
lam = (1-0.5)**(1/eta)

print(weight(fa_0, eta, lam))
print(weight(fa_1, eta, lam))
print(weight_diff(fa_0, fa_1, eta, 0.9))
