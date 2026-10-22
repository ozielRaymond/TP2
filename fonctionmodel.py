import sympy as sp

from sympy import Expr

class FonctionModel:

    __borneA:float
    __borneB:float
    __x:Expr
    __fonction:Expr

    def __init__(self):
        super().__init__()
        self.__x = sp.symbols("x")
        self.__fonction = None

    @property
    def fonction(self):
        return self.__fonction

    @fonction.setter
    def fonction(self, value):
        expr = sp.sympify(value)
        self.__fonction = sp.lambdify(self.variable, expr, modules="numpy")

    @property
    def variable(self):
        return self.__x