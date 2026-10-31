from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import numpy as np

from fonctionmodel import FonctionModel


class MPLCanvas(FigureCanvasQTAgg):

    def __init__(self, model : FonctionModel, show_grid = False, colors=None):
        # Implémentation suggérée par l'IA de self.__fig = Figure() au lieu de self.__fig, self.__ax
        # permet de créer une figure indépendante à chaque fois au lieu d'accumuler les fonctions dans le subplot
        self.__fig = Figure()
        self.__ax = self.__fig.subplots(1, 2)

        self.__fig.subplots_adjust(bottom=0.25)

        if colors is not None:
            self.colors = colors
        else:
            self.colors = {'f':"blue", "f'":"blue", "t":"blue"}

        self.show_grid = show_grid

        super().__init__(self.__fig)
        self.dessiner(model)

    def dessiner(self, model : FonctionModel):
        x0 = model.tangente

        x = np.linspace(model.minimum, model.maximum, 500)

        y1 = model.fonction(x)
        y2 = model.differentie(x)

        self.__ax[0].plot(x, y1, color=self.colors["f"])
        self.__ax[0].set_title("Graphe de f(x)")
        self.__ax[0].grid(self.show_grid)

        self.__ax[1].plot(x, y2, color=self.colors["f'"])
        self.__ax[1].set_title("Graphe de f'(x)")
        self.__ax[1].grid(self.show_grid)

        #Aide de l'IA pour afficher la tangente
        if model.minimum <= x0 <= model.maximum:
            y0 = model.fonction(np.array([x0]))[0]
            m0 = float(model.differentie(x0))

            delta = (model.maximum - model.minimum) / 20
            x_tangente = np.linspace(x0 - delta, x0 + delta, 100)
            y_tangente = m0 * (x_tangente - x0) + y0

            b = y0 - m0 * x0

            label_tangente = f"y = {m0:.2f}x {b:+.2f}"

            self.__ax[0].plot(x_tangente, y_tangente, color=self.colors['t'], linestyle='-', label=label_tangente)
            self.__ax[0].scatter([x0], [y0], color=self.colors['t'], s=25, zorder=5)
            self.__ax[0].set_xlim(model.minimum, model.maximum)

            self.__ax[1].vlines(x=x0, ymin=m0, ymax=m0 + 0.4, color=self.colors['t'], linestyle='-', label=f"{m0:.2f}")


        #Aide de l'IA pour correctement agencer les légendes
        self.__ax[0].legend(loc='lower center', bbox_to_anchor=(0.5, -0.37), framealpha=0.8, ncol=1)
        self.__ax[1].legend(loc='lower center', bbox_to_anchor=(0.5, -0.37), framealpha=0.8, ncol=1)