"""Механизм выбора произвольных точек на кривой"""

import numpy as np
from config import NUM_RANDOM_POINTS, RANDOM_SEED


def select_random_points(num_points=None, seed=None):
    """
    Выбирает случайные значения θ на кривой.

    Args:
        num_points: количество точек (по умолчанию из config)
        seed: зерно для воспроизводимости (по умолчанию из config)

    Returns:
        numpy.ndarray: отсортированный массив углов θ
    """
    if num_points is None:
        num_points = NUM_RANDOM_POINTS
    if seed is None:
        seed = RANDOM_SEED

    np.random.seed(seed)
    theta_points = np.random.uniform(0, 2 * np.pi, num_points)

    return np.sort(theta_points)


def select_uniform_points(num_points=10):
    """
    Выбирает равномерно распределённые точки.

    Args:
        num_points: количество точек

    Returns:
        numpy.ndarray: массив углов θ
    """
    return np.linspace(0, 2 * np.pi, num_points, endpoint=False)


def select_custom_points(theta_list):
    """
    Использует пользовательский список углов.

    Args:
        theta_list: список или массив углов

    Returns:
        numpy.ndarray: отсортированный массив углов
    """
    return np.sort(np.array(theta_list))