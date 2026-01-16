import matplotlib.pyplot as plt

from point_selector import select_random_points
from curve_math import get_multiple_points_data, verify_orthogonality

from visualization_base import (create_figure, draw_curve, setup_axes)
from visualization_points import (add_points_to_plot, add_points_legend)
from visualization_tangents import (add_tangents_to_plot, add_tangents_legend)
from visualization_normals import (add_normals_to_plot, add_normals_legend)


def print_points_table(theta_points, points_data):
    """Выводит таблицу с данными точек."""
    print("\n" + "=" * 90)
    print(f"{'Точка':<8} {'θ (рад)':<12} {'x':<12} {'y':<12} "
          f"{'Касат. (tx,ty)':<22} {'Норм. (nx,ny)':<22}")
    print("=" * 90)

    for i, (theta, data) in enumerate(zip(theta_points, points_data)):
        px, py = data['point']
        tx, ty = data['tangent']
        nx, ny = data['normal']
        print(f"P{i + 1:<6} {theta:<12.4f} {px:<12.4f} {py:<12.4f} "
              f"({tx:>7.4f}, {ty:>7.4f})    ({nx:>7.4f}, {ny:>7.4f})")

    print("=" * 90)


def verify_all_orthogonality(theta_points):
    """Проверяет ортогональность для всех точек."""
    print("\nПроверка ортогональности (T · N должно быть ≈ 0):")
    for i, theta in enumerate(theta_points):
        dot_product = verify_orthogonality(theta)
        print(f"  P{i + 1}: T · N = {dot_product:.2e}")


def visualize_full():
    """Создаёт полную визуализацию."""

    theta_points = select_random_points()
    points_data = get_multiple_points_data(theta_points)

    fig, ax = create_figure()

    draw_curve(ax)
    add_points_to_plot(ax, theta_points)
    add_tangents_to_plot(ax, theta_points)
    add_normals_to_plot(ax, theta_points)

    add_points_legend(ax)
    add_tangents_legend(ax)
    add_normals_legend(ax)

    setup_axes(ax, title='Кривая с касательными и нормалями в 10 точках')
    ax.legend(fontsize=12, loc='upper right')

    return fig, ax, theta_points, points_data


def main():
    """Главная функция."""

    print("=" * 50)
    print("  ВИЗУАЛИЗАЦИЯ КРИВОЙ С КАСАТЕЛЬНЫМИ И НОРМАЛЯМИ")
    print("=" * 50)

    # Полная визуализация
    fig, ax, theta_points, points_data = visualize_full()

    # Таблица данных
    print_points_table(theta_points, points_data)

    # Проверка ортогональности
    verify_all_orthogonality(theta_points)

    plt.show()


if __name__ == '__main__':
    main()