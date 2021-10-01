"""
    *** PreProcessing.py aims to  determine eliminate list of the model
    *** the main method of this file is identifying_eliminate_list(model)
"""



import cobra.test
import time
import numpy as np

#Removing blocked reactions
def remove_blocked_rxn(model):

    blocked_rxn = cobra.flux_analysis.variability.find_blocked_reactions(model, reaction_list=None, zero_cutoff=None, open_exchanges=False)
    for i in blocked_rxn:
        reaction = model.reactions.get_by_id(i)
        reaction.remove_from_model()

    return model


#Finding essential reactions
def essential_reaction(model):
    
    essential_rxn = []    
    for  i in model.reactions:
        
        lb = model.reactions[model.reactions.index(i)].lower_bound
        ub = model.reactions[model.reactions.index(i)].upper_bound

        if (i.id == 'ATPM'):
            continue
        
        model.reactions[model.reactions.index(i)].lower_bound = 0.0
        model.reactions[model.reactions.index(i)].upper_bound = 0.0
        
        solutionKO_i  = model.optimize()
        if (solutionKO_i.objective_value < 0.01) or (np.isnan(solutionKO_i.objective_value)) :
            essential_rxn.append(i.id)
            
        model.reactions[model.reactions.index(i)].lower_bound = lb
        model.reactions[model.reactions.index(i)].upper_bound = ub        
            
    return essential_rxn

#Finding exchange reactions
def find_Exchange(model):

    ex_rxn = []
    for i in model.exchanges:
        ex_rxn.append(i.id)
        
    return ex_rxn


#Finding reactions belong to especial subsystems
def find_subsystems(model):

    Cell_Envelope_Biosynthesis = str("Cell Envelope Biosynthesis")
    Glycerophospholipid_Metabolism = str("Glycerophospholipid Metabolism")
    Inorganic_Ion_Transport_and_Metabolism = str("Inorganic Ion Transport and Metabolism")
    Lipopolysaccharide_Biosynthesis_Recycling = str("Lipopolysaccharide Biosynthesis / Recycling")
    Membrane_Lipid_Metabolism = str("Membrane Lipid Metabolism")    
    Murein_Biosynthesis = str("Murein Biosynthesis")
    Murein_Recycling = str("Murein Recycling")
    Transport_Inner_Membrane = str("Transport, Inner Membrane")
    Transport_Outer_Membrane = str("Transport, Outer Membrane")
    Transport_Outer_Membrane_Porin = str("Transport, Outer Membrane Porin")
    tRNA_Charging = str("tRNA Charging")

    removable_from_search_space_subsystems = []
    removable_from_search_space_subsystems.append(Cell_Envelope_Biosynthesis)
    removable_from_search_space_subsystems.append(Glycerophospholipid_Metabolism)
    removable_from_search_space_subsystems.append(Inorganic_Ion_Transport_and_Metabolism)
    removable_from_search_space_subsystems.append(Lipopolysaccharide_Biosynthesis_Recycling)
    removable_from_search_space_subsystems.append(Membrane_Lipid_Metabolism)
    removable_from_search_space_subsystems.append(Murein_Biosynthesis)
    removable_from_search_space_subsystems.append(Murein_Recycling)
    removable_from_search_space_subsystems.append(Transport_Inner_Membrane)
    removable_from_search_space_subsystems.append(Transport_Outer_Membrane)
    removable_from_search_space_subsystems.append(Transport_Outer_Membrane_Porin)
    removable_from_search_space_subsystems.append(tRNA_Charging)

    removable_reaction_from_subsystem = []
    
    for i in model.reactions:
        
        if i.subsystem in removable_from_search_space_subsystems:
            removable_reaction_from_subsystem.append(i.id)
            print (i.id)

    return removable_reaction_from_subsystem
    
#finding zero bound reactions
def zero_bound_reactions(model):
    
    zero_bound_rxns = []
    for i in model.reactions:

        if abs(i.lower_bound - i.upper_bound) < 1e-10 and i.lower_bound == 0 and i.upper_bound==0:
            zero_bound_rxns.append(i.id)
    return zero_bound_rxns


def identifying_eliminate_list(model):

    essential_rxn = essential_reaction(model)
    ex_rxn = find_Exchange(model)

    removable_rxn_from_subsystem = find_subsystems(model)
    zero_bound_rxns = zero_bound_reactions(model)
    
    eliminate_list = list ( set(essential_rxn) | set(ex_rxn) | set(removable_rxn_from_subsystem) |
                                        set(zero_bound_rxns) )

    with open("eliminate_list.txt" , 'w') as f:
        for i in eliminate_list:
            f.write(str(i))
            f.write('\n')
        f.write('ATPM')
        f.write('\n')
    f.close() 
        
    return eliminate_list

if __name__ =='__main__':
    main()
