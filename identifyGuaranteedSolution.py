"""
    *** isGuaranteedSolution specifies whether a minimum flux distribution of a node X can be the maximized
    *** In this function all of the desired chemicals and their threshold are defined and set.
"""
from cobra.flux_analysis import flux_variability_analysis

def isGuaranteedSolution(X, model):

    #
    # As mentioned in the 4th step of README.md file, the desired chemical and biomass (and their threshold) reactions should be defined in the following lines.
    chemical = 'EX_succ_e[u]'
    biomass = "ecoli_BIOMASS_Ec_iML1515_core_75p37M"
    Th_chemical = 0.64
    Th_biomass = 0.01
    #
    #
   
   
    fva_result = flux_variability_analysis(model , model.reactions ,fraction_of_optimum=0.95)

    if (fva_result['minimum'][chemical] >Th_chemical and fva_result['minimum'][biomass] > Th_biomass):
            X.chemical = fva_result['minimum'][chemical]
            X.biomass = fva_result['minimum'][biomass]

    return 
