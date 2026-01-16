from config import (
    EVOLUTE_POINT_COLOR,
    EVOLUTE_POINT_SIZE,
    EVOLUTE_CONNECTION_COLOR,
    EVOLUTE_CONNECTION_STYLE,
    EVOLUTE_CONNECTION_WIDTH,
    EVOLUTE_CONNECTION_ALPHA
)


def add_evolute_to_plot(ax, theta_points, show_connections=True, show_labels=True):
    """
    Добавляет точки эволюты на график.

    Args:
        ax: объект осей matplotlib
        theta_points: массив углов θ выбранных точек кривой
        show_connections: показывать линии от точек кривой к точкам эволюты
        show_labels: показывать подписи точек

    Returns:
        list: данные точек эволюты
    """
    from curve_math import get_evolute_points
    from curve_definition import get_cartesian_coordinates

    evolute_data = get_evolute_points(theta_points)

    for i, data in enumerate(evolute_data):
        x_e, y_e = data['evolute_point']

        # Точка эволюты
        ax.scatter(x_e, y_e, s=EVOLUTE_POINT_SIZE, c=EVOLUTE_POINT_COLOR,
                   zorder=5, edgecolors='white', linewidths=1.5)

        # Соединительная линия
        if show_connections:
            x, y = data['curve_point']
            ax.plot([x, x_e], [y, y_e],
                    color=EVOLUTE_CONNECTION_COLOR,
                    linestyle=EVOLUTE_CONNECTION_STYLE,
                    linewidth=EVOLUTE_CONNECTION_WIDTH,
                    alpha=EVOLUTE_CONNECTION_ALPHA)

        # Подпись
        if show_labels:
            ax.annotate(f'E{i + 1}', (x_e, y_e),
                        textcoords="offset points",
                        xytext=(8, 8),
                        fontsize=9,
                        color=EVOLUTE_POINT_COLOR,
                        fontweight='bold')

    return evolute_data


def add_evolute_legend(ax):
    """
    Добавляет точки эволюты в легенду.

    Args:
        ax: объект осей matplotlib
    """
    ax.scatter([], [], s=EVOLUTE_POINT_SIZE, c=EVOLUTE_POINT_COLOR,
               label='Точки эволюты')