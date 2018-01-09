import DeepLearning.article_3.Node as Node
import DeepLearning.article_3.ConstNode as ConstNode


class Layer:
    def __init__(self, layer_index, node_count):
        """
        初始化单层信息
        layer_index: 层号
        node_count: 该层节点数
        """
        self.layer_index = layer_index
        self.node_count = node_count
        self.nodes = []
        for i in range(node_count):
            self.nodes.append(Node.Node(layer_index, i))
        self.nodes.append(ConstNode.ConstNode(layer_index, node_count))

    def sef_output(self, data):
        """
        当该层为输出层时，调用此函数
        """
        for i in range(len(data)):
            self.nodes[i].set_output(data[i])

    def calc_output(self):
        """
        用于计算该层输出值
        """
        for node in self.nodes[:-1]:
            node.calc_output()

    def dump(self):
        """
        打印层的信息
        """
        for node in self.nodes:
            print(node)
