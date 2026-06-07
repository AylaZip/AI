from pgmpy.example_models import load_model
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.causal_discovery import PC

import pandas as pd
from pgmpy.base import DAG


#Exercise 1: Learning from data
# Example of creating a Bayesian network and fitting to input data
data = pd.DataFrame({
    "A": [0, 0, 1], 
    "B": [0, 1, 0], 
    "C": [1, 1, 0]
    })
dag = DAG([("A", "C"), ("B", "C")])

model = DiscreteBayesianNetwork(dag)
fitted_model = model.fit(data)
for c in fitted_model.get_cpds():
    print(c)

# Use the example to fit to the data provided for exercise 1
raise NotImplementedError("Please implement the code for exercise 1 here.")


#Exercise 2 learning from simualtion
# Use the knowledge from Exercise 1, and the comments below to fully solve the task.

# Load a Discrete Bayesian Network and simulate data, use the link for guidance.
# https://pgmpy.org/api/generated/structure_learning/pgmpy.causal_discovery.PC.html#pgmpy.causal_discovery.PC:~:text=arXiv%3A1302.4972%20(2013).-,Examples,-Simulate%20some%20data
raise NotImplementedError("Load the network and simulate data.")

# Learn a network from simulated data. use the link above for guidance.
raise NotImplementedError("Fit the network to the simulated data.")

# Use the edges from the fitted graph to create a new Discrete Bayesian Network and fit it to the data using Maximum Likelihood Estimation.
# https://pgmpy.org/api/generated/models/pgmpy.models.DiscreteBayesianNetwork.html#pgmpy.models.DiscreteBayesianNetwork.fit:~:text=dtype%20%60float.)-,estimator,-%3A%20Estimator%20class
raise NotImplementedError("Create a new Bayesian Network and fit it to the data.")