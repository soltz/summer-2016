
import numpy as np
import matplotlib.pyplot as plt

#   200 GeV Au Au
Npart1 = np.array([350.9, 297.9, 251.0, 211.0, 176.3, 146.8, 120.9, 98.3, 78.7, 61.9, 47.6, 35.6])
Npart_err1 = np.array([4.7, 6.6, 7.3, 7.3, 7.0, 7.1, 7.0, 6.8, 6.1, 5.2, 4.9, 5.1])
dNch1 = np.array([687.4, 560.4, 456.8, 371.5, 302.5, 245.6, 197.2, 156.4, 123.5, 95.3, 70.9, 52.2])
dNch_err1 = np.array([36.6, 27.9, 22.3, 18.2, 15.8, 13.8, 12.2, 10.9, 9.6, 8.6, 7.6, 6.5])

#   130 GeV Au Au
Npart2 = np.array([347.7, 294.0, 249.5, 211.0, 178.6, 149.7, 124.8, 102.9, 83.2, 66.3, 52.1, 40.1])
Npart_err2 = np.array([10.0, 8.9, 8.0, 7.2, 6.6, 6.0, 5.5, 5.1, 4.7, 4.3, 4, 3.8])
dNch2 = np.array([601.8, 488.5, 402.7, 328.8, 270.5, 219.3, 175.7, 139.0, 109.4, 84.1, 64.3, 48.4])
dNch_err2 = np.array([28.4, 21.6, 17.4, 15.2, 12.8, 11.4, 10.3, 9.1, 8.4, 7.0, 6.3, 5.4])

#   62.4 GeV Au Au
Npart3 = np.array([342.6, 291.3, 244.5, 205.0, 171.3, 142.2, 116.7, 95.2, 76.1, 59.9, 46.8, 35.8])
Npart_err3 = np.array([4.9, 7.3, 8.9, 9.6, 8.9, 8.5, 8.9, 7.7, 7.7, 6.9, 5.2, 4.6])
dNch3 = np.array([447.5, 367.4, 301.8, 248.0, 203.0, 165.1, 133.0, 105.9, 83.0, 63.9, 48.4, 35.8])
dNch_err3 = np.array([38.9, 31.6, 25.8, 21.0, 17.1, 13.8, 11.1, 8.76, 6.83, 5.24, 3.95, 2.92])

#   39 GeV Au Au
Npart4 = np.array([340.0, 289.6, 244.1, 206.5, 174.1, 145.8, 120.8, 98.6, 79.8, 63.9, 50.3])
Npart_err4 = np.array([7.4, 8.1, 6.4, 6.3, 6.3, 6.2, 7.5, 6.4, 6.0, 5.8, 5.5])
dNch4 = np.array([363.2, 297.8, 246.6, 204.4, 168.9, 138.3, 112.6, 90.6, 72.1, 56.8, 43.7])
dNch_err4 = np.array([31.6, 25.8, 21.3, 17.5, 14.4, 11.8, 9.6, 7.7, 6.1, 4.8, 3.7])

#   27 GeV Au Au
Npart5 = np.array([338.9, 288.8, 244.3, 205.7, 173.0, 144.6, 110.4, 97.6, 77.9, 60.8])
Npart_err5 = np.array([3.1, 4.7, 6.5, 5.8, 5.5, 6.2, 6.1, 5.8, 5.7, 6.0])
dNch5 = np.array([321.2, 258.7, 212.6, 175.0, 143.5, 116.7, 94.2, 75.0, 59.0, 45.7])
dNch_err5 = np.array([28.1, 22.5, 18.5, 15.1, 12.4, 10.0, 8.1, 6.4, 5.0, 3.9])

#   19.6 GeV Au Au
Npart6 = np.array([338.5, 288.3, 242.4, 204.3, 172.4, 143.5, 117.9, 95.7, 77.4, 61.7])
Npart_err6 = np.array([4.4, 6.0, 6.1, 5.7, 7.3, 6.6, 6.7, 6.9, 5.7, 4.8])
dNch6 = np.array([285.3, 229.3, 188.8, 155.7, 128.2, 104.8, 85.1, 68.4, 54.3, 42.4])
dNch_err6 = np.array([25.1, 20.1, 16.5, 13.5, 11.1, 9.1, 7.4, 5.9, 4.7, 3.7])

#   14.5 GeV Au Au
Npart7 = np.array([337.3, 287.7, 242.5, 205.1, 172.6, 143.6, 119.2, 98.4, 80.2, 63.9])
Npart_err7 = np.array([4.2, 4.9, 5.5, 5.9, 6.4, 7.8, 7.2, 5.8, 5.6, 4.7])
dNch7 = np.array([250.9, 201.2, 164.5, 134.7, 110.0, 89.4, 72.0, 57.4, 45.2, 34.9])
dNch_err7 = np.array([22.2, 17.7, 14.5, 11.8, 9.6, 7.8, 6.3, 5.0, 3.9, 3.0])

#   7.7 GeV Au Au
Npart8 = np.array([332.1, 283.2, 240.1, 204.1, 172.9, 145.5, 121.0, 98.2, 78.8, 61.8])
Npart_err8 = np.array([5.4, 5.9, 5.7, 5.7, 6.7, 7.2, 7.3, 7.0, 6.7, 6.5])
dNch8 = np.array([192.4, 159.2, 129.3, 105.4, 85.6, 68.8, 55.0, 43.5, 33.9, 26.1])
dNch_err8 = np.array([16.9, 14.0, 11.3, 9.2, 7.5, 6.0, 4.8, 3.8, 3.0, 2.3])


plt.figure(1)

plt.title("Au + Au")
plt.ylabel("dN$_{ch}$/d$\eta$")
plt.xlabel("N$_{part}$")
plt.errorbar(Npart1,dNch1, xerr = Npart_err1, yerr = dNch_err1, label = '200 GeV')
plt.errorbar(Npart2,dNch2, xerr = Npart_err2, yerr = dNch_err2, label = '130 GeV')
plt.errorbar(Npart3,dNch3, xerr = Npart_err3, yerr = dNch_err3, label = '62.4 GeV')
plt.errorbar(Npart4,dNch4, xerr = Npart_err4, yerr = dNch_err4, label = '39 GeV')
plt.errorbar(Npart5,dNch5, xerr = Npart_err5, yerr = dNch_err5, label = '27 GeV')
plt.errorbar(Npart6,dNch6, xerr = Npart_err6, yerr = dNch_err6, label = '19.6 GeV')
plt.errorbar(Npart7,dNch7, xerr = Npart_err7, yerr = dNch_err7, label = '14.5 GeV')
plt.errorbar(Npart8,dNch8, xerr = Npart_err8, yerr = dNch_err8, label = '7.7 GeV')
plt.legend(loc = 0)

plt.show()
