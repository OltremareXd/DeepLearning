import functools

import DeepLearning.article_3.Connection as Connection
import DeepLearning.article_3.Connections as Connections
import DeepLearning.article_3.Layer as Layer


class Network:
    def __init__(self, layers):
        """
        初始化全连接神经网络
        layers: 二维数组，描述神经网络每层的结点数
        """
        self.connections = Connections.Connections()
        self.layers = []
        layer_cont = len(layers)
        node_count = 0
        for i in range(layer_cont):
            self.layers.append(Layer.Layer(i, layers[i]))
        for layer in range(layer_cont - 1):
            connections = [Connection.Connection(upstream_node, downstream_node)
                           for upstream_node in self.layers[layer].nodes
                           for downstream_node in self.layers[layers + 1].nodes[:-1]]
            for conn in connections:
                self.connections.add_connection(conn)
                conn.downstream_node.append_upstream_connection(conn)
                conn.upstream_node.append_downstream_connection(conn)

    def train(self, labels, data_set, rate, iteration):
        """
        训练神经网络
        labels: 数组， 每个元素是一个标签
        data_set: 二维数组，每个元素是一个样本值的特征
        rate: 学习率
        iteration: 迭代次数
        """
        for i in range(iteration):
            for d in range(len(data_set)):
                self.train_one_sample(labels[d], data_set[d], rate)

    def train_one_sample(self, label, sample, rate):
        """
        用一个样本训练
        """
        self.predict(sample)
        self.calc_delta(label)
        self.update_weight(rate)

    def calc_delta(self, label):
        output_node = self.layers[-1].nodes
        for i in range(len(label)):
            output_node[i].calc_output_layer_delta(label[i])
        for layer in self.layers[-2::-1]:
            for node in layer.nodes:
                node.calc_hidden_layer_delta()

    def update_weight(self, rate):
        """
        用于更新每个结点的权重
        """
        for layer in self.layers[-1]:
            for node in layer.nodes:
                for conn in node.downstream:
                    conn.update_weight(rate)

    def calc_gradient(self):
        """
        用于计算梯度
        """
        for layer in self.layers[:-1]:
            for node in layer.nodes:
                for conn in node.downstream:
                    conn.calc_gradient()

    def get_gradient(self, label, sample):
        """
        获得网络在同一个样本下，每个连接的梯度
        主要用于梯度检查
        label:样本标签
        sample:样本输入
        """
        self.predict(sample)
        self.calc_delta(label)
        self.calc_gradient()

    def predict(self, sample):
        """
        根据输入的样本值预测输出值
        sample: 二维数组，样本特征
        :return 预测的结果
        """
        self.layers[0].set_output(sample)
        for i in range(1, len(self.layers)):
            self.layers[i].calc_output()
        return list(map(lambda node: node.output, self.layers[-1].nodes[:-1]))

    def dum(self):
        """
        打印网络信息
        """
        for layer in self.layers:
            print(layer)


def gradient_check(network, sample_feature, sample_label):
    """
    执行梯度检查
    network:生成的网络对象
    sample_feature:输入的样本数据
    sample_label:输入的标准标签
    """

    # 获取在本次样例中的各层梯度
    network.get_gradient(sample_label, sample_feature)

    # 对每个权重做梯度检查
    for conn in network.connections.connections:
        # 获取当前连接的梯度
        actual_gradient = conn.get_gradient

        # 将网络误差加一个很小的值
        epsilon = 0.0001
        conn.weight += epsilon
        error1 = network_error(network.predict(sample_feature), sample_label)

        # 将网络误差减一个很小的值
        # 因为刚刚已经加过一次，所以这次要减2倍
        conn.weight -= 2 * epsilon
        error2 = network_error(network.predict(sample_feature), sample_label)

        # 根据极限的定义公式计算期望的梯度值
        expected_gradient = (error2 - error1) / (2 * epsilon)

        # 比较
        print('expected gradient: %f \n actual gradient: %f' % (expected_gradient, actual_gradient))


# 计算结果值与标准值的误差，即使用梯度下降的误差的平方计算
def network_error():
    return lambda v1, v2: \
        0.5 * functools.reduce(lambda a, b: a + b,
                               map(lambda v: (v[0] - v[1]) * (v[0] - v[1]),
                                   zip(v1, v2)))