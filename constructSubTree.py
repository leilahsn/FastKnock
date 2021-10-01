"""
    *** This method is construct corresponding subtree of the node X
    *** it returns children nodes of X at level (X.level+1)
"""

from Node import Node
from identifyTargetSpace import identifyTargetSpace
from identifyMaximizedSolution import isMaximizedSolution
from identifyMaximizedSolution import setSolution
from identifyGuaranteedSolution import  isGuaranteedSolution

def constructSubTree (X, target_level, checked, queue, solution, model, Removable,all_fba_call, coKnockoutRxns, guaranteed_flag, guaranteed_solution ):

    current_level = X.level
    next_level = int(current_level) + 1

    if int(current_level) == int(target_level):
        return target_level, queue, checked, solution, all_fba_call

    else:
        for rxn in X.target_space:
            
            if (rxn not in checked[int(next_level)]) and (rxn in coKnockoutRxns):
                
                r = Node (next_level, X.deleted_rxns+[rxn], [], [],0,0)

                r = identifyTargetSpace(r, model, Removable, coKnockoutRxns)
                all_fba_call[int(next_level)] += 1
                
                if  (r.flux_dist != 0):
                    if (isMaximizedSolution(r)):
                        r = setSolution(r)
                        solution[int(next_level)].append(r)

                        if (guaranteed_flag):
                            r = isGuaranteedSolution(r, model)
                            guaranteed_solution[int(next_level)].append(r)

                queue[int(next_level)].append(r)
                checked[int(next_level)].append(rxn)

        return next_level, queue, checked, solution, all_fba_call

                
                
    
