"""
    *** in this function, based on the analysis of the Clustering_Reactions.py and Gene_Rule.py,
            all of coKnockout reactions are identified.
"""

import cobra.test
import time
import Gene_Rule as GR
import Clustering_Reactions as CR

def findingCoKnockoutRxns(model):
    
    ess_and_inv_genes_of_reactions, deleted_reaction_by_genes = GR.gene_rules(model)

    coKnockoutRxns = {}
    checked_rxns = []

    for i in model.reactions:
        rxn = i.id
        if rxn in checked_rxns:
            continue

        coKnockoutrxn = CR.clustering_reactions_with_generule(rxn, ess_and_inv_genes_of_reactions, deleted_reaction_by_genes )
        coKnockoutRxns[rxn] = coKnockoutrxn
        checked_rxns.extend(coKnockoutrxn)

    return coKnockoutRxns
