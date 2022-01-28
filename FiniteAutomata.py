class FiniteAutomata:
    """ Finite Automata is a class to create objects from NFAs and DFAs. On which various operations implemented below can be performed.
    """
    # Classes variables
    alphabet = set()
    SIMUEQ = 0
    BISIMU = 1
    minimization_engine = SIMUEQ

    """ =======================================================================================================================
        Getter and setter methods for the class variables. 
        =======================================================================================================================
    """
    @classmethod
    def set_minimization_engine(cls,engine):
        """ Set the method that can be used to minimize a finite automata object. Currently BISIMU and SIMUEQ can be used.

        Args:
            engine (string): SIMUEQ or BISIMU
        """
        FiniteAutomata.minimization_engine = engine

    @classmethod
    def set_alphabet(cls,sigma):
        """ Set the alphabet which uses finite automata. 
        !!!Important this is a class variable and not an object variable. Therefore, special care must be taken when using automata 
        with different alphabets. It is also not useful to set this class variable to the union of the alphabets of all automata.
        Since this leads with the computation of the weighting to wrong results, because thereby the quantity of the maximum possible words 
        increases clearly.

        Args:
            sigma (set() of strings): The alphabet of finite automata.
        """
        FiniteAutomata.alphabet = sigma

    @classmethod
    def get_alphabet(cls):
        """ Returns the set of all alphabet letters. 

        Returns:
            set() of strings: Set of alphabet letters.
        """
        return FiniteAutomata.alphabet

    """ =======================================================================================================================
        Methods for creating some simple example automata.
        =======================================================================================================================
    """
    @classmethod
    def one_symbol_nfa(cls,a):
        """ Create a finite automaton object that accepts only the exact word of length 1 that reads the letter a. 

        Args:
            a (char): letter

        Returns:
            FiniteAutomat: Finite automaton object.
        """
        return cls({0},[(0,a,1)],{1})

    @classmethod
    def univ_symbol_nfa(cls):
        """ Create a finite automaton object that describes the language that describes all words of length 1 over the given alphabet (FiniteAutomat.alphabet).

        Returns:
            FiniteAutomat: Finite automaton object.
        """
        transitions = [(0,a,1) for a in cls.alphabet]
        return cls({0},transitions,{1})

    @classmethod
    def empty_nfa(cls):
        """ Create a finite automaton object that describes the empty language.

        Returns:
            FiniteAutomat: Finite automaton object.
        """
        return cls({0},[],set())

    @classmethod
    def full_nfa(cls):
        """ Creates a finite automaton object of the full language over the given alphabet (FiniteAutomat.alphabet).

        Returns:
            FiniteAutomat: Finite automaton object.
        """
        transitions = [(0,a,0) for a in cls.alphabet]
        return cls({0}, transitions, {0})

    """ =======================================================================================================================
        Object methods.
        =======================================================================================================================
    """
    def __init__(self, initials, transitions, finals):
        """ Constructor of the FiniteAutomata class.

        Args:
            initials (set() of integers):                   Set of initial states of the finite automaton.
            transitions (list of tupels(int, char, int)):   List with tuples of all transitions between two states. The tuples have 
                                                            the form (q, a, p) and describe by reading the letter a the automaton goes from the 
                                                            state q to the state p.
            finals ([type]):                                Set of finial states of the finite automaton.
        """
        self.num_states = 0
        self.initials = set()
        self.finals = set()
        self.successors = {}
        self.predecessors = {}

        for p in initials:
            self.__make_initial(p)
        for q in finals:
            self.__make_final(q)
        for (p,a,q) in transitions:
            self.__add_transition(p,a,q)

    """ =======================================================================================================================
        Getter and setter methods for the object variables and some simple methods.
        =======================================================================================================================
    """

    def get_number_of_states(self):
        return self.num_states

    def get_successors(self,s,a):
        if (s,a) in self.successors:
            return self.successors[(s,a)]
        else:
            return set()

    def get_all_successors(self,s):
        return { q for a in self.alphabet for q in self.get_successors(s,a) }

    def get_all_succesors_with_letter(self, p):
        return { (q, a) for a in self.get_alphabet() for q in self.get_successors(p, a) }

    def get_predecessors(self,s,a):
        if (s,a) in self.predecessors:
            return self.predecessors[(s,a)]
        else:
            return set()

    def get_all_predecessors(self, s):
        return { p for a in self.alphabet for p in self.get_predecessors(s, a) }

    def get_initials(self):
        return self.initials

    def get_finals(self):
        return self.finals

    def get_transitions(self):
        return [ (p,a,q) for (p,a), succs in self.successors.items() for q in succs ]

    def __add_state(self,p):
        if p >= self.num_states:
            self.num_states = p+1

    def __clear_states(self):
        self.num_states = 0

    def __add_transition(self,p,a,q):
        self.__add_state(p)
        self.__add_state(q)
        succs = self.get_successors(p,a)
        succs.add(q)
        self.successors[(p,a)] = succs
        preds = self.get_predecessors(q,a)
        preds.add(p)
        self.predecessors[(q,a)] = preds

    def __remove_transition(self,p,a,q):
        succs = self.get_successors(p,a)
        succs.discard(q)
        self.successors[(p,a)] = succs
        preds = self.get_predecessors(q,a)
        preds.discard(p)
        self.predecessors[(q,a)] = preds

    def __clear_transitions(self):
        self.successors = {}
        self.predecessors = {}

    def __make_initial(self,q):
        self.__add_state(q)
        self.initials.add(q)

    def __set_initials(self,qs):
        self.__clear_initials()
        for q in qs:
            self.__make_initial(q)

    def __clear_initials(self):
        self.initials = set()

    def __make_final(self,q):
        self.__add_state(q)
        self.finals.add(q)

    def __make_nonfinal(self,q):
        self.__add_state(q)
        self.finals.discard(q)

    def __set_finals(self,qs):
        self.__clear_finals()
        for q in qs:
            self.__make_final(q)

    def __clear_finals(self):
        self.finals = set()

    def __get_all_states(self):
        states = set()
        for i in range(self.get_number_of_states()):
            states.add(str(i))
        return states  

    def unpack(self):
        return FiniteAutomata.alphabet, set(range(self.get_number_of_states())), self.successors, self.get_initials(), self.get_finals()

    def accepts_empty_word(self):
        """ Determines whether the empty word is in the language described by the machine.

        Returns:
            bool: Is the empty word in the language.
        """
        return self.get_initials().intersection(self.get_finals()) != set()

    def is_empty(self):
        """ Determines whether the language described by the automaton is the empty language.

        Returns:
            bool: Is the language the empty language.
        """
        if len(self.__productives()) == 0:
            return True
        return False

    def __str__(self):
        """ Overwrite the standard console output.
        """
        return(f'alphabet:    {self.get_alphabet()}\n'
          f'states:      {self.__get_all_states()}\n'
          f'starting:    {self.get_initials()}\n'
          f'accepting:   {self.get_finals()}\n'
          f'transitions: {self.get_transitions()}\n')

    def get_length_longest_run(self):
        """ Determines the length of the longest run on the machine without visiting a state twice. 
        This is useful because incrementing this value by 1 in most cases gives the pumping constant of the language of the automaton. 

        Returns:
            int: Length of the longest run.
        """
        
        def next_step(before):
            res = []
            found_one_next = False
       
            for next in self.get_all_successors(before[1]):
                if next in before[0]:
                    res.append(len(before[0]))
                else:
                    found_one_next = True
                    new_set = before[0].copy()
                    new_set.add(next)
                    res.append(next_step((new_set, next)))

            if(not found_one_next):
                return len(before[0])
            return max(res)
        
        list = []
        res = []

        for init in self.get_initials():
            list.append(({init}, init))

        for next in list:
            res.append(next_step(next))

        if res == []:
            return 1
        return max(res)
        
    """ =======================================================================================================================
        Methods for the minimization of finite automata.
        =======================================================================================================================
    """
    def __reachables(self):
        """ Calculates the set of reachable states of the finite automaton.
        Returns:
            set() of integer: Set of reachable states.
        """
        reachables = set()

        todo = list(self.get_initials())
        while todo:
            p = todo.pop(0)
            if not p in reachables:
                reachables.add(p)
                for a in FiniteAutomata.get_alphabet():
                    for q in self.get_successors(p,a):
                        todo.append(q)

        return reachables

    def __productives(self):
        """ Calculates the set of productive states of the finite automaton. 
        A productive state is a state from which at least one run to a final state exists.  

        Returns:
            set() of integer:  Set of productive states.
        """
        productives = set()

        todo = list(self.get_finals())
        while todo:
            q = todo.pop(0)
            if not q in productives:
                productives.add(q)
                for a in FiniteAutomata.get_alphabet():
                    for p in self.get_predecessors(q,a):
                        todo.append(p)
        return productives

    def __shrink_to(self, remaining):
        """ By means of this method, a finite automaton can be shrunk to a given set. Only the transitions between the states to which the 
        automaton is to be reduced are retained. This can be especially helpful when minimizing to the productive states, since this results 
        in smaller and more efficient automata. 

        Args:
            remaining (set() of integer): The set of states to which the finite automaton is to be shrink.

        Returns:
            self: Returns the own object but shrunk to the amount of input states.
        """
        i = 0
        new_names = {}
        for q in remaining:
            new_names[q] = i
            i += 1

        self.__clear_states()

        # reset initial and final states
        ps = self.get_initials()
        self.__clear_initials()
        for p in ps:
            if p in remaining:
                self.__make_initial(new_names[p])

        qs = self.get_finals()
        self.__clear_finals()
        for q in qs:
            if q in remaining:
                self.__make_final(new_names[q])

        # reinsert all transitions between remaining
        transitions = self.get_transitions()
        self.__clear_transitions()
        for (p,a,q) in transitions:
            if p in remaining and q in remaining:
                self.__add_transition(new_names[p],a,new_names[q])

        return self

    def __simulation_pairs(self):
        """ TODO

        Returns:
            set of pairs of integer: { (p,q) | p ~< q } TODO 
        """
        n = self.get_number_of_states()
        fs = self.get_finals()
        sim = { (p,q) for p in range(n) for q in range(n) if p != q and (p not in fs or q in fs) }
        old_sim = set()
        
        # turn sim into largest is-simulated-by relation by successively removing pairs (p,q) such that p is not simulated by q
        while sim != old_sim:
            old_sim = sim.copy()
            for (p,q) in old_sim:
                is_simulated = True
                for a in FiniteAutomata.get_alphabet():
                    p_succs = self.get_successors(p,a)
                    q_succs = self.get_successors(q,a)

                    for s in p_succs:
                        found_match = False
                        for t in q_succs:
                            if s==t or (s,t) in sim:
                                found_match = True
                                break

                        if not found_match:
                            is_simulated = False
                            break
                    if not is_simulated:
                        break

                if not is_simulated:
                    sim.discard((p,q))
        return sim

    def simulation_equivalence_pairs(self):
        """ TODO

        Returns:
            set of pairs of integer: { (p,q) | p ~~ q and p < q } TODO
        """
        simulated_by = self.__simulation_pairs()
        return { (p,q) for (p,q) in simulated_by if p < q and (q,p) in simulated_by }

    def bisimulation_pairs(self):
        """ TODO

        Returns:
            set of pairs of integer: { (p,q) | p ~ q and p < q } TODO
        """  
        n = self.get_number_of_states()
        fs = self.get_finals()
        sim = { (p,q) for p in range(n-1) for q in range(p,n) if (p not in fs or q in fs) and (p in fs or q not in fs) }
        old_sim = set()
        
        # turn sim into largest bisimulation by successively removing pairs (p,q) such that p is not bisimilar to q
        while sim != old_sim:
            old_sim = sim.copy()
            for (p,q) in old_sim:
                is_bisimilar = True
                for a in FiniteAutomata.get_alphabet():
                    p_succs = self.get_successors(p,a)
                    q_succs = self.get_successors(q,a)

                    for s in p_succs:
                        found_match = False
                        for t in q_succs:
                            if s==t or (s,t) in sim or (t,s) in sim:
                                found_match = True
                                break

                        if not found_match:
                            is_bisimilar = False
                            break
                    if not is_bisimilar:
                        break

                    for t in q_succs:
                        found_match = False
                        for s in p_succs:
                            if s == t or (s,t) in sim or (t,s) in sim:
                                found_match = True
                                break

                        if not found_match:
                            is_bisimilar = False
                            break
                    if not is_bisimilar:
                        break

                if not is_bisimilar:
                    sim.discard((p,q))
        return sim

    def __merge_states(self,replacements):
        """ Merges the states of the automaton q and p exactly when the dictionary (replacement) maps from q to p. 
        For example, simulation-equivalent states can be combined into one state to minimize the automaton. 

        Args:
            replacements (dict of int: int): Describes the replacements where the state from the key is replaced by the state from the value. 

        Returns:
            self: Returns the finite automaton objeckt with the substitutions/merges of states.
        """
        for (p, a, q) in self.get_transitions().copy():
            p1 = replacements[p]
            q1 = replacements[q]
            if p1 != p or q1 != q:
                self.__remove_transition(p,a,q)
                self.__add_transition(p1,a,q1)
        return self

    def __minimize(self):
        """ Minimisation via some simulation-based equivalence quotienting. 
        Merge pairs of equivalent states, using smallest state as representative of equivalence class.   

        Returns:
            self: Returns the minimized automaton.
        """     
        replacements = { p: p for p in range(0,self.get_number_of_states()) }
        mergable = set()

        # Determine the states that can be combined into one.
        if FiniteAutomata.minimization_engine == FiniteAutomata.SIMUEQ:
            mergable = self.simulation_equivalence_pairs()
        elif FiniteAutomata.minimization_engine == FiniteAutomata.BISIMU:
            mergable = self.bisimulation_pairs()

        for (p,q) in mergable:
            r = replacements[q]
            if p < r:
                replacements[q] = p
        self.__merge_states(replacements)

        # if s <=> t and s<t and t is initial, then s becomes initial now
        new_initials = { replacements[t] for t in self.get_initials() }
        self.__clear_initials()
        for s in new_initials:
            self.__make_initial(s)

        self.__shrink_to(self.__reachables())
        return self

    """ =======================================================================================================================
        Operations on the finite automata like: determinize, complement, ...
        =======================================================================================================================
    """
    def star(self):
        """ Surround the set of words in the language with the star opration.
        For example, if the automaton describes the language "aa", the language of the automaton after this operation is "(aa)*".

        Returns:
            self: Finite automaton created by the star operation.
        """
        finals_without_outgoing = { q for q in self.get_finals() if self.get_all_successors(q) == set() }
        initials_without_incoming = { q for q in self.get_initials() if self.get_all_predecessors(q) == set() }

        # add transitions from all final states to successors of initial states
        for p in self.get_finals():
            for r in self.get_initials():
                for a in FiniteAutomata.get_alphabet():
                    for q in self.get_successors(r,a):
                        self.__add_transition(p,a,q)

        # add possibility to accept empty word if not already in the language
        if not self.accepts_empty_word():
            # only do something if empty word not already in the original language
            if self.get_finals() == set():
                # if there are no final states then reduce everything to a one-state NFA that accepts epsilon
                self.__clear_initials()
                self.__make_initial(0)
                self.__make_final(0)
                self.__clear_transitions()
            else:
                # see if it is safe to make final states initial or vice-versa
                done = False
                for q in finals_without_outgoing:
                    self.__make_initial(q)
                    done = True
                for q in initials_without_incoming:
                    self.__make_final(q)
                    done = True
                if not done:
                    # add an additional final state, make this the only initial only
                    n = self.get_number_of_states()
                    for a in FiniteAutomata.get_alphabet():
                        for p in self.get_initials():
                            for q in self.get_successors(p,a):
                                self.__add_transition(n,a,q)
                    self.__clear_initials()
                    self.__make_initial(n)
                    self.__make_final(n)

        self.__minimize()
        return self

    def __power_set_construction(self):
        """ Power sets construction of the finite automaton.

        Returns:
            FiniteAutomata: The deterministic finite automaton resulting from the power set construction. 
        """
        codes = {}
        n = 0

        def code(ps):
            nonlocal n
            if ps in codes:
                return codes[ps]
            else:
                codes[ps] = n
                n += 1
                return n-1

        res = FiniteAutomata.empty_nfa()

        initial_state = frozenset(self.get_initials())
        c = code(initial_state)
        res.__make_initial(c)

        todo = [ (initial_state,c) ]
        visited = set()
        while todo:
            (ps,c) = todo.pop(0)
            if c not in visited:
                visited.add(c)

                for a in FiniteAutomata.get_alphabet():
                    succs = set()
                    for p in ps:
                        succs = succs.union(self.get_successors(p,a))
                    succs = frozenset(succs)
                    c1 = code(succs)
                    new_state = (succs, c1)
                    res.__add_transition(c,a,c1)
                    todo.append(new_state)

                if self.get_finals().intersection(ps) != set():
                    res.__make_final(c)

        return res

    def determinize(self):
        """ Method to determine a finite automaton to obtain a deterministic finite automaton. 

        Returns:
            FiniteAutomata: A deterministic finite automaton describing the same language.
        """
        dfa = self.__power_set_construction()
        dfa.__shrink_to(dfa.__productives())
        dfa.__minimize()
        return dfa

    def complement(self):
        compl = self.__power_set_construction()

        n = compl.get_number_of_states()
        for p in range(0,n):
            if p in compl.get_finals():
                compl.__make_nonfinal(p)
            else:
                compl.__make_final(p)

        compl.__shrink_to(compl.__productives())
        compl.__minimize()
        return compl

    """ =======================================================================================================================
        Operations between two finite automata like: union, intersect, ...
        =======================================================================================================================
    """
    def union(self, other):
        """ Unions the language of this finite automaton with the language of another finite automaton.

        Args:
            other (FiniteAutomata:): The finite automaton with which this object is to be union.

        Returns:
            self: The union of the two finite automatas.
        """
        # add a new initial state which behaves like all initial states of self and nfa
        s = self.get_number_of_states()

        for a in FiniteAutomata.get_alphabet():
            for p in self.get_initials():
                for q in self.get_successors(p,a):
                    self.__add_transition(s,a,q)

            for p in other.get_initials():
                for q in other.get_successors(p,a):
                    self.__add_transition(s,a,q+s+1)

        # make the new state final if any of the initial states was final
        for q in self.get_initials().intersection(self.get_finals()).union(other.get_initials().intersection(other.get_finals())):
            self.__make_final(s)
            break

        self.__clear_initials()
        self.__make_initial(s)

        # import transitions from other into self
        for (p,a,q) in other.get_transitions():
            self.__add_transition(p+s+1, a, q+s+1)

        # make finals states of other final in self as well
        for q in other.get_finals():
            self.__make_final(q+s+1)

        # union construction can create unreachable states, remove these now
        self.__shrink_to(self.__reachables())
        self.__minimize()
        return self

    def concatenate(self, other):
        """ Concatenates the language of this finite automaton with the language of another finite automaton.

        Args:
            other (FiniteAutomata:): The finite automaton with which this object is to be concatenate.

        Returns:
            self: The concatenation of the two finite automatas.
        """
        s = self.get_number_of_states()

        # import all transitions from other into self
        for (p,a,q) in other.get_transitions():
            self.__add_transition(p+s,a,q+s)

        # add transitions from all final states in self to successors of initial states in other
        for a in FiniteAutomata.get_alphabet():
            for p in other.get_initials():
                succs = other.get_successors(p,a)
                for q in succs:
                    for r in self.get_finals():
                        self.__add_transition(r,a,q+s)

        # set new final states
        if not other.accepts_empty_word():
            self.__clear_finals()
        for q in other.get_finals():
            self.__make_final(q+s)

        self.__shrink_to(self.__reachables())
        self.__minimize()
        return self

    def intersect(self,other):
        """ Intersect the language of the finite automaton with the language of another finite automaton.

        Args:
            other (FiniteAutomata:): The finite automaton with which this object is to be intersect.

        Returns:
            self: The intersection of the two finite automatas.
        """
        codes = {}
        n = 0
        def code(p,q):
            nonlocal n
            if (p,q) in codes:
                return codes[(p,q)]
            else:
                codes[(p,q)] = n
                n += 1
                return n-1

        result = FiniteAutomata.empty_nfa()

        # set new initial states
        initial_pairs = [ (p,q,code(p,q)) for p in self.get_initials() for q in other.get_initials() ]
        for (p,q,c) in initial_pairs:
            result.__make_initial(c)

        todo = initial_pairs
        visited = set()
        while todo:
            (p,q,c) = todo.pop(0)
            if c not in visited:
                visited.add(c)

                # set new transitions
                for a in FiniteAutomata.get_alphabet():
                    p_succs = self.get_successors(p,a)
                    q_succs = other.get_successors(q,a)
                    new_states = [ (p1,q1,code(p1,q1)) for p1 in p_succs for q1 in q_succs ]
                    for (p1,q1,c1) in new_states:
                        result.__add_transition(c,a,c1)
                    todo += new_states
                
                # set new final states
                if p in self.get_finals() and q in other.get_finals():
                    result.__make_final(c)

        result.num_states = n
        result.__shrink_to(result.__productives())
        result.__minimize()
        return result

    def symetrical_difference(self, other):
        """ Determines the symmetric difference between the languages described by 2 finite automata and 
        additionally the two disjoint subsets of the symmetric difference. 

        Args:
            other (FiniteAutomata:): The finite automaton with which the symmetric difference is to be formed. 

        Returns:
            FiniteAutomata, FiniteAutomata, FiniteAutomata: 1, 2, 3
                                                            1: The finite automaton that describes the language in which all words are located 
                                                            that were only in the language of self and not in the language of the other. 
                                                            2: The finite automaton that describes the language in which all words are located 
                                                            that were only in the language of the other and not in the language of self. 
                                                            3: The finite automaton describing the union of the languages from 1 and 2. 
                                                            So the symmetric difference between self and other.
        """
        self.__minimize()
        other.__minimize()

        s_sub_o = self.determinize().intersect(other.complement())
        o_sub_s = other.determinize().intersect(self.complement())
        sym_diff = s_sub_o.union(o_sub_s)

        return s_sub_o, o_sub_s, sym_diff