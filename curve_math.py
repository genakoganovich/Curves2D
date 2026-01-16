"""Математические расчёты: касательные и нормали"""

import numpy as np
from curve_definition import r_function, dr_function


def compute_derivatives(theta):
    """
    Вычисляет производные dx/dθ и dy/dθ аналитически.

    Используется правило произведения:
        x = r·cos(θ)  →  dx/dθ = dr/dθ·cos(θ) - r·sin(θ)
        y = r·sin(θ)  →  dy/dθ = dr/dθ·sin(θ) + r·cos(θ)

    Args:
        theta: угол (скаляр или массив)

    Returns:
        tuple: (dx_dtheta, dy_dtheta)
    """
    r = r_function(theta)
    dr = dr_function(theta)

    dx_dtheta = dr * np.cos(theta) - r * np.sin(theta)
    dy_dtheta = dr * np.sin(theta) + r * np.cos(theta)

    return dx_dtheta, dy_dtheta


def compute_tangent_vector(theta):
    """
    Вычисляет единичный касательный вектор.

    T = (dx/dθ, dy/dθ) / ||(dx/dθ, dy/dθ)||

    Args:
        theta: угол (скаляр или массив)

    Returns:
        tuple: (tx, ty) компоненты единичного касательного вектора
    """
    dx, dy = compute_derivatives(theta)
    length = np.sqrt(dx ** 2 + dy ** 2)

    tx = dx / length
    ty = dy / length

    return tx, ty


def compute_normal_vector(theta):
    """
    Вычисляет единичный вектор нормали.

    Нормаль перпендикулярна касательной.
    Поворот на 90° против часовой: (tx, ty) → (-ty, tx)

    Args:
        theta: угол (скаляр или массив)

    Returns:
        tuple: (nx, ny) компоненты единичного вектора нормали
    """
    tx, ty = compute_tangent_vector(theta)

    nx = -ty
    ny = tx

    return nx, ny


def get_point_data(theta):
    """
    Получает полную информацию о точке на кривой.

    Args:
        theta: угол (скаляр)

    Returns:
        dict: словарь с координатами, касательной и нормалью
    """
    from curve_definition import get_cartesian_coordinates

    x, y = get_cartesian_coordinates(theta)
    tx, ty = compute_tangent_vector(theta)
    nx, ny = compute_normal_vector(theta)

    return {
        'theta': theta,
        'point': (x, y),
        'tangent': (tx, ty),
        'normal': (nx, ny)
    }


def get_multiple_points_data(theta_array):
    """
    Получает данные для массива точек.

    Args:
        theta_array: массив углов

    Returns:
        list: список словарей с данными точек
    """
    return [get_point_data(t) for t in theta_array]


def verify_orthogonality(theta):
    """
    Проверяет ортогональность касательной и нормали.

    Args:
        theta: угол

    Returns:
        float: скалярное произведение (должно быть ≈ 0)
    """
    tx, ty = compute_tangent_vector(theta)
    nx, ny = compute_normal_vector(theta)

    return tx * nx + ty * ny