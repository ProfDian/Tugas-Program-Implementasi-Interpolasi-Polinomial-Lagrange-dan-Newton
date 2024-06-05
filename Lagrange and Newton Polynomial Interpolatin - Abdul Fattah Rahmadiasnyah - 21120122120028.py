banner = """
====================================================
||          Program Implementasi Interpolasi      ||
||               Lagrange dan Newton              ||
||                                                ||
||             Abdul Fattah Rahmadiansyah         ||
||                  21120122120028                ||
====================================================
"""

print(banner)

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt


class LagrangeInterpolation:
    def __init__(self, Tegangan, Waktu_Patah):
        self.Tegangan = Tegangan
        self.Waktu_Patah = Waktu_Patah
    
    def interpolate(self, x):
        total = 0
        n = len(self.Tegangan)
        for i in range(n):
            term = self.Waktu_Patah[i]
            for j in range(n):
                if j != i:
                    term = term * (x - self.Tegangan[j]) / (self.Tegangan[i] - self.Tegangan[j])
            total += term
        return total

    def get_polynomial(self):
        x = sp.symbols('x')
        total = 0
        n = len(self.Tegangan)
        for i in range(n):
            term = self.Waktu_Patah[i]
            for j in range(n):
                if j != i:
                    term *= (x - self.Tegangan[j]) / (self.Tegangan[i] - self.Tegangan[j])
            total += term
        return sp.simplify(total)
    
    def plot(self, x_test):
        y_test = [self.interpolate(xi) for xi in x_test]
        plt.plot(self.Tegangan, self.Waktu_Patah, 'ro', label='Data points')
        plt.plot(x_test, y_test, label='Lagrange Interpolation')
        plt.xlabel('Tegangan (kg/mm^2)')
        plt.ylabel('Waktu Patah (jam)')
        plt.legend()
        plt.title('Lagrange Interpolation')
        plt.show()

class NewtonInterpolation:
    def __init__(self, Tegangan, Waktu_Patah):
        self.Tegangan = Tegangan
        self.Waktu_Patah = Waktu_Patah
        self.divided_diff_table = self.divided_diff()
    
    def divided_diff(self):
        n = len(self.Tegangan)
        divided_diff_table = np.zeros([n, n])
        divided_diff_table[:, 0] = self.Waktu_Patah

        for j in range(1, n):
            for i in range(n - j):
                divided_diff_table[i][j] = (divided_diff_table[i + 1][j - 1] - divided_diff_table[i][j - 1]) / (self.Tegangan[i + j] - self.Tegangan[i])
        
        return divided_diff_table[0, :]
    
    def interpolate(self, x):
        n = len(self.Tegangan)
        result = self.divided_diff_table[0]
        for i in range(1, n):
            term = self.divided_diff_table[i]
            for j in range(i):
                term *= (x - self.Tegangan[j])
            result += term
        return result

    def get_polynomial(self):
        x = sp.symbols('x')
        n = len(self.Tegangan)
        result = 0
        for i in range(n):
            term = self.divided_diff_table[i]
            for j in range(i):
                term *= (x - self.Tegangan[j])
            result += term
        return sp.simplify(result)
    
    def plot(self, x_test):
        y_test = [self.interpolate(xi) for xi in x_test]
        plt.plot(self.Tegangan, self.Waktu_Patah, 'ro', label='Data points')
        plt.plot(x_test, y_test, label='Newton Interpolation')
        plt.xlabel('Tegangan (kg/mm^2)')
        plt.ylabel('Waktu Patah (jam)')
        plt.legend()
        plt.title('Newton Interpolation')
        plt.show()

# Data points
Tegangan = np.array([5, 10, 15, 20, 25, 30, 35, 40])
Waktu_Patah = np.array([40, 30, 25, 40, 18, 20, 22, 15])

# Mencoba Interpolasi Lagrange
lagrange_test = np.linspace(5, 40)
lagrange = LagrangeInterpolation(Tegangan, Waktu_Patah)
lagrange.plot(lagrange_test)

# Membuat fungsi polinomial lagrange
lagrange_poly = lagrange.get_polynomial()
print(f"Fungsi Polinomial hasil Interpolasi Lagrange:\n {lagrange_poly.expand()}")

# Mencoba Interpolasi Newton
newton_test = np.linspace(5, 40)
newton = NewtonInterpolation(Tegangan, Waktu_Patah)
newton.plot(newton_test)

# Membuat gungsi polinomial newton
newton_poly = newton.get_polynomial()
print(f"Fungsi Polinomial hasil Interpolasi Newton:\n {lagrange_poly.expand()}")
