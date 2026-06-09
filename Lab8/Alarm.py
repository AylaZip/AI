from pgmpy.example_models import load_model
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.parameter_estimator import DiscreteMLE
from pgmpy.causal_discovery import PC
from pgmpy.sampling import BayesianModelSampling

import pandas as pd
from pgmpy.base import DAG


# Exercise 1: Learning from data
data = pd.DataFrame({
    "Study": [1, 1, 1, 1, 0, 0, 0, 0, 1, 0],
    "Sleep": [1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    "Pass":  [1, 1, 1, 0, 0, 0, 0, 0, 1, 0],
})
dag = DAG([("Study", "Pass"), ("Sleep", "Pass")])

model = DiscreteBayesianNetwork(dag)
fitted_model = model.fit(data, estimator=DiscreteMLE())
print("Exercise 1 - CPDs:")
for c in fitted_model.get_cpds():
    print(c)
print()


# Exercise 2: Learning from simulation
print("Exercise 2:")
alarm = load_model('bnlearn/alarm')

sim = BayesianModelSampling(alarm)
simulated = sim.forward_sample(size=100)
print(f"Simulated {len(simulated)} records from ALARM")

pc = PC(variant='stable', return_type='dag')
pc.fit(simulated)
learned_edges = list(pc.causal_graph_.edges())
print(f"Learned edges: {learned_edges}")

fitted = DiscreteBayesianNetwork(learned_edges)
fitted.fit(simulated, estimator=DiscreteMLE())
print("Learned CPDs (first 5):")
for c in fitted.get_cpds()[:5]:
    print(c)