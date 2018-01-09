# 相当于初始化偏置项b
import functools


class ConstNode:
    def __init__(self, layer_index, node_index):
        self.layer_index = layer_index
        self.node_index = node_index
        self.downstream = []
        self.delta = 0
        self.output = 1

    def append_downstream_connection(self, conn):
        self.downstream.append(conn)

    def calc_hidden_layer_delta(self):
        """
        计算隐藏层的delta
        """
        downstream_delta = functools.reduce(lambda ret, conn: ret + conn.downstream_node.delta * conn.weight,
                                            self.downstream, 0.0)
        self.delta = self.output * (1 - self.output) * downstream_delta

    def __str__(self):
        node_str = '%u-%u: output: %1' % (self.layer_index, self.node_index)
        downstream_str = functools.reduce(lambda ret, conn: ret + '\n\t' + str(conn), self.downstream, '')
        return node_str + '\n\tdownstream: ' + downstream_str
