import sys
import glob
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats

def main(argv):
    dfs = []
    file_names = glob.glob('results/*.csv')
    for file_name in file_names:
        dfs.append(pd.read_csv(file_name))

    this_color = 0
    for df in dfs:
        df['color'] = [this_color] * df.shape[0]
        this_color = this_color + 1

    df = pd.concat(dfs)


    x_label = 'elasticity'
    x2_label = 'patience'

    df = df.sort_values(x_label)
    df2 = df.sort_values(x2_label)

    x = df[x_label]
    x2 = df2[x2_label]
    y = df['Earnings']
    y2 = df2['Earnings']

    plt.subplot(121)
    plt.scatter(x, y, c=df[x_label])
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r--")
    print("y=%.6fx+(%.6f)" % (z[0], z[1]))
    pr = stats.pearsonr(x, y)
    plt.title("Correlation between {0} and earnings. Pearson-R correlation coefficient = {1}".\
        format(x_label, pr[0].round(3)))
    plt.xlabel(x_label)
    plt.ylabel("Earnings")
    plt.colorbar()


    plt.subplot(122)
    plt.scatter(x2, y2, c=df2['elasticity'])
    z2 = np.polyfit(x2, y2, 1)
    p2 = np.poly1d(z2)
    plt.plot(x2, p2(x2), "r--")
    print("y2=%.6fx2+(%.6f)" % (z2[0], z2[1]))
    pr2 = stats.pearsonr(x2, y2)
    plt.title("Correlation between {0} and earnings. Pearson-R correlation coefficient = {1}".\
        format(x2_label, pr2[0].round(3)))
    plt.xlabel(x2_label)
    plt.colorbar()

    plt.show()

    print(df)


if __name__ == "__main__":
    main(sys.argv)
