import time

import numpy as np
import pandas as pd
import networkx as nx
import json


# from networkx.algorithms import bipartite
# import scipy.stats


def read_data(file_name):
    return pd.ExcelFile(file_name)


def show(input_book):
    input_sheet_name = input_book.sheet_names
    # lenでシートの総数を確認
    num_sheet = len(input_sheet_name)
    # シートの数とシートの名前のリストの表示
    print("Sheet の数:", num_sheet)
    print(input_sheet_name)


def add_node(col, G):
    G.add_nodes_from(col.values.tolist(), fontname='MS Gothic')


def add_edge(df, G):
    edges = df.values.tolist()
    G.add_edges_from(edges)


def make_network(df, G):
    for col in df:
        add_node(df[col], G)
    add_edge(df, G)


def set_nodes_color(A, nodes, color="red"):
    for node in nodes:
        A.get_node(node).attr['fillcolor'] = color


def average_degree(G):
    degree = list(dict(nx.degree(G)).values())
    return np.mean(degree)


def is_in_df(df, element):
    return element in df.values


def conv_RGB_to_colorcode(rgb):
    R = int((rgb[0]) * 255)
    G = int(rgb[1] * 255)
    B = int(rgb[2] * 255)
    color_code = '#{:02x}{:02x}{:02x}'.format(R, G, B)
    color_code = color_code.replace('0x', '')
    return color_code


def get_network_d3(input_book, sheet):
    group1, group2 = "會社名", "役員名"
    df = input_book.parse(sheet, usecols=["會社名", "役員名"])

    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.applymap(lambda x: x.replace('　', '') if isinstance(x, str) else x)
    df = df.replace("", pd.NA).dropna(how='any')
    # df = df.dropna(how='any')

    # df[group1] = df[group1].apply(lambda x: x.strip())
    # df[group2] = df[group2].apply(lambda x: x.strip())

    # 支店などを消す
    df = df[~df['會社名'].str.contains('支店')]
    df = df[~df['會社名'].str.contains('出張')]
    # # 株式会社でないものを消す
    # df = df[df['會社名'].str.contains('株式')]
    # 米穀取引所を消す
    df = df[~df['會社名'].str.contains('米穀')]

    G = nx.Graph()
    make_network(df[["會社名", "役員名"]], G)

    d = nx.json_graph.node_link_data(G)

    largest = max(nx.connected_components(G), key=len)
    d["saidai"] = list(largest)

    return d


def get_saidai_renketsu(data):
    G = nx.node_link_graph(json.loads(data))
    largest = max(nx.connected_components(G), key=len)
    saidai_G = G.subgraph(largest)

    return nx.json_graph.node_link_data(saidai_G)
