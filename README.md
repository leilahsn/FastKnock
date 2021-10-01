# FastKnock
Version: 1.1

Introduction:
	FastKnock is an efficient algorithm to identify all possible knockout strategies for growth-coupled overproduction of biochemical(s) of interest. The details of the methodology and algorithm are explained in the following manuscript: 

Hassani et al. "FastKnock: An efficient approach to identify all knockout strategies for strain optimization", Submitted 2021.


Prerequisites:
- python 3.9
- COBRApy 0.21.0 and above

	To install COBRApy used the command: pip install cobra


Running FastKnock:

1 - Copy a desired genome scale model (.mat or .xml file) to the main directory of the project. For example you can use iJR904 model available in this project folder: https://github.com/leilahsn/FastKnock/blob/main/iJR904.mat

2 - Specify the name of the model in the main method of FastKnock.py. The main method is called at the end of the file Fastknock.py.

3 - Define the medium culture (for example Oxygen and Glucose uptake rate for iJR904) in the model_preparation function in FastKnock.py. 

4 - Define the desired chemicals and biomass reactions and their threshold in both identifyMaximizedSolution.py and identifyGuaranteedSolution.py files.

5 - In the main function of FastKnock.py demonstrate the the workspace of each process (i.e., the number of proccessor cores)

6 - Run the fastKnock.py file. In the command line of shell in the directory of the fastknock project execute the command: python Fastknock.py

7 - The output is a set of files knockoutStrategy_i.txt where i is the number of simultaneous reaction knockout.

		
Details of each file:

- Fastknock.py: FastKnock.py is the main method of the algorithm.
		Processes are defined in this method for traversing the tree branches.
    		Each Process writes its solutions into the separate files.

- PreProcessing.py : PreProcessing.py aims to  determine eliminate list of the model.

- Gene_Rule.py : This file demonstrates the essential and involved sets of each reaction.
    		 These sets are being used in Clustering_Reactions.py and findingCoKnockOut.py

- Clustering_Reactions.py: In this file, based on the obtained essential and involved sets of each reaction in Gene_Rule.py,
			   the way of each reaction knockout by the genes is determined.
			   Other reactions that are forcibly eliminated with the reaction are also identified.

- Node.py: This class is definition of the node object and its properties.


- findingCoKnockOut.py: In this function, based on the analysis of the Clustering_Reactions.py and Gene_Rule.py,
		        all of coKnockout reactions are identified.

- traverseTree_nonrec.py: This file contains two function, procTraverseTree which call traverseTree function for each processes of the parallel algorithm.
   			  The traverseTree sub-procedure recursively navigates the tree based on a depth-first traversal. 

- constructSubTree.py: This method is construct corresponding subtree of the node X
    		       It returns children nodes of X at level (X.level+1)

- identifyTargetSpace.py: In this method the target_space of each node X is obtained.
    			  It determines the flux distribution and target space of node X.

- identifyMaximizedSolution.py: This method specifies whether a flux distribution of a node X can be the maximized solution to the problem. In this function all of the desired chemicals and their threshold are defined.

- identifyGuaranteedSolution.py: This method specifies whether a minimum flux distribution of a node X can be maximized to the problem. In this function all of the desired chemicals and their threshold are defined.
