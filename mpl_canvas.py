from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import numpy as np

from fonctionmodel import FonctionModel


class MPLCanvas(FigureCanvasQTAgg):

    def __init__(self, model : FonctionModel):
        self.__fig, self.__ax = plt.subplots()
        super().__init__(self.__fig)
        self.dessiner(model)

    def dessiner(self, model):

        x = np.linspace(model.minimum, model.maximum, 500)
        y1 = model.fonction(x)

        y1 = y1 * np.ones(len(x))
        #y2 = model.differentie()

        self.__ax.plot(x, y1)
        self.__ax.set_title("Graphe de f")

        #self.__ax.plot(x, y2)
        #self.__ax.set_title("Graphe de f'")
