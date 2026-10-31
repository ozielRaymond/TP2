import sympy as sp
import numpy as np

from sympy import Expr


class FonctionModel:
    __minimum: float
    __maximum: float
    __x: Expr
    __fonction: str
    __tangente: float

    def __init__(self, fonction, minimum, maximum, tangente):
        super().__init__()
        self.__x = sp.symbols('x')
        self.__fonction = fonction
        self.__minimum = minimum
        self.__maximum = maximum
        self.__tangente = tangente

    def derivee_texte(self):
        expr = sp.sympify(self.__fonction)
        derivee = sp.diff(expr, self.__x)
        return str(derivee)

    # Fonction Utilisé pour convertir l'expression expr en latex
    def derivee_latex(self):
        expr = sp.sympify(self.__fonction)
        derivee = sp.diff(expr, self.__x)
        return sp.latex(derivee)

    def get_y_tangente(self, x):
        return float(self.fonction(x))

    def get_taux_variation(self, value):
        return float(self.differentie(value))

    @property
    def tangente(self):
        return self.__tangente

    @tangente.setter
    def tangente(self, value):
        self.__tangente = value

    @property
    def minimum(self):
        return self.__minimum

    @property
    def maximum(self):
        return self.__maximum

    @minimum.setter
    def minimum(self, value):
        self.__minimum = value

    @maximum.setter
    def maximum(self, value):
        self.__maximum = value

    @property
    def variable(self):
        return self.__x

    @property
    def differentie(self):
        expr = sp.sympify(self.__fonction)
        derivee = sp.diff(expr, self.__x)

        if derivee.is_number:
            constante = float(derivee)
            return lambda x: np.broadcast_to(constante, np.shape(x))

        return sp.lambdify(self.__x, derivee, modules="numpy")

    @property
    def fonction(self):
        expr = sp.sympify(self.__fonction)

        if expr.is_number:
            constante = float(expr)
            return lambda x: np.broadcast_to(constante, np.shape(x))

        return sp.lambdify(self.__x, expr, modules="numpy")

    @fonction.setter
    def fonction(self, value):
        self.__fonction = value
