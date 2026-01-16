"""Дополнительная визуализация — добавление касательных"""

import matplotlib.pyplot as plt
from curve_definition import get_cartesian_coordinates
from curve_math import compute_tangent_vector
from config import VECTOR_SCALE, TANGENT_COLOR, VECTOR_LINEWIDTH


def add_tangents_to_plot(ax, theta_points, scale=None):
    """
    Добавляет касательные векторы на график.

    Args:
        ax: объект осей matplotlib
        theta_points: массив углов θ для точек
        scale: масштаб векторов (по умолчанию из config)

    Returns:
        list: список данных касательных [{'point': (x,y), 'vector': (tx,ty)}, ...]
    """
    if scale is None:
        scale = VECTOR_SCALE

    tangents_data = []

    for theta in theta_points:
        x, y = get_cartesian_coordinates(theta)
        tx, ty = compute_tangent_vector(theta)

        tangents_data.append({
            'point': (x, y),
            'vector': (tx, ty)
        })

        # Рисуем касательную
        ax.annotate('',
                    xy=(x + tx * scale, y + ty * scale),
                    xytext=(x, y),
                    arrowprops=dict(arrowstyle='->',
                                    color=TANGENT_COLOR,
                                    lw=VECTOR_LINEWIDTH))

    return tangents_data


def add_tangents_legend(ax):
    """
    Добавляет касательные в легенду.

    Args:
        ax: объект осей matplotlib
    """
    ax.plot([], [], color=TANGENT_COLOR, linewidth=VECTOR_LINEWIDTH,
            label='Касательная')


if __name__ == '__main__':
    from visualization_base import create_figure, draw_curve, setup_axes
    from visualization_points import add_points_to_plot, add_points_legend
    from point_selector import select_random_points

    fig, ax = create_figure()
    draw_curve(ax)

    theta_points = select_random_points(10)
    add_points_to_plot(ax, theta_points)
    add_tangents_to_plot(ax, theta_points)

    add_points_legend(ax)
    add_tangents_legend(ax)

    setup_axes(ax, title='Кривая с точками и касательными')
    ax.legend(fontsize=12, loc='upper right')

    plt.show()