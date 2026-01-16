from point_selector import select_random_points
from visualization_3d import (
    create_figure_3d, setup_axes_3d, draw_curve_3d,
    add_points_3d, add_tangents_3d, add_normals_3d,
    add_evolute_3d, add_curvature_circles_3d ,add_legend_3d
)
import matplotlib.pyplot as plt

# Выбираем точки
theta_points = select_random_points(10)

# Создаём 3D график
fig, ax = create_figure_3d()

# Добавляем элементы
draw_curve_3d(ax)
add_points_3d(ax, theta_points)
add_tangents_3d(ax, theta_points)
add_normals_3d(ax, theta_points)
add_curvature_circles_3d(ax, theta_points)
add_evolute_3d(ax, theta_points)

# Легенда и настройка
add_legend_3d(ax, show_tangents=True, show_normals=True, show_evolute=True, show_curvature_circles=True)
plt.show()
setup_axes_3d(ax, title='Моя 3D кривая', elevation=45, azimuth=-45)

plt.show()