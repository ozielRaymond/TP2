from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import numpy as np

from fonctionmodel import FonctionModel


class MPLCanvas(FigureCanvasQTAgg):

    def __init__(self, model : FonctionModel, derivee : bool):
        self.__fig, self.__ax = plt.subplots(1, 2)
        super().__init__(self.__fig)
        self.dessiner(model, derivee)

    def dessiner(self, model : FonctionModel, derivee):

        x = np.linspace(0, 10, 500)

        y1 = model.fonction(x)


        #y1 = y1 * np.ones(len(x))
        #y2 = model.differentie()

        self.__ax[0].plot(x, y1)
        self.__ax[0].set_title("Graphe de f")

        self.__ax[1].plot(x, y1)
        self.__ax[1].set_title("Graphe de f'")
