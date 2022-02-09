from wofa import FiniteAutomata
from wofa import weight_diff, weight

import numpy as np
import matplotlib.pyplot as plt



# Setting the alphabet.
FiniteAutomata.set_alphabet({'a', 'b'})

# laden der Automaten
sol = FiniteAutomata({1}, [(1, 'a', 2), (1, 'b', 1), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2), (3, 'b', 4), (4, 'b', 1)], {1, 2, 3, 4})

automatas = []

# automat1
automatas.append(FiniteAutomata({1}, [(1, 'a', 3), (1, 'b', 2), (2, 'a', 3), (2, 'b', 2), (3, 'a', 3), (3, 'b', 4), (4, 'a', 3), (4, 'b', 5),              (5, 'b', 3)], {1, 2, 3, 4, 5}))
    
# automat2
automatas.append(FiniteAutomata({1}, [(1, 'a', 2), (1, 'b', 2), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2), (3, 'b', 4),              (4, 'b', 5), (5, 'a', 2), (5, 'b', 5)], {1, 2, 3, 4, 5}))
    
# automat3
automatas.append(FiniteAutomata({1}, [(1, 'a', 2), (1, 'b', 1), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2), (3, 'b', 4), (4, 'b', 4), (4, 'b', 2)                          ], {2, 3, 4}))
    
# automat4
automatas.append(FiniteAutomata({1}, [(1, 'a', 1), (1, 'b', 2), (2, 'a', 1), (2, 'b', 3),              (3, 'b', 2)                                                    ], {1, 2, 3}))
    
# automat5
automatas.append(FiniteAutomata({1}, [(1, 'a', 2), (1, 'b', 1), (2, 'a', 1), (2, 'b', 3), (3, 'a', 1), (3, 'b', 4),              (4, 'b', 1)                          ] ,{1}))
    
# automat6
automatas.append(FiniteAutomata({1}, [(1, 'a', 2), (1, 'b', 1), (2, 'a', 2), (2, 'b', 3), (3, 'a', 3), (3, 'b', 4), (4, 'a', 5), (4, 'b', 4), (5, 'a', 5), (5, 'b', 5)], {5}))
   

# Anzahl der Werte pro Dimension
num_val = 10
max_eta = 10

# defnieren der Werte
etas = np.array([int(i) for i in np.linspace(0, max_eta, num_val)])
lams = np.linspace(0.5, 1, num_val + 1)[:num_val]

X, Y = np.meshgrid(etas, lams)


fig = plt.figure()

ax = plt.axes(projection ='3d')
ax.set_xlabel("eta")
ax.set_ylabel("lambda")
ax.set_zlabel('weight')





res = []
for automata in automatas: 
    res_i = []
    for eta in etas:
        r = []
    
        for lam in lams:
            #r.append(weight(sol, eta, lam))
            r.append(weight_diff(sol, automata, eta, lam)[2])
        res_i.append(r)
    res.append(res_i)

Z = np.array(res[0])
ax.plot_surface(X, Y, Z, cmap ='Greys', edgecolor ='grey')

Z = np.array(res[1])
ax.plot_surface(X, Y, Z, cmap ='Purples', edgecolor ='purple')

Z = np.array(res[2])
ax.plot_surface(X, Y, Z, cmap ='Greens', edgecolor ='green')

Z = np.array(res[3])
ax.plot_surface(X, Y, Z, cmap ='Oranges', edgecolor ='orange')

Z = np.array(res[4])
ax.plot_surface(X, Y, Z, cmap ='BuPu', edgecolor ='blue')

Z = np.array(res[5])
ax.plot_surface(X, Y, Z, cmap ='BuGn', edgecolor ='green')



# hinzufügen der ursrünglichen Werts
x = 0.5
eta = sol.get_length_longest_run() + 1
lam = (1-x)**(1/eta)


X = np.array([eta  for _ in range(2)])
Y = np.array([lam  for _ in range(2)])
Z = np.linspace(0,1,2)


ax.plot3D(X, Y, Z, 'red')


# anzeigen des Plots
plt.show()
