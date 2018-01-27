import numpy as np
import matplotlib.pyplot as plt

money = [0, 15, 10, 20, 234, 23, 12, 5, 41, 3, 4]


def vis(Y):
    plt.ion()
    plt.show()
    # Y = $ value
    # T = final time
    T = len(Y)
    Ysub = []
    Tsub = []
    for t in range(0, T):
        print(t, Y[t])
        Ysub.append(Y[t])
        Tsub.append(t)
        #plt.title("UofTrader $")
        plt.plot(Tsub, Ysub, '-')
        #plt.axis([0, 10, 0, 20])
        plt.show()
        plt.pause(0.1)

    return

if __name__ == "__main__":
    vis(money)
    
    