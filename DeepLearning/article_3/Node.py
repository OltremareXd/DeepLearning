import functools

import math


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


class Node:
    """
    此类用于构造结点对象，保存自身的信息
    layer_index:表示结点所属层的编号
    node_index:表示结点编号
    """
    def __init__(self, layer_index, node_index):
        self.layer_index = layer_index
        self.node_index = node_index
        self.upstream = []
        self.downstream = []
        self.delta = 0
        self.output = 0

    def set_output(self, output):
        """
        设置输出值。当结点是输入层时使用
        """
        self.output = output

    def append_downstream_connection(self, conn):
        """
        添加当前结点与下游节点的连接
        """
        self.downstream.append(conn)

    def append_upstream_connection(self, conn):
        """
        添加当前结点与上游节点的连接
        """
        self.upstream.append(conn)

    def calc_output(self):
        """
        通过w*x+b后，使用sigmoid函数计算输出值
        """
        output = functools.reduce(lambda ret, conn: ret + conn.upstream_node.output * conn.weight, self.upstream, 0)
        self.output = sigmoid(output)

    def calc_hidden_layer_delta(self):
        """
        根据隐藏层求delta的方法获得当前输出结点的delta值
        :return:
        """
        downstream_delta = functools.reduce(lambda ret, conn: ret + conn.downstream_node.delta * conn.weight,
                                            self.downstream, 0.0)
        self.delta = self.output * (1 - self.output) * downstream_delta

    def calc_output_layer_delta(self, label):
        """
        根据output*(1-output)(label-output)计算输出层的delta
        """
        self.delta = self.output * (1 - self.output) * (label - self.output)

    def __str__(self):
        node_str = '%u-%u: output: %f delta: %f' % (self.layer_index, self.node_index, self.output, self.delta)
        downstream_str = functools.reduce(lambda ret, conn: ret + '\n\t' + str(conn), self.downstream, '')
        upstream_str = functools.reduce(lambda ret, conn: ret + '\n\t' + str(conn), self.upstream, '')
        return node_str + '\n\tdownstream:' + downstream_str + '\n\tupstream:' + upstream_str
