"""
    *** this class is definition of the node object and its properties
"""


class Node:
    def __init__(self, level, deleted_rxns, target_space, flux_dist, biomass, chemical):
        self.level = level
        self.deleted_rxns = deleted_rxns
        self.target_space = target_space
        self.flux_dist = flux_dist
        self.biomass = biomass
        self.chemical = chemical
