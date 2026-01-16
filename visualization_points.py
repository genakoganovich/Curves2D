"""Дополнительная визуализация — добавление точек"""

import matplotlib.pyplot as plt
from curve_definition import get_cartesian_coordinates
from config import (POINT_SIZE, POINT_COLOR, POINT_EDGE_COLOR,
                    POINT_EDGE_WIDTH)


def add_points_to_plot(ax, theta_points, show_labels=True):
    """
    Добавляет точки на график.

    Args:
        ax: объект осей matplotlib
        theta_points: массив углов θ для точек
        show_labels: показывать ли подписи точек

    Returns:
        list: список координат точек [(x, y), ...]
    """
    points_coords = []

    for i, theta in enumerate(theta_points):
        x, y = get_cartesian_coordinates(theta)
        points_coords.append((x, y))

        # Рисуем точку
        ax.scatter(x, y, s=POINT_SIZE, c=POINT_COLOR,
                   zorder=5, edgecolors=POINT_EDGE_COLOR,
                   linewidths=POINT_EDGE_WIDTH)

        # Подпись
        if show_labels:
            ax.annotate(f'P{i + 1}', (x, y),
                        textcoords="offset points",
                        xytext=(10, 10),
                        fontsize=10,
                        fontweight='bold')

    return points_coords


def add_points_legend(ax):
    """
    Добавляет точки в легенду.

    Args:
        ax: объект осей matplotlib
    """
    ax.scatter([], [], s=POINT_SIZE, c=POINT_COLOR, label='Точки')


if __name__ == '__main__':
    from visualization_base import create_figure, draw_curve, setup_axes
    from point_selector import select_random_points

    fig, ax = create_figure()
    draw_curve(ax)

    theta_points = select_random_points(10)
    add_points_to_plot(ax, theta_points)
    add_points_legend(ax)

    setup_axes(ax, title='Кривая с точками')
    ax.legend(fontsize=12, loc='upper right')

    plt.show()