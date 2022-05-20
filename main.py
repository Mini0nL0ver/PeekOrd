import matplotlib.pyplot as plt
from matplotlib import widgets

from containers import *
from render import *


def main():
    col: PeekOrdCol[int] = PeekOrdCol(1, 2, 3)
    lst: List[PeekOrdProxy[int]] = sorted(col.as_list(), key=lambda proxy: proxy.val)  # sort without messing with order
    print(lst)
    _ = lst[0] < lst[1]
    _ = lst[1] < lst[2]
    print(col.get_or_make_log(col))
    tl: PeekOrdTimeline[int] = PeekOrdTimeline(col.get_or_make_log(col))
    fr: PeekOrdFrame[int] = tl[-1]
    print(str(lst[0]) + " < " + str(lst[2]) + " = " + str(fr.lt(lst[0], lst[2])))

    fig, ax = plt.pyplot.subplots()

    graph = init_poset(tl[0], subset_key="order")
    pos = [partialorder_layout(graph, subset_key="order")]

    nx.draw(graph, pos=pos[0], with_labels=True, ax=ax)

    def update(snapshot):
        ax.clear()
        frame = tl[snapshot]
        new_graph = init_poset(frame, subset_key="order")
        pos[0] = update_layout(new_graph, pos=pos[0])
        nx.draw(new_graph, pos=pos[0], with_labels=True, ax=ax)

    time_slider = widgets.Slider(plt.pyplot.axes([0.25, 0.1, 0.65, 0.03]), "Time", 0, len(tl) - 1, valinit=0, valstep=1)
    time_slider.on_changed(update)

    plt.pyplot.show()


if __name__ == '__main__':
    main()
