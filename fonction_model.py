import sympy as sp
import numpy as np

from sympy import Expr


# L'IA a été consultée et utilisée dans cette classe
# pour contribuer à la documentation et
# me guider pour la gestion du LaTex

class FonctionModel:
    """Modèle représentant une fonction et ses propriétés

    Attributs :
        __minimum (float) : Borne inférieure de la fonction
        __maximum (float) : Borne supérieure de la fonction
        __x (expr) : Symbole sympy représentant la variable indépendante
        __fonction (str) : expression en texte de la fonction mathématique
        __tangente (float) : point d'évaluation de la tangente
    """

    __minimum: float
    __maximum: float
    __x: Expr
    __fonction: str
    __tangente: float

    def __init__(self, fonction, minimum, maximum, tangente):
        """Initialise FonctionModel.

        Args :
            fonction (str) : L'expression mathématique de la fonction
            minimum (float) : Borne inférieur de la fonction
            maximum (float) : Borne supérieur de la fonction
            tangente (float) : point d'évaluation de la tangente
        """
        super().__init__()
        self.__x = sp.symbols('x')
        self.__fonction = fonction
        self.__minimum = minimum
        self.__maximum = maximum
        self.__tangente = tangente

    def derivee_texte(self):
        """Calcule la dérivée symbolique de la fonction et la retourne en string.

        Returns :
            str : Représentation textuelle de f'(x).
        """
        expr = sp.sympify(self.__fonction)
        derivee = sp.diff(expr, self.__x)
        return str(derivee)

    # La fonction sympy sp.latex permet d'obtenir l'expression en LaTex.
    def derivee_latex(self):
        """Convertit l'expression de la dérivée en LaTex.

        Returns :
            str : Expression de f'(x) formatée en LaTeX.
        """
        expr = sp.sympify(self.__fonction)
        derivee = sp.diff(expr, self.__x)
        return sp.latex(derivee)

    def get_y_tangente(self, x):
        """Calcule la valeur de f(x) au point spécifié.

        Args :
            x (float) : Le point spécifié

        Returns :
            float : La valeur de la fonction en x.
        """
        return float(self.fonction(x))

    def get_taux_variation(self, value):
        """Calcule le taux de variation instantané au point spécifié.

        Args :
            value (float) : Le point spécifié

        Returns :
            float : La valeur de la dérivée en value.
        """
        return float(self.differentie(value))

    @property
    def tangente(self):
        """float : Obtient la valeur de x du point de tangente."""
        return self.__tangente

    @tangente.setter
    def tangente(self, value):
        """Définit la valeur x du point de tangente."""
        self.__tangente = value

    @property
    def minimum(self):
        """float : Obtient la borne inférieure de la fonction."""
        return self.__minimum

    @property
    def maximum(self):
        """float : Obtient la borne supérieure de la fonction."""
        return self.__maximum

    @minimum.setter
    def minimum(self, value):
        """Définit la borne inférieure de la fonction."""
        self.__minimum = value

    @maximum.setter
    def maximum(self, value):
        """Définit la borne supérieure de la fonction."""
        self.__maximum = value

    @property
    def variable(self):
        """Expr : Obtient le symbole SymPy utilisé pour la variable 'x'."""
        return self.__x

    @property
    def differentie(self):
        """Génère une fonction NumPy évaluant la dérivée.

        Returns :
            callable: Une fonction NumPy acceptant des scalaires ou des tableaux ndarray.
        """
        expr = sp.sympify(self.__fonction)
        derivee = sp.diff(expr, self.__x)

        if derivee.is_number:
            constante = float(derivee)
            return lambda x: np.broadcast_to(constante, np.shape(x))

        return sp.lambdify(self.__x, derivee, modules="numpy")

    @property
    def fonction(self):
        """Génère une fonction vectorisée NumPy évaluant f(x).

        Returns :
            callable : Une fonction NumPy acceptant des scalaires ou des tableaux ndarray.
        """
        expr = sp.sympify(self.__fonction)

        if expr.is_number:
            constante = float(expr)
            return lambda x: np.broadcast_to(constante, np.shape(x))

        return sp.lambdify(self.__x, expr, modules="numpy")

    @fonction.setter
    def fonction(self, value):
        """Définit l'expression textuelle de la fonction mathématique."""
        self.__fonction = value
