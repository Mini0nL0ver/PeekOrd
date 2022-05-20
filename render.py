import networkx as nx
import matplotlib as plt
from typing import TypeVar

import containers
T = TypeVar("T")


def init_poset(frame: containers.PeekOrdFrame, subset_key="order") -> nx.DiGraph:
    graph = nx.DiGraph()
    lft = {entry.left() for entry in frame.timeline._entries}
    rgh = {entry.right() for entry in frame.timeline._entries}
    proxies = [proxy for proxy in lft.union(rgh)]
    proxies.sort(key=lambda p: p.val)
    for i in range(len(proxies)):
        graph.add_node(proxies[i], **{subset_key: i})
    for entry in frame.timeline.past(frame):
        graph.add_edge(entry.left(), entry.right())
    nx.transitive_reduction(graph)
    return graph


def partialorder_layout(graph: nx.DiGraph, subset_key=None, iterations=50):
    x_pos = nx.multipartite_layout(graph, subset_key=subset_key, align="vertical")

    def fix_x(new_pos):
        return {node: (x_pos[node][0], new_pos[node][1]) for node in graph.nodes()}
    pos = fix_x(nx.random_layout(graph))
    for _ in range(iterations):
        pos = fix_x(nx.spring_layout(graph, pos=pos, iterations=1))
    return pos


def update_layout(graph: nx.DiGraph, pos, iterations=5):
    x_pos = pos

    def fix_x(new_pos):
        return {node: (x_pos[node][0], new_pos[node][1]) for node in graph.nodes()}
    for _ in range(iterations):
        pos = fix_x(nx.spring_layout(graph, pos=pos, iterations=1))
    return pos
