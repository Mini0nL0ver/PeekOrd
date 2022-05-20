import matplotlib.pyplot as plt
from matplotlib import widgets

from containers import *
from render import *
from algorithms import *


def main():

    col_xs = PeekOrdCol(9, 2, 6, 3, 7, 4, 1, 5)
    xs = sorted(col_xs.as_list(), key=lambda proxy: proxy.val)
    xys = merge_sort(xs)

    comparisons_xx = col_xs.get_or_make_log(col_xs)
    timeline = PeekOrdTimeline(comparisons_xx)

    fig, ax = plt.subplots()

    graph = init_poset(timeline[0], subset_key="order")
    pos = [partialorder_layout(graph, subset_key="order")]

    nx.draw(graph, pos=pos[0], with_labels=True, ax=ax)

    def update(snapshot):
        ax.clear()
        frame = timeline[snapshot]
        new_graph = init_poset(frame, subset_key="order")
        pos[0] = update_layout(new_graph, pos=pos[0])
        nx.draw(new_graph, pos=pos[0], with_labels=True, ax=ax)

    time_slider = widgets.Slider(plt.axes([0.25, 0.1, 0.65, 0.03]), "Time", 0, len(timeline) - 1, valinit=0, valstep=1)
    time_slider.on_changed(update)

    plt.show()


if __name__ == '__main__':
    main()
