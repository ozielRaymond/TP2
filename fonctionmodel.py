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

        # Bloc proposé par l'IA
        # Évite les erreurs quand la dérivée est une constante
        if derivee.is_number:
            constante = float(derivee)
            return lambda x : np.full_like(x, constante)

        return sp.lambdify(self.__x, derivee, modules="numpy")

    def derivee_text(self):
        expr = sp.sympify(self.__fonction)
        derivee = sp.diff(expr, self.__x)
        return str(derivee)

    @property
    def fonction(self):
        expr = sp.sympify(self.__fonction)

        # Bloc proposé par l'IA
        # Évite les erreurs quand la fonction est une constante
        if expr.is_number:
            # noinspection PyTypeChecker
            constante = float(expr)
            return lambda x: np.full_like(x, constante)

        return sp.lambdify(self.__x, expr, modules="numpy")

    @fonction.setter
    def fonction(self, value):
        self.__fonction = value
