import sys
import glob
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats

<<<<<<< HEAD
=======

def report_p(p):
    if p.round(3) < 0.001:
        return "<0.001"
    else:
        return str(p.round(3))


>>>>>>> 2e695fcb7caf23d49e0f8f6f0dd14b242dcc92e8
def main(argv):
    dfs = []
    file_names = glob.glob('results/*.csv')
    for file_name in file_names:
        dfs.append(pd.read_csv(file_name))

    df = pd.concat(dfs)

    # sub_plots = [121, 122]
    x_labels = ['elasticity', 'patience']
    color_map_labels = ['patience', 'elasticity']
    file_names = ['elasticity.pdf', 'patience.pdf']
    for i in [0, 1]:
        x_label = x_labels[i]
        df = df.sort_values(x_label)
        x = df[x_label]
        y = df['Earnings']
        # plt.subplot(sub_plots[i])
        plt.scatter(x, y, c=df[color_map_labels[i]])
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), "r--")
        print("y=%.6fx+(%.6f)" % (z[0], z[1]))
        pr = stats.pearsonr(x, y)

        plt.title("Pearson-R correlation coefficient = {0}, p-value = {1}".format(pr[0].round(3), report_p(pr[1])))
        plt.xlabel(x_label)
        plt.ylabel("Earnings")
        plt.colorbar()
        plt.savefig('img/' + file_names[i])
        print("saved file to {0}".format('img/' + file_names[i]))
        print()

        # plt.show()


if __name__ == "__main__":
    main(sys.argv)
