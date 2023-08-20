"""
    *** In this file, based on the obtained essential and involved sets of each reaction in Gene_Rule.py,
           the way of each reaction knockout by the genes is determined.
    *** Other reactions that are forcibly eliminated with the reaction are also identified.
"""



import cobra.io
import time
import Gene_Rule as GR

def clustering_reactions_with_generule(deleted_rxn,
                                       ess_and_inv_genes_of_reactions, deleted_reaction_by_genes ):
        
    del_genes = []
    co_clustered_rxn = []
    
    ess_genes = ess_and_inv_genes_of_reactions[deleted_rxn]['essential']
    inv_genes = ess_and_inv_genes_of_reactions[deleted_rxn]['involved']

    #reaction with unknown gene rule
    if len(ess_genes) == 0 and len(inv_genes) == 0:
        return co_clustered_rxn

    #reactions with single gene gene-rule
    if len(ess_genes) == 1:
        co_clustered_rxn = deleted_reaction_by_genes[ess_genes[0]]['essential']
        return co_clustered_rxn

    #reaction with some genes ANDed in the gene-rule
    if len(ess_genes) > 1:
        temp_num = 10000
        for gene in ess_genes:
            gene = gene.replace('(', '')
            gene = gene.replace(')', '')
            if len(deleted_reaction_by_genes[gene]['essential']) < temp_num:
                best_ess_gene = gene
                temp_num = len(deleted_reaction_by_genes[gene]['essential'])
                

        co_clustered_rxn = deleted_reaction_by_genes[best_ess_gene]['essential']
        return co_clustered_rxn

    #Some genes ORed or ANDed/ORed in the gene-rule
    deleted_genes = inv_genes
    for gene in inv_genes:
        tmp_rxn = deleted_reaction_by_genes[gene]['essential']
        co_clustered_rxn.extend(tmp_rxn)

    for gene in inv_genes:
        tmp_rxn = deleted_reaction_by_genes[gene]['involved']
        for rxn in tmp_rxn:
            tmp_genes = ess_and_inv_genes_of_reactions[deleted_rxn]['involved']
            is_cluster_rxn = all(elem in deleted_genes for elem in tmp_genes)
            if is_cluster_rxn:
                co_clustered_rxn.append(rxn)

    co_clustered_rxn = set(co_clustered_rxn)
    
    return co_clustered_rxn
           
