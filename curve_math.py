"""Математические расчёты: касательные, нормали и кривизна"""

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


def compute_second_derivatives(theta):
    """
    Вычисляет вторые производные d²x/dθ² и d²y/dθ² аналитически.

    Используется дифференцирование первых производных:
        dx/dθ = dr/dθ·cos(θ) - r·sin(θ)
        d²x/dθ² = d²r/dθ²·cos(θ) - 2·dr/dθ·sin(θ) - r·cos(θ)

        dy/dθ = dr/dθ·sin(θ) + r·cos(θ)
        d²y/dθ² = d²r/dθ²·sin(θ) + 2·dr/dθ·cos(θ) - r·sin(θ)

    Args:
        theta: угол (скаляр или массив)

    Returns:
        tuple: (d2x_dtheta2, d2y_dtheta2)
    """
    r = r_function(theta)
    dr = dr_function(theta)
    d2r = d2r_function(theta)

    d2x_dtheta2 = (d2r * np.cos(theta) -
                   2 * dr * np.sin(theta) -
                   r * np.cos(theta))

    d2y_dtheta2 = (d2r * np.sin(theta) +
                   2 * dr * np.cos(theta) -
                   r * np.sin(theta))

    return d2x_dtheta2, d2y_dtheta2


def d2r_function(theta):
    """
    Вторая производная d²r/dθ² (аналитически).

    r(θ) = 1 + 0.3·cos(2θ) + 0.2·sin(3θ) + 0.1·cos(7θ) + 0.05·sin(11θ)
    dr/dθ = -0.6·sin(2θ) + 0.6·cos(3θ) - 0.7·sin(7θ) + 0.55·cos(11θ)
    d²r/dθ² = -1.2·cos(2θ) - 1.8·sin(3θ) - 4.9·cos(7θ) - 6.05·sin(11θ)

    Args:
        theta: угол (скаляр или массив)

    Returns:
        float или numpy.ndarray: значение второй производной
    """
    return (-0.3 * 4 * np.cos(2 * theta) -      # -1.2·cos(2θ)
            0.2 * 9 * np.sin(3 * theta) -        # -1.8·sin(3θ)
            0.1 * 49 * np.cos(7 * theta) -       # -4.9·cos(7θ)
            0.05 * 121 * np.sin(11 * theta))     # -6.05·sin(11θ)


def compute_curvature(theta):
    """
    Вычисляет кривизну κ (каппа) в точке.

    Формула кривизны для параметрической кривой:
        κ = |x'·y'' - y'·x''| / (x'² + y'²)^(3/2)

    где x' = dx/dθ, y' = dy/dθ, x'' = d²x/dθ², y'' = d²y/dθ²

    Args:
        theta: угол (скаляр или массив)

    Returns:
        float или numpy.ndarray: значение кривизны
    """
    dx, dy = compute_derivatives(theta)
    d2x, d2y = compute_second_derivatives(theta)

    numerator = np.abs(dx * d2y - dy * d2x)
    denominator = (dx**2 + dy**2) ** 1.5

    curvature = numerator / denominator

    return curvature


def compute_radius_of_curvature(theta):
    """
    Вычисляет радиус кривизны R = 1/κ.

    Радиус кривизны — это радиус окружности, которая лучше всего
    приближает кривую в данной точке (соприкасающаяся окружность).

    R = (x'² + y'²)^(3/2) / |x'·y'' - y'·x''|

    Args:
        theta: угол (скаляр или массив)

    Returns:
        float или numpy.ndarray: радиус кривизны
    """
    curvature = compute_curvature(theta)

    # Защита от деления на ноль (в точках перегиба κ → 0, R → ∞)
    with np.errstate(divide='ignore', invalid='ignore'):
        radius = np.where(curvature > 1e-10, 1.0 / curvature, np.inf)

    return radius


def compute_curvature_center(theta):
    """
    Вычисляет центр кривизны (центр соприкасающейся окружности).

    Центр кривизны находится на расстоянии R от точки кривой
    в направлении нормали.

    Формулы:
        x_c = x - y'·(x'² + y'²) / (x'·y'' - y'·x'')
        y_c = y + x'·(x'² + y'²) / (x'·y'' - y'·x'')

    Args:
        theta: угол (скаляр или массив)

    Returns:
        tuple: (x_center, y_center) координаты центра кривизны
    """
    from curve_definition import get_cartesian_coordinates

    x, y = get_cartesian_coordinates(theta)
    dx, dy = compute_derivatives(theta)
    d2x, d2y = compute_second_derivatives(theta)

    # Знаменатель (определяет направление)
    denom = dx * d2y - dy * d2x

    # Защита от деления на ноль
    with np.errstate(divide='ignore', invalid='ignore'):
        factor = (dx**2 + dy**2) / denom

        x_center = x - dy * factor
        y_center = y + dx * factor

    return x_center, y_center


def compute_signed_curvature(theta):
    """
    Вычисляет знаковую кривизну.

    Положительная кривизна — кривая поворачивает влево.
    Отрицательная кривизна — кривая поворачивает вправо.

    κ_signed = (x'·y'' - y'·x'') / (x'² + y'²)^(3/2)

    Args:
        theta: угол (скаляр или массив)

    Returns:
        float или numpy.ndarray: знаковая кривизна
    """
    dx, dy = compute_derivatives(theta)
    d2x, d2y = compute_second_derivatives(theta)

    numerator = dx * d2y - dy * d2x
    denominator = (dx**2 + dy**2) ** 1.5

    return numerator / denominator


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
    length = np.sqrt(dx**2 + dy**2)

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
        dict: словарь с координатами, касательной, нормалью и кривизной
    """
    from curve_definition import get_cartesian_coordinates

    x, y = get_cartesian_coordinates(theta)
    tx, ty = compute_tangent_vector(theta)
    nx, ny = compute_normal_vector(theta)
    curvature = compute_curvature(theta)
    radius = compute_radius_of_curvature(theta)
    x_center, y_center = compute_curvature_center(theta)

    return {
        'theta': theta,
        'point': (x, y),
        'tangent': (tx, ty),
        'normal': (nx, ny),
        'curvature': curvature,
        'radius_of_curvature': radius,
        'curvature_center': (x_center, y_center)
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


# === Дополнительные утилиты ===

def get_curvature_extremes(num_samples=1000):
    """
    Находит точки с максимальной и минимальной кривизной.

    Args:
        num_samples: количество точек для поиска

    Returns:
        dict: информация о экстремумах кривизны
    """
    theta_samples = np.linspace(0, 2 * np.pi, num_samples)
    curvatures = compute_curvature(theta_samples)

    max_idx = np.argmax(curvatures)
    min_idx = np.argmin(curvatures)

    return {
        'max_curvature': {
            'theta': theta_samples[max_idx],
            'curvature': curvatures[max_idx],
            'radius': 1.0 / curvatures[max_idx] if curvatures[max_idx] > 0 else np.inf
        },
        'min_curvature': {
            'theta': theta_samples[min_idx],
            'curvature': curvatures[min_idx],
            'radius': 1.0 / curvatures[min_idx] if curvatures[min_idx] > 0 else np.inf
        },
        'mean_curvature': np.mean(curvatures)
    }