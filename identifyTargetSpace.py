"""
    *** In this method the target_space of each node X is obtained.
    *** It determines the flux distribution and target space of node X. 
"""

def identifyTargetSpace(X, model, Removable, coKnockoutRxns):

    #Construct model_X
    deleted_rxns_details = {}

    cokKnockouts = []
    for rxn in X.deleted_rxns:
        if rxn in coKnockoutRxns:
            cokKnockouts.extend(coKnockoutRxns[rxn])

    cokKnockouts = set(cokKnockouts)
    cokKnockouts = list(cokKnockouts)
    
    X.deleted_rxns.extend(cokKnockouts)
    X.deleted_rxns = set(X.deleted_rxns)
    X.deleted_rxns = list(X.deleted_rxns)

    
    for rxn in X.deleted_rxns:
        if rxn in model.reactions:
            LB = model.reactions[model.reactions.index(rxn)].lower_bound
            UB = model.reactions[model.reactions.index(rxn)].upper_bound
            model.reactions[model.reactions.index(rxn)].lower_bound = 0
            model.reactions[model.reactions.index(rxn)].upper_bound = 0
            deleted_rxns_details[rxn] = [LB, UB]
        else:
            X.deleted_rxns.remove(rxn)

    X.flux_dist = model.optimize()

    if (X.flux_dist != 0):
        if (X.flux_dist.status != 0) or (X.flux_dist.status == "optimal") :
            for key,value in X.flux_dist.fluxes.iteritems():
                if abs(float(value)) > 1e-09 and key in Removable :
                    X.target_space.append(key)

    #Restore  model
    for key, value in deleted_rxns_details.items():
        model.reactions[model.reactions.index(key)].lower_bound = value[0]
        model.reactions[model.reactions.index(key)].upper_bound = value[1]

    return X
    
