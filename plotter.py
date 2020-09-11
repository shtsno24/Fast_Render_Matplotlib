import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time


class Scatter:

    def __init__(self, fig, ax, plot_area=(1000, 1000), len_points=100, show_icon=False, icon_radius=100):
        self.fig = fig
        self.plot_area = plot_area
        self.icon_radius = icon_radius if show_icon is True else None

        # axis setup
        self.pos_ax = ax
        self.pos_ax.set_xlim(-plot_area[0], plot_area[0])
        self.pos_ax.set_ylim(-plot_area[1], plot_area[1])
        self.pos_points = self.pos_ax.scatter([], [])
        self.xy = [[0.0, 0.0] for x in range(len_points)]
        if show_icon is True:
            self.agent_icon = mpatches.RegularPolygon(xy=(0, 0), numVertices=4, radius=self.icon_radius, orientation=0.0, ec="r", fill=False)
            self.pos_ax.add_patch(self.agent_icon)

        # show figure
        self.fig.canvas.draw()
        self.fig.show()

    def update_data(self, points, orientation=0.0):
        # draw background with white
        self.pos_ax.draw_artist(self.pos_ax.patch)

        # plot points
        self.xy.append(points)
        self.xy.pop(0)
        self.pos_points.set_offsets(self.xy)
        self.pos_ax.draw_artist(self.pos_points)

        # plot the icon
        if self.icon_radius is not None:
            self.agent_icon.xy = points
            self.agent_icon.orientation = orientation
            self.pos_ax.draw_artist(self.agent_icon)

        # update this graph
        self.fig.canvas.blit(self.pos_ax.bbox)

    def plot(self, points, orientation=0.0):
        self.update_data(points, orientation)
        self.fig.canvas.flush_events()


class Line:

    def __init__(self, fig, ax, plot_area=(1000, 1000), len_points=100):
        self.fig = fig
        self.plot_area = plot_area

        # axis setup
        self.line_ax = ax
        self.line_ax.set_xlim(0, plot_area[0])
        self.line_ax.set_ylim(-plot_area[1], plot_area[1])
        self.ydata = [0.0 for x in range(len_points)]
        self.line, = self.line_ax.plot(self.ydata)
        # show figure
        self.fig.canvas.draw()
        self.fig.show()

    def update_data(self, points):
        # draw background with white
        self.line_ax.draw_artist(self.line_ax.patch)

        # plot points
        self.ydata.append(points)
        self.ydata.pop(0)
        self.line.set_ydata(self.ydata)
        self.line_ax.draw_artist(self.line)

        # update this graph
        self.fig.canvas.blit(self.line_ax.bbox)

    def plot(self, ydata):
        self.update_data(ydata)
        self.fig.canvas.flush_events()


if __name__ == "__main__":
    loop_times = 5000
    fig = plt.figure()
    pos_ax = fig.add_subplot(2, 1, 1)
    line_ax = fig.add_subplot(2, 1, 2)
    scatter_view = Scatter(fig, pos_ax, len_points=1250, show_icon=True)
    line_view = Line(fig, line_ax, plot_area=(1250, 1000), len_points=1250)

    input(">>")
    sum_time = 0.0
    for i in range(loop_times):
        rand_array = np.random.randint(-1000, 1000, 2)
        start = time.perf_counter_ns()
        scatter_view.plot(rand_array)
        line_view.plot(rand_array[1])
        while True:
            end = time.perf_counter_ns()
            if ((end - start) * 1.0e-9) > 0.001:
                break
        sum_time += end - start
    input("Done : " + str(loop_times / sum_time / 1.0e-9) + " [fps]")
