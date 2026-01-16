"""Интерактивное управление графиком: zoom, pan, сброс."""

import matplotlib.pyplot as plt


class InteractiveZoom:
    """
    Класс для интерактивного управления matplotlib графиком.

    Возможности:
        - Zoom колёсиком мыши (относительно позиции курсора)
        - Pan средней кнопкой мыши (перетаскивание)
        - Сброс вида клавишей 'r'
        - Закрытие окна клавишей 'q'

    Использование:
        fig, ax = plt.subplots()
        ax.plot(x, y)
        zoom = InteractiveZoom(ax)
        plt.show()
    """

    def __init__(self, ax, scale_factor=1.2, print_help=True):
        """
        Инициализация интерактивного управления.

        Args:
            ax: объект осей matplotlib
            scale_factor: коэффициент масштабирования (по умолчанию 1.2)
            print_help: выводить ли справку в консоль
        """
        self.ax = ax
        self.fig = ax.figure
        self.scale_factor = scale_factor
        self.press = None

        # Сохраняем начальные границы для сброса
        self.original_xlim = ax.get_xlim()
        self.original_ylim = ax.get_ylim()

        # Подключаем обработчики событий
        self._connect_events()

        if print_help:
            self._print_help()

    def _connect_events(self):
        """Подключает обработчики событий мыши и клавиатуры."""
        canvas = self.fig.canvas

        self._cid_scroll = canvas.mpl_connect('scroll_event', self._on_scroll)
        self._cid_press = canvas.mpl_connect('button_press_event', self._on_press)
        self._cid_release = canvas.mpl_connect('button_release_event', self._on_release)
        self._cid_motion = canvas.mpl_connect('motion_notify_event', self._on_motion)
        self._cid_key = canvas.mpl_connect('key_press_event', self._on_key)

    def disconnect(self):
        """Отключает все обработчики событий."""
        canvas = self.fig.canvas

        canvas.mpl_disconnect(self._cid_scroll)
        canvas.mpl_disconnect(self._cid_press)
        canvas.mpl_disconnect(self._cid_release)
        canvas.mpl_disconnect(self._cid_motion)
        canvas.mpl_disconnect(self._cid_key)

    def _print_help(self):
        """Выводит справку по управлению."""
        help_text = """
╔══════════════════════════════════════════════════╗
║           УПРАВЛЕНИЕ ГРАФИКОМ                    ║
╠══════════════════════════════════════════════════╣
║  Колёсико мыши      : Zoom in / out              ║
║  Средняя кнопка     : Pan (перетаскивание)       ║
║  Клавиша 'r'        : Сброс к исходному виду     ║
║  Клавиша 'g'        : Вкл/выкл сетку             ║
║  Клавиша 'q'        : Закрыть окно               ║
╚══════════════════════════════════════════════════╝
        """
        print(help_text)

    def _on_scroll(self, event):
        """Обработчик прокрутки колёсика — zoom."""
        if event.inaxes != self.ax:
            return

        # Определяем направление zoom
        if event.button == 'up':
            scale = 1 / self.scale_factor  # zoom in
        elif event.button == 'down':
            scale = self.scale_factor  # zoom out
        else:
            return

        # Текущие границы
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        # Позиция курсора — центр масштабирования
        xdata = event.xdata
        ydata = event.ydata

        # Вычисляем новые границы относительно курсора
        new_xlim = [
            xdata - (xdata - xlim[0]) * scale,
            xdata + (xlim[1] - xdata) * scale
        ]
        new_ylim = [
            ydata - (ydata - ylim[0]) * scale,
            ydata + (ylim[1] - ydata) * scale
        ]

        # Применяем новые границы
        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        self.fig.canvas.draw_idle()

    def _on_press(self, event):
        """Обработчик нажатия кнопки мыши — начало pan."""
        if event.inaxes != self.ax:
            return

        # Средняя кнопка мыши для pan
        if event.button == 2:
            self.press = {
                'x': event.xdata,
                'y': event.ydata,
                'xlim': self.ax.get_xlim(),
                'ylim': self.ax.get_ylim()
            }

    def _on_release(self, event):
        """Обработчик отпускания кнопки мыши — конец pan."""
        self.press = None

    def _on_motion(self, event):
        """Обработчик движения мыши — pan."""
        if self.press is None:
            return
        if event.inaxes != self.ax:
            return

        # Вычисляем смещение
        dx = event.xdata - self.press['x']
        dy = event.ydata - self.press['y']

        # Применяем смещение
        xlim = self.press['xlim']
        ylim = self.press['ylim']

        self.ax.set_xlim(xlim[0] - dx, xlim[1] - dx)
        self.ax.set_ylim(ylim[0] - dy, ylim[1] - dy)
        self.fig.canvas.draw_idle()

    def _on_key(self, event):
        """Обработчик нажатия клавиш."""
        if event.key == 'r':
            self.reset_view()
        elif event.key == 'g':
            self.toggle_grid()
        elif event.key == 'q':
            plt.close(self.fig)

    def reset_view(self):
        """Сбрасывает вид к исходным границам."""
        self.ax.set_xlim(self.original_xlim)
        self.ax.set_ylim(self.original_ylim)
        self.fig.canvas.draw_idle()

    def toggle_grid(self):
        """Переключает отображение сетки."""
        self.ax.grid(not self.ax.xaxis.get_gridlines()[0].get_visible())
        self.fig.canvas.draw_idle()

    def set_scale_factor(self, factor):
        """
        Устанавливает коэффициент масштабирования.

        Args:
            factor: новый коэффициент (> 1.0)
        """
        if factor > 1.0:
            self.scale_factor = factor

    def update_original_limits(self):
        """Обновляет 'исходные' границы на текущие."""
        self.original_xlim = self.ax.get_xlim()
        self.original_ylim = self.ax.get_ylim()


def enable_interactive_zoom(ax, **kwargs):
    """
    Функция-обёртка для быстрого включения интерактивности.

    Args:
        ax: объект осей matplotlib
        **kwargs: аргументы для InteractiveZoom

    Returns:
        InteractiveZoom: экземпляр класса

    Пример:
        fig, ax = plt.subplots()
        ax.plot(x, y)
        enable_interactive_zoom(ax)
        plt.show()
    """
    return InteractiveZoom(ax, **kwargs)