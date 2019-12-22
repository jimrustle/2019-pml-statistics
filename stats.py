# 2019 Princess Margaret Lottery
# 500 000 total tickets (ticket numbers = 0 to 50000)
# use python3.5+

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sp

winning_numbers = []

# open winners list and read in data
with open("winners.txt", "r") as f:
    for line in f:
        winning_numbers.append(int(line))

winning_numbers = np.array(winning_numbers)

# plot histogram for bins from 10 to 1000, also use Freedman-Diaconis rule for best bin number
bins = [10, 25, 50, 100, 250, 500, 1000]

iqr = np.subtract(*np.percentile(winning_numbers, [75, 25]))
h = 2.0 * iqr / (500000**(1/3))
fd_bins = int(500000/h)
bins.append(fd_bins)
bins.sort()

# plot histograms, save to file
fig = plt.figure()
for i, bin in enumerate(bins):
    ax = plt.subplot(421 + i)
    plt.hist(winning_numbers, bins=bin)
    ax.title.set_text("bins = {}".format(bin))
fig.suptitle('2019 Princess Margaret Lotto Winning Numbers Histograms', fontsize=13)
plt.tight_layout()
plt.show()
plt.close()

# plot a CDF of the winning numbers, using FD bin number
mu = np.mean(winning_numbers)
sigma = np.std(winning_numbers)
fig = plt.figure()
for i, bin in enumerate(bins):
    ax = plt.subplot(421 + i)
    ax.title.set_text("bins = {}".format(bin))
    _, bins, _ = plt.hist(winning_numbers, bins=bin, density=True, histtype='step', cumulative=True)

    # the theoretical CDF of a uniform distribution is a line, in this case from (0, 0) to (500000, 1)
    plt.plot([0, 500000], [0, 1], 'k--', linewidth=1.5, label='Theoretical')

fig.suptitle('2019 Princess Margaret Lotto Winning Numbers CDFs', fontsize=13)
plt.tight_layout()
plt.show()
plt.close()

print("Mean: {}, expected: {}".format(mu, 500000/2.0))
print("Variance: {}, expected: {}".format(sigma**2, ((500000 + 1)**2 - 1) / 12.0))
print("Skewness: {}, expected: 0".format(sp.skew(winning_numbers)))
print("Entropy: {}, expected: {}".format(sp.entropy(np.unique(winning_numbers, return_counts=True)[1]),
                                         np.log(len(winning_numbers))))

# calculate chi-squared test (see https://www.cse.wustl.edu/~jain/cse567-08/ftp/k_27trg.pdf)
# use 80 bins since it's close to the FD bin number, and divides 500e3 easily
hist, _ = np.histogram(winning_numbers, bins=80)
expected = np.ones(80) * len(winning_numbers) / 80.0
c2 = sp.chisquare(hist, expected)
print("Chi-squared: {}".format(c2))

