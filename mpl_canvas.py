from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import numpy as np

from fonctionmodel import FonctionModel


class MPLCanvas(FigureCanvasQTAgg):

    def __init__(self, model : FonctionModel, show_grid = False, colors="None"):
        # Implémentation suggérée par l'IA de self.__fig = Figure() au lieu de self.__fig, self.__ax
        # permet de créer une figure indépendante à chaque fois au lieu d'accumuler les fonctions dans le subplot
        self.__fig = Figure()
        self.__ax = self.__fig.subplots(1, 2)

        if colors is not None:
            self.colors = colors
        else:
            self.colors = {'f':"blue", "f'":"blue", "t":"blue"}

        self.show_grid = show_grid

        super().__init__(self.__fig)
        self.dessiner(model)

    def dessiner(self, model : FonctionModel):
        x = np.linspace(model.minimum, model.maximum, 500)

        y1 = model.fonction(x)
        y2 = model.differentie(x)

        self.__ax[0].plot(x, y1, color=self.colors["f"])
        self.__ax[0].set_title("Graphe de f(x)")
        self.__ax[0].grid(self.show_grid)

        self.__ax[1].plot(x, y2, color=self.colors["f'"])
        self.__ax[1].set_title("Graphe de f'(x)")
        self.__ax[1].grid(self.show_grid)
