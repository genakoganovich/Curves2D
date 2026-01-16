"""Дополнительная визуализация — добавление нормалей"""

import matplotlib.pyplot as plt
from curve_definition import get_cartesian_coordinates
from curve_math import compute_normal_vector
from config import VECTOR_SCALE, NORMAL_COLOR, VECTOR_LINEWIDTH


def add_normals_to_plot(ax, theta_points, scale=None):
    """
    Добавляет векторы нормалей на график.

    Args:
        ax: объект осей matplotlib
        theta_points: массив углов θ для точек
        scale: масштаб векторов (по умолчанию из config)

    Returns:
        list: список данных нормалей [{'point': (x,y), 'vector': (nx,ny)}, ...]
    """
    if scale is None:
        scale = VECTOR_SCALE

    normals_data = []

    for theta in theta_points:
        x, y = get_cartesian_coordinates(theta)
        nx, ny = compute_normal_vector(theta)

        normals_data.append({
            'point': (x, y),
            'vector': (nx, ny)
        })

        # Рисуем нормаль
        ax.annotate('',
                    xy=(x + nx * scale, y + ny * scale),
                    xytext=(x, y),
                    arrowprops=dict(arrowstyle='->',
                                    color=NORMAL_COLOR,
                                    lw=VECTOR_LINEWIDTH))

    return normals_data


def add_normals_legend(ax):
    """
    Добавляет нормали в легенду.

    Args:
        ax: объект осей matplotlib
    """
    ax.plot([], [], color=NORMAL_COLOR, linewidth=VECTOR_LINEWIDTH,
            label='Нормаль')


if __name__ == '__main__':
    from visualization_base import create_figure, draw_curve, setup_axes
    from visualization_points import add_points_to_plot, add_points_legend
    from point_selector import select_random_points

    fig, ax = create_figure()
    draw_curve(ax)

    theta_points = select_random_points(10)
    add_points_to_plot(ax, theta_points)
    add_normals_to_plot(ax, theta_points)

    add_points_legend(ax)
    add_normals_legend(ax)

    setup_axes(ax, title='Кривая с точками и нормалями')
    ax.legend(fontsize=12, loc='upper right')

    plt.show()