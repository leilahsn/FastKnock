"""
    *** isMaximizedSolution specifies whether a flux distribution of a node X can be the maximized solution to the problem
    *** In this function all of the desired chemicals and their threshold are defined and set.
"""

def isMaximizedSolution(X):

    #
    #As mentioned in the 4th step of README.md file, the desired chemical and biomass (and their threshold) reactions should be defined in the following lines.
    chemical = 'EX_succ_e[u]'
    # biomass = "BiomassEcoli"
    biomass = "ecoli_BIOMASS_Ec_iML1515_core_75p37M"
    Th_chemical = 0.1
    Th_biomass = 0.01
    #
    #

    if (X.flux_dist.fluxes[biomass] >Th_biomass) and (X.flux_dist.fluxes[chemical] >Th_chemical):
        return True
    else:
        return False

def setSolution(X):
    chemical = 'EX_succ_e[u]'
    # biomass = "BiomassEcoli"
    biomass = "ecoli_BIOMASS_Ec_iML1515_core_75p37M"

    X.biomass = X.flux_dist.fluxes[biomass]
    X.chemical = X.flux_dist.fluxes[chemical]

    return X

    
    
