# 用于记录连接权重以及该连接中的上下游结点
import random


class Connection:
    def __init__(self, upstream_node, downstream_node):
        self.upstream_node = upstream_node
        self.downstream_node = downstream_node
        self.weight = random.uniform(-0.1, 0.1)
        self.gradient = 0.0

    def calc_gradient(self):
        """
        计算梯度
        在此处delta即是通过反向传播算法求得的导数值
        """
        self.gradient = self.downstream_node.delta * self.upstream_node.output

    def get_gradient(self):
        return self.gradient

    def update_weight(self, rate):
        self.calc_gradient()
        self.weight += rate * self.gradient

    def __str__(self):
        return '(%u - %u) : (%u - %u) = %f' % (
            self.upstream_node.layer_index,
            self.upstream_node.node_index,
            self.downstream_node.layer_index,
            self.downstream_node.node_index,
            self.weight
        )

    