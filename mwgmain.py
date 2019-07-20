import pandas as pd
import urllib
import os, sys, json, re
from math import *
from scipy import stats
import numpy as np




# with open(filename) as fp:
#     data = json.load(fp)
# Standard plotly imports
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode
import matplotlib.pyplot as plt
import plotly_express as px

# Using plotly + cufflinks in offline mode

filename = "submasterDurations_sols2170to2395_postUpdate.json"
f = open(filename, "r")
data = pd.read_json(f)
print(data)