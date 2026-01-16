import matplotlib.pyplot as plt

from point_selector import select_random_points
from curve_math import get_multiple_points_data, verify_orthogonality

from visualization_base import create_figure, draw_curve, setup_axes
from visualization_points import add_points_to_plot, add_points_legend
from visualization_tangents import add_tangents_to_plot, add_tangents_legend
from visualization_normals import add_normals_to_plot, add_normals_legend
from interactive_zoom import InteractiveZoom
from visualization_evolute import (add_evolute_to_plot, add_evolute_legend)
from visualization_curvature import add_curvature_circles_to_plot, add_curvature_legend

def print_points_table(theta_points, points_data):
    """Выводит таблицу с данными точек."""
    print("\n" + "=" * 110)
    print(f"{'Точка':<6} {'θ (рад)':<10} {'x':<10} {'y':<10} "
          f"{'Касат.':<18} {'Норм.':<18} {'κ':<10} {'R':<10}")
    print("=" * 110)

    for i, (theta, data) in enumerate(zip(theta_points, points_data)):
        px, py = data['point']
        tx, ty = data['tangent']
        nx, ny = data['normal']
        k = data['curvature']
        r = data['radius_of_curvature']

        r_str = f"{r:.4f}" if r < 100 else "∞"

        print(f"P{i + 1:<4} {theta:<10.4f} {px:<10.4f} {py:<10.4f} "
              f"({tx:>6.3f},{ty:>6.3f})  ({nx:>6.3f},{ny:>6.3f})  "
              f"{k:<10.4f} {r_str:<10}")

    print("=" * 110)


def verify_all_orthogonality(theta_points):
    """Проверяет ортогональность для всех точек."""
    print("\nПроверка ортогональности (T · N должно быть ≈ 0):")
    for i, theta in enumerate(theta_points):
        dot_product = verify_orthogonality(theta)
        print(f"  P{i + 1}: T · N = {dot_product:.2e}")


def visualize_full_interactive():
    """Создаёт полную интерактивную визуализацию."""

    theta_points = select_random_points()
    points_data = get_multiple_points_data(theta_points)

    fig, ax = create_figure()

    # Рисуем все элементы
    draw_curve(ax)
    add_points_to_plot(ax, theta_points)
    add_tangents_to_plot(ax, theta_points)
    add_normals_to_plot(ax, theta_points)
    add_curvature_circles_to_plot(ax, theta_points)
    add_evolute_to_plot(ax, theta_points)


    # Легенда
    add_points_legend(ax)
    add_tangents_legend(ax)
    add_normals_legend(ax)
    add_curvature_legend(ax)
    add_evolute_legend(ax)


    setup_axes(ax, title='Интерактивный график: кривая с касательными и нормалями')
    ax.legend(fontsize=12, loc='upper right')

    # Включаем интерактивность
    zoom = InteractiveZoom(ax)

    return fig, ax, theta_points, points_data, zoom




def main():
    """Главная функция."""

    print("=" * 50)
    print("  ВИЗУАЛИЗАЦИЯ КРИВОЙ С КАСАТЕЛЬНЫМИ И НОРМАЛЯМИ")
    print("=" * 50)

    fig, ax, theta_points, points_data, zoom = visualize_full_interactive()
    print_points_table(theta_points, points_data)
    verify_all_orthogonality(theta_points)
    plt.show()

if __name__ == '__main__':
    main()