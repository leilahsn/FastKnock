"""
    *** FastKnock.py is the main method of the algorithm
    *** Processes are defined in this method for traversing the tree branches.
    *** Each Process writes its solutions into the separate files.
"""

from Node import Node
import PreProcessing as PreProc
import cobra.io
from identifyTargetSpace import identifyTargetSpace
from constructSubTree import constructSubTree
from traverseTree import procTraverseTree
import sys
import multiprocessing
from findingCoKnockOut import findingCoKnockoutRxns
import mergeFile 



def construct_data_structure (number):
    data_struct = [[] for i in range(int(number)+1)]
    return data_struct

"""
    * medium culture is determined and 
    * by preprocessing the model Removable and
    * coKnockoutRxns sets are obtained in this method
"""
def model_preparation (model_name):
    model = cobra.io.load_matlab_model(model_name)
    model.solver = "glpk"
    
      
    #
    # As mentioned in the third step of README.md file, the medium culture should be specified in the following lines.
    # model.reactions[model.reactions.index("EX_o2(e)")].lower_bound = 0
    # model.reactions[model.reactions.index("EX_o2(e)")].upper_bound = 0

    # model.reactions[model.reactions.index("EX_glc(e)")].lower_bound = -10
    # model.reactions[model.reactions.index("EX_glc(e)")].upper_bound = 0
    # #
    #
      

    coKnockoutRxns = findingCoKnockoutRxns(model)
    PreProc.identifying_eliminate_list(model)

    eliminate_list = []
    with open("eliminate_list.txt" , 'r') as f:
        for line in f:
            if line not in ['\n', '\r\n', '\t']:
                line = line.replace('\n', '')
                eliminate_list.append(line)
    model = PreProc.remove_blocked_rxn(model)

    Removable = []
    for i in model.reactions:
        if i.id not in eliminate_list:
            Removable.append(i.id)

    return model, Removable, coKnockoutRxns


def print_node(X):
    print (X.level)
    print (X.deleted_rxns)
    print (X.target_space)
    print (X.flux_dist)


""" The solutions are written in the file by this method"""
def writeInFile (level, solution):

    file_name = str(level)+".txt"
    with open(file_name , 'w') as f:
        for X in solution:
            sol = [X.deleted_rxns, X.biomass, X.chemical]
            f.write(str(sol))
            f.write('\n')
    f.close()
    
    

def main():
    
    target_level = input("Enter your desired level (maximum number of simultaneous reaction knockout ):  ")

    guaranteed_flag = 0
    if ( int(input("If you want to use FastKnock in guaranteed mood, press 1 othrwise press 0: ")) == 1 ):
        guaranteed_flag = 1

    num_of_processes = input("Enter number of proccessor cores: ")

    queue = construct_data_structure (target_level)
    checked = construct_data_structure (target_level)
    solution = construct_data_structure (target_level)
    guaranteed_solution = construct_data_structure (target_level)

    #  
    #As mentioned in the second step of README.md file, the name of model should be replaced in the next line.
    x="Community1.mat"
    model, Removable, coKnockoutRxns = model_preparation (x)

    root = Node (0,[] , [] , [],0,0)
    root = identifyTargetSpace(root, model, Removable,coKnockoutRxns)

    all_fba_call = [[] for i in range(int(target_level)+1)]
    for i in range (int(target_level)+1):
        all_fba_call[i] = 0
    
    level_one, queue, checked, solution, all_fba_call = constructSubTree(root, target_level, checked, queue, solution, model, Removable, all_fba_call, coKnockoutRxns, guaranteed_flag, guaranteed_solution )



    queue_index = 0
    elements = (len(queue[int(level_one)]) - 3)/(int(num_of_processes) - 2)

    for j in range (int(num_of_processes)):
        globals()['queue_p%s' % (j+1)] = construct_data_structure (target_level)
        globals()['checked_p%s' % (j+1)] = construct_data_structure (target_level)
        globals()['solution_p%s' % (j+1)] = construct_data_structure (target_level)
        globals()['guaranteed_solution_p%s' % (j+1)] = construct_data_structure (target_level)

        globals()['all_fba_call_p%s' % (j+1)] = construct_data_structure (target_level)
        for i in range (int(target_level)+1):
            globals()['all_fba_call_p%s' % (j+1)][i] = 0

        if (j == 0):
            globals()['queue_p%s' % (j+1)][int(level_one)] = queue[int(level_one)][0:1]
        
        elif (j == 1):
            globals()['queue_p%s' % (j+1)][int(level_one)] = queue[int(level_one)][1:3]
            globals()['checked_p%s' % (j+1)][int(level_one)] = queue[int(level_one)][0:1]

             
        else:
            globals()['queue_p%s' % (j+1)][int(level_one)] = queue[int(level_one)][int(elements)*(j-1):int(elements)*j]

        if(j > 1):
            globals()['checked_p%s' % (j+1)][int(level_one)] = queue[int(level_one)][0:int(elements)*(j-1)]

        
        globals()[f"p{j+1}"] = multiprocessing.Process(target = procTraverseTree, args=(f"p{j+1}", level_one, globals()['queue_p%s' % (j+1)], globals()['checked_p%s' % (j+1)], globals()['solution_p%s' % (j+1)], target_level, model, Removable, globals()['all_fba_call_p%s' % (j+1)], coKnockoutRxns , guaranteed_flag, globals()['guaranteed_solution_p%s' % (j+1)] ))



    for j in range (int(num_of_processes)):
       globals()['p%s' % (j+1)].start()

    for j in range (int(num_of_processes)):
       globals()['p%s' % (j+1)].join()

    mergeFile.merge(int(num_of_processes), int(target_level))

if __name__ =='__main__':
    main()
