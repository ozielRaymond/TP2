import sympy as sp

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
        derivee = sp.diff(expr, self.__x) + 0 * self.__x
        return sp.lambdify(self.__x, derivee, modules="numpy")

    @property
    def fonction(self):
        expr = sp.sympify(self.__fonction)
        return sp.lambdify(self.__x, expr, modules="numpy")

    @fonction.setter
    def fonction(self, value):
        self.__fonction = value
