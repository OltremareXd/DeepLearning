import functools as ft


class Perceptron:
    def __init__(self, input_num, activator):
        self.input_num = input_num
        self.activator = activator
        self.weights = [0.0 for _ in range(input_num)]
        self.bias = 0.0

    def __str__(self):
        return 'weight:%s, bias:%f' % (self.weights, self.bias)

    def predict(self, input_vector):
        return self.activator(ft.reduce(lambda x, y: x + y,
                                        map(lambda x_y: x_y[0] * x_y[1],
                                            zip(input_vector, self.weights)),
                                        0.0) + self.bias)

    def _one_iteration(self, input_vectors, labels, rate):
        samples = zip(input_vectors, labels)
        for (input_vector, label) in samples:
            output = self.predict(input_vector)
            self.update_weight_and_bias(output, input_vector, label, rate)

    def update_weight_and_bias(self, output, input_vector, label, rate):
        delta = label - output
        self.weights = list(map(lambda x_y: x_y[1] + delta * rate * x_y[0],
                                zip(input_vector, self.weights)))
        self.bias += rate * delta

    def train(self, input_vectors, labels, rate, iteration):
        for _ in range(iteration):
            self._one_iteration(input_vectors, labels, rate)


def get_train_data():
    inputs = [[1, 1], [0, 0], [1, 0], [0, 1]]
    labels = [1, 0, 0, 0]
    return inputs, labels


def f(x):
    return 1 if x > 0 else 0


def train_perceptron():
    perceptron = Perceptron(2, f)
    inputs, samples = get_train_data()
    perceptron.train(inputs, samples, 0.1, 10)
    return perceptron


if __name__ == '__main__':
    p = train_perceptron()
    print(p)
    print(p.predict([1, 1]))
