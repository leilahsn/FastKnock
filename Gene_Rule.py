"""
    *** Gene rule file demonstrates the essential and involved sets of each reaction in the model
    *** These sets are being used in findingCoKnockoutRxns.py and Clustering_Reactions.py file
"""


from collections import defaultdict
import cobra.test
import cobra.core.reaction


#Creating a list of reactions gene rules 
def gene_rules(model):
    
    gene_rule =  []
    
    for i in range (len(model.reactions)):
        rxn = model.reactions[i]
        genes = rxn.gene_reaction_rule
        genes = genes.replace(" ", '')
        genes = genes.replace(")", '')
        genes = genes.replace("(", '')
        gene_rule.append([rxn.id, genes])
      
    return ess_and_inv_genes(model, gene_rule)


#Checking a rule is AND/OR or not
def checking_and_or_rule(rule):
    
    rule = rule.split('or')
    andOrFlag = False

    for r in rule:
        if len(r.split('and')) > 1 :
            andOrFlag = True

    return andOrFlag


#Evaluation essential and involved genes of each reaction
def ess_and_inv_genes(model, gene_rule):

    ess_and_inv_genes_of_reactions = defaultdict(list)

    #evaluation of reaction deletion from a gene acording to essential and involved sets
    deleted_reaction_by_genes = defaultdict(list)
    for i in model.genes:
        ess_inv_rxn = defaultdict(list)
        ess_inv_rxn['essential'] = []
        ess_inv_rxn['involved'] = []
        deleted_reaction_by_genes[i.id] = ess_inv_rxn
     
    andOrRule = []
    andOrRxn  = []

    for i in gene_rule:
        rxn  = i[0]
        rule = i[1]

        #Reactions with unknown gene-rule
        if len(rule) == 0:
            
            ess_inv = defaultdict(list)
            ess_inv['essential'] = []
            ess_inv['involved']  = []
            ess_and_inv_genes_of_reactions[rxn] = ess_inv
            
            continue


        #reactions with single gene gene-rule
        if len(rule.split('or')) == 1 and len(rule.split('and')) == 1:
            
            ess_inv = defaultdict(list)
            ess_inv['essential'] = [rule]
            ess_inv['involved']  = []
            ess_and_inv_genes_of_reactions[rxn] = ess_inv

            deleted_reaction_by_genes[rule]['essential'].append(rxn)
            continue

    
        #Some genes ANDed in the gene-rule
        if len(rule.split('or')) == 1 and len(rule.split('and')) > 1:
            
            rule = rule.split('and')

            ess_inv = defaultdict(list)
            ess_inv['essential'] = rule
            ess_inv['involved'] = []
            ess_and_inv_genes_of_reactions[rxn] = ess_inv

            for g in rule:
                g = g.replace('(', '')
                g = g.replace(')', '')
                deleted_reaction_by_genes[g]['essential'].append(rxn)
                
            continue

        #Some genes ORed in the gene-rule
        if (len(rule.split('or')) > 1) and (checking_and_or_rule(rule) == False):
            
            rule = rule.split('or')

            ess_inv = defaultdict(list)
            ess_inv['essential'] = []
            ess_inv['involved'] = rule
            ess_and_inv_genes_of_reactions[rxn] = ess_inv

            
            for g in rule:
                deleted_reaction_by_genes[g]['involved'].append(rxn)
                
            continue


        #Some genes ANDed/ORed in the gene-rule
        if (len(rule.split('or')) > 1) and checking_and_or_rule(rule):

            ess_inv = defaultdict(list)
            ess_inv['essential'] = []
    
            rule = rule.replace(')', '').replace('(', '').split('or')
            for j in rule:
                j = j.split('and')
                ess_inv['involved'].append(j)

            ess_and_inv_genes_of_reactions[rxn] = ess_inv
            ess_and_inv_for_and_or_rule(rxn, ess_and_inv_genes_of_reactions, deleted_reaction_by_genes)
            
            continue
    
    return ess_and_inv_genes_of_reactions, deleted_reaction_by_genes



#Evaluating the minimal effective gene for And/Or gene rule reaction
def ess_and_inv_for_and_or_rule(rxn, ess_and_inv_genes_of_reactions, deleted_reaction_by_genes):

    inv_sets = ess_and_inv_genes_of_reactions[rxn]['involved']

    final_ess = []
    numOfDelRxn = 10000

    for i in inv_sets:
        for j in i:
            num = len(deleted_reaction_by_genes[j]['essential'])
            if num < numOfDelRxn:
                num = numOfDelRxn
                delgene = j

            final_ess.append(delgene)

        ess_and_inv_genes_of_reactions[rxn]['involved'] = set(final_ess)

    for g in final_ess:
        deleted_reaction_by_genes[g]['involved'].append(rxn)

    return ess_and_inv_genes_of_reactions, deleted_reaction_by_genes
