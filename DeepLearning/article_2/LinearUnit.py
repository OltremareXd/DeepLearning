from DeepLearning.article_1.perceptron import Perceptron


def f(x):
    return x


class LinearUnit(Perceptron):
    def __init__(self, input_num):
        Perceptron.__init__(self, input_num, f)


def get_train_data_set():
    input_vectors = [[5], [3], [8], [1.4], [10.1]]
    standards = [5500, 2300, 7600, 1800, 11400]
    return input_vectors, standards


def train_linear_unit():
    linear_unit = LinearUnit(1)
    input_vectors, standards = get_train_data_set()
    linear_unit.train(input_vectors, standards, 0.01, 10)
    return linear_unit


if __name__ == '__main__':
    unit = train_linear_unit()
    print(unit)
    print('工作{0}年的人，工资约为{1}.' .format(3.4, unit.predict([3.4])))
