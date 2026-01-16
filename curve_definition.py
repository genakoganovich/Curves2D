"""Определение параметрической кривой (клякса)"""

import numpy as np


def r_function(theta):
    """
    Радиус-функция r(θ) для полярных координат.

    Кривая: r(θ) = 1 + 0.3·cos(2θ) + 0.2·sin(3θ) + 0.1·cos(7θ) + 0.05·sin(11θ)
    """
    return (1 +
            0.3 * np.cos(2 * theta) +
            0.2 * np.sin(3 * theta) +
            0.1 * np.cos(7 * theta) +
            0.05 * np.sin(11 * theta))


def dr_function(theta):
    """
    Производная dr/dθ (аналитически).

    dr/dθ = -0.6·sin(2θ) + 0.6·cos(3θ) - 0.7·sin(7θ) + 0.55·cos(11θ)
    """
    return (-0.3 * 2 * np.sin(2 * theta) +
            0.2 * 3 * np.cos(3 * theta) -
            0.1 * 7 * np.sin(7 * theta) +
            0.05 * 11 * np.cos(11 * theta))


def get_cartesian_coordinates(theta):
    """
    Преобразование из полярных в декартовы координаты.

    x(θ) = r(θ)·cos(θ)
    y(θ) = r(θ)·sin(θ)

    Returns:
        tuple: (x, y) координаты
    """
    r = r_function(theta)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


def get_curve_points(num_points=1000):
    """
    Генерирует массив точек кривой.

    Args:
        num_points: количество точек

    Returns:
        tuple: (theta, x, y) массивы
    """
    theta = np.linspace(0, 2 * np.pi, num_points)
    x, y = get_cartesian_coordinates(theta)
    return theta, x, y