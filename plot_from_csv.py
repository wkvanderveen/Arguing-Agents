import sys
import glob
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np



def main(argv):
    dfs = []
    file_names = glob.glob('results/time=1000_nAgents=20/*.csv')
    for file_name in file_names:
        dfs.append(pd.read_csv(file_name))

    df = pd.concat(dfs)
    x_label = 'elasticity'

    df = df.sort_values(x_label)



    x = df[x_label]
    y = df['Earnings']
    plt.plot(x, y, 'o')

    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r--")
    print("y=%.6fx+(%.6f)" % (z[0], z[1]))

    plt.xlabel(x_label)
    plt.ylabel("Earnings")

    plt.show()

    print(df)


if __name__ == "__main__":
    main(sys.argv)