# Weight finite automata 

TODO description

## Installation

TODO...

## Usage

TODO...

## Example




TODO

Grafik der Testautomaten für dieses Beispiel.....
```python   

    # Setting the alphabet.
    FiniteAutomata.set_alphabet({'a', 'b'})

    # Create a solution object.
    sol = FiniteAutomata({0}, [(0, 'a', 2), (0, 'b', 0), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2), (3, 'b', 1), (1, 'b', 0)], {0, 1, 2, 3})

    # Determine the parameters. x is the proportion of the weight to be allocated to the constant part.
    x = 0.5
    eta = sol.get_length_longest_run() + 1
    lam = (1-x)**(1/eta)

    # Loading of different finite automata over the same alphabet.
    a_1 = FiniteAutomata({0}, [(0, 'b', 0), (0, 'a', 3), (3, 'a', 3), (3, 'b', 2), (2, 'a', 3), (2, 'b', 1), (1, 'a', 4), (1, 'b', 1), (1, 'b', 3)], {1, 2, 3})
    a_2 = FiniteAutomata({0}, [(0, 'a', 0), (0, 'b', 2), (2, 'a', 0), (2, 'b', 1), (1, 'b', 2), (1, 'a', 3)], {0, 1, 2})

    # Determine the weight of the symmetrical difference and then print the result.
    print(f'Automata 1 diff. to Solution = {weight_diff(sol, a_1, eta, lam)[2]}')
    print(f'Automata 2 diff. to Solution = {weight_diff(sol, a_2, eta, lam)[2]}')

```

Console Output: 
```
Automata 1 diff. to Solution = 0.05534231111710203
Automata 2 diff. to Solution = 0.145111985762509
```
## Project structure
- [Example.py](https://syre.fm.cs.uni-kassel.de/mherwig/weight-of-finite-automata/-/blob/main/Example.py)

  This file contains some examples of computations of the weights of regular languages represented by a finite automaton. Thus, the file should help to get an understanding of the application of weighting and to clarify the usage with some examples.  

- [FiniteAutomata.py](https://syre.fm.cs.uni-kassel.de/mherwig/weight-of-finite-automata/-/blob/main/FiniteAutomata.py)

  Finite automata can be used to create finite automata objects on which various operations such as minimization, determinization, complement formation, determination of the symmetric difference and many more can be performed. 

- [WeightFiniteAutomata.py](https://syre.fm.cs.uni-kassel.de/mherwig/weight-of-finite-automata/-/blob/main/WeightFiniteAutomata.py)

  This class can be used to calculate the weight of a FiniteAutomata object and the weight of the difference between two FiniteAutomata objects.

## Authors

Research group "[Theoretical Computer Science / Formal Methods](https://www.uni-kassel.de/eecs/fmv/ueber-uns)" of the University of Kassel.

- [Martin Lange](https://www.uni-kassel.de/eecs/fmv/team/detailansicht?tx_ukpersons_personfunctiondetail%5BpersonFunction%5D=105&cHash=d4aafd324e09a6f60e57566642936ee3)
- [Florian Bruse](https://www.uni-kassel.de/eecs/fmv/team/detailansicht?tx_ukpersons_personfunctiondetail%5BpersonFunction%5D=107&cHash=13125e24f465be73259db38fd7f9891e)
- [Maurice Herwig](https://www.uni-kassel.de/eecs/fmv/team/detailansicht?tx_ukpersons_personfunctiondetail%5BpersonFunction%5D=497&cHash=1c737081a13775b82036f707dc667f39)



## License
TODO...