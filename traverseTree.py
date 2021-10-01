"""
    *** This file contains two function, procTraverseTree which call traverseTree function for each processes of the parallel algorithm
    *** The traverseTree subprocedure recursively navigates the tree based on a depth-first traversal. 
"""


from constructSubTree import constructSubTree

def writeInFile (process_name, level, solution):

    file_name = process_name+'_'+str(level)+".txt"
    with open(file_name , 'w') as f:
        for X in solution:
            sol = [X.deleted_rxns, X.biomass, X.chemical]
            f.write(str(sol))
            f.write('\n')
    f.close()
    

def traverseTree(process_name,level, queue, checked, solution, target_level, model, Removable, all_fba_call, coKnockoutRxns, guaranteed_flag, guaranteed_solution):

    while True:

        if int(level)  == 0:
            return solution

        elif len(queue[int(level) ]) == 0:
            checked[int(level) ] = []
            level = int(level)  - 1

        else:
            X = queue[int(level)].pop(0)
            if X is None:
                continue
            next_level, queue, checked, solution, all_fba_call = constructSubTree (X, target_level, checked, queue, solution, model, Removable, all_fba_call, coKnockoutRxns, guaranteed_flag, guaranteed_solution)
            level = next_level
            print (process_name,level,len(queue[int(level) ]), len (checked[int(level) ]))


def procTraverseTree(process_name, level, queue, checked, solution, target_level, model, Removable, all_fba_call, coKnockoutRxns, guaranteed_flag, guaranteed_solution):

    print ("process ", process_name, " is started.")
    solution = traverseTree(process_name,level, queue, checked, solution, target_level, model, Removable, all_fba_call, coKnockoutRxns, guaranteed_flag, guaranteed_solution)
    for i in range(len(solution)):
        writeInFile (process_name,i, solution[i])

    print ("process ", process_name, " is fininshed.")


        
