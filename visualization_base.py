"""Основная визуализация — только кривая"""

import matplotlib.pyplot as plt
from curve_definition import get_curve_points
from config import (FIGURE_SIZE, CURVE_COLOR, CURVE_LINEWIDTH,
                    CURVE_FILL_ALPHA)


def create_figure():
    """
    Создаёт фигуру и оси для визуализации.

    Returns:
        tuple: (fig, ax)
    """
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    return fig, ax


def setup_axes(ax, title='Кривая'):
    """
    Настраивает оси графика.

    Args:
        ax: объект осей matplotlib
        title: заголовок графика
    """
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')


def draw_curve(ax, show_fill=True):
    """
    Рисует кривую на осях.

    Args:
        ax: объект осей matplotlib
        show_fill: заливать ли область внутри кривой

    Returns:
        tuple: (theta, x, y) данные кривой
    """
    theta, x, y = get_curve_points()

    ax.plot(x, y, color=CURVE_COLOR, linewidth=CURVE_LINEWIDTH,
            label='Кривая', zorder=1)

    if show_fill:
        ax.fill(x, y, alpha=CURVE_FILL_ALPHA, color=CURVE_COLOR)

    return theta, x, y


def visualize_curve_only(save_path=None):
    """
    Создаёт визуализацию только кривой.

    Args:
        save_path: путь для сохранения (опционально)

    Returns:
        tuple: (fig, ax)
    """
    fig, ax = create_figure()
    draw_curve(ax)
    setup_axes(ax, title='Сложная замкнутая кривая (клякса)')
    ax.legend(fontsize=12, loc='upper right')

    return fig, ax


if __name__ == '__main__':
    visualize_curve_only()
    plt.show()