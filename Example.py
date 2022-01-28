from FiniteAutomata import FiniteAutomata
from WeightFiniteAutomata import weight_diff, weight

FiniteAutomata.set_alphabet({'a', 'b'})
#TODO ordentliche Beispiel automaten heraussuchen....


fa_0 = FiniteAutomata({0},[(0, 'a',1)], {1})
print(fa_0)
fa_1 = FiniteAutomata({0},[(0, 'a',1),(1, 'a',0)], {1})
print(fa_1)

print()
res = fa_0.symetrical_difference(fa_1)
print(res[0])
print(res[1])

eta = fa_0.get_length_longest_run() + 1
lam = (1-0.5)**(1/eta)

print(weight(fa_0, eta, lam))
print(weight(fa_1, eta, lam))
print(weight_diff(fa_0, fa_1, eta, lam))



fa_emp = FiniteAutomata.empty_nfa()
print(fa_emp)
print(weight(fa_emp, eta, lam))

fa_full = FiniteAutomata.full_nfa()
print(fa_full)
print(weight(fa_full, eta, lam))

print(weight_diff(fa_emp, fa_full, eta, lam))


