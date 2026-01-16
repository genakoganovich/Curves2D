"""Дополнительная визуализация — соприкасающиеся окружности (кривизна)"""

import numpy as np
import matplotlib.pyplot as plt
from curve_definition import get_cartesian_coordinates
from curve_math import compute_radius_of_curvature, compute_curvature_center
from config import VECTOR_SCALE

# Цвет для окружностей кривизны
CURVATURE_CIRCLE_COLOR = 'purple'
CURVATURE_CIRCLE_ALPHA = 0.3
CURVATURE_CENTER_COLOR = 'purple'


def add_curvature_circles_to_plot(ax, theta_points, max_radius=2.0):
    """
    Добавляет соприкасающиеся окружности на график.

    Args:
        ax: объект осей matplotlib
        theta_points: массив углов θ для точек
        max_radius: максимальный радиус для отрисовки (чтобы не было огромных кругов)

    Returns:
        list: список данных окружностей
    """
    circles_data = []

    for theta in theta_points:
        radius = compute_radius_of_curvature(theta)
        x_center, y_center = compute_curvature_center(theta)

        circles_data.append({
            'theta': theta,
            'center': (x_center, y_center),
            'radius': radius
        })

        # Рисуем только если радиус не слишком большой
        if radius < max_radius and not np.isinf(radius):
            circle = plt.Circle((x_center, y_center), radius,
                                fill=False,
                                color=CURVATURE_CIRCLE_COLOR,
                                linestyle='--',
                                linewidth=1.5,
                                alpha=0.7)
            ax.add_patch(circle)

            # Центр кривизны
            ax.scatter(x_center, y_center, s=30,
                       color=CURVATURE_CENTER_COLOR,
                       marker='x', zorder=4)

    return circles_data


def add_curvature_legend(ax):
    """
    Добавляет окружности кривизны в легенду.
    """
    ax.plot([], [], color=CURVATURE_CIRCLE_COLOR, linestyle='--',
            linewidth=1.5, label='Соприкасающаяся окружность')


def plot_curvature_distribution(save_path=None):
    """
    Строит график распределения кривизны вдоль кривой.

    Args:
        save_path: путь для сохранения
    """
    from curve_math import compute_curvature, compute_radius_of_curvature

    theta = np.linspace(0, 2 * np.pi, 1000)
    curvature = compute_curvature(theta)
    radius = compute_radius_of_curvature(theta)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Кривизна
    axes[0].plot(theta, curvature, 'b-', linewidth=2)
    axes[0].set_xlabel('θ (рад)', fontsize=12)
    axes[0].set_ylabel('Кривизна κ', fontsize=12)
    axes[0].set_title('Кривизна вдоль кривой', fontsize=14)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_xlim(0, 2 * np.pi)

    # Радиус кривизны (ограничиваем для наглядности)
    radius_clipped = np.clip(radius, 0, 5)
    axes[1].plot(theta, radius_clipped, 'r-', linewidth=2)
    axes[1].set_xlabel('θ (рад)', fontsize=12)
    axes[1].set_ylabel('Радиус кривизны R', fontsize=12)
    axes[1].set_title('Радиус кривизны вдоль кривой (ограничен R ≤ 5)', fontsize=14)
    axes[1].grid(True, alpha=0.3)
    axes[1].set_xlim(0, 2 * np.pi)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)

    return fig, axes


if __name__ == '__main__':
    from visualization_base import create_figure, draw_curve, setup_axes
    from visualization_points import add_points_to_plot, add_points_legend
    from point_selector import select_random_points

    # График с окружностями кривизны
    fig, ax = create_figure()
    draw_curve(ax)

    theta_points = select_random_points(10)
    add_points_to_plot(ax, theta_points)
    add_curvature_circles_to_plot(ax, theta_points, max_radius=1.5)

    add_points_legend(ax)
    add_curvature_legend(ax)

    setup_axes(ax, title='Кривая с соприкасающимися окружностями')
    ax.legend(fontsize=10, loc='upper right')

    plt.show()