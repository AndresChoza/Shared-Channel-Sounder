import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def graficar():
    data = pd.read_csv("pds.csv")
    data.plot()
    print(data)
    plt.show()