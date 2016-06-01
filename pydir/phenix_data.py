
import numpy as np
import matplotlib.pyplot as plt

Npart = np.array([350.9, 297.9, 251.0, 211.0, 176.3, 146.8, 120.9, 98.3, 78.7, 61.9, 47.6, 35.6])
Npart_err = np.array([4.7, 6.6, 7.3, 7.3, 7.0, 7.1, 7.0, 6.8, 6.1, 5.2, 4.9, 5.1])

dNch = np.array([687.4, 560.4, 456.8, 371.5, 302.5, 245.6, 197.2, 156.4, 123.5, 95.3, 70.9, 52.2])
dNch_err = np.array([36.6, 27.9, 22.3, 18.2, 15.8, 13.8, 12.2, 10.9, 9.6, 8.6, 7.6, 6.5])


plt.errorbar(Npart,dNch, xerr = Npart_err, yerr = dNch_err)
plt.title("dN$_{ch}$/d$\eta$ vs. N$_{part}$")
plt.ylabel("dN$_{ch}$/d$\eta$")
plt.xlabel("N$_{part}$")
plt.show()
