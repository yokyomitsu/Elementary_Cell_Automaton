import os
from random import randint
import matplotlib.pyplot as plt

class Rule:
    def __init__(self, rule_no):
        self.rule_no = rule_no
        self.rule = self._init_rule(rule_no)

    def _init_rule(self, rule_no):
        R = 8
        rule = [0 for _ in range(R)]
        for i in range(R):
            rule[i] = rule_no % 2
            rule_no //= 2
        return rule

    def apply(self, left, center, right):
        return self.rule[right * 4 + center * 2 + left]


class CellularAutomaton:
    def __init__(self, size=50, is_rand=False):
        self.size = size
        self.is_rand = is_rand
        self.ca, self.current_state = self._init_eca(size, is_rand)

    def _init_eca(self, size, is_rand):
        ca = [randint(0, 1) for _ in range(size)] if is_rand else [0] * size
        if not is_rand:
            ca[size // 2] = 1
        current_state = [[0] * size for _ in range(size)]
        current_state[0] = ca[::-1]
        return ca, current_state

    def update(self, rule):
        size = len(self.ca)
        next_ca = [0] * size
        for i in range(size):
            left = self.ca[i - 1]
            center = self.ca[i]
            right = self.ca[(i + 1) % size]
            next_ca[i] = rule.apply(left, center, right)
        self.ca = next_ca

    def run(self, rule, max_t):
        for t in range(1, max_t):
            self.update(rule)
            self.current_state[t] = self.ca[::-1]

    def get_current_state(self):
        return self.current_state


class ECAPlotter:
    @staticmethod
    def plot_and_save(current_state, rule_no, save_path):
        os.makedirs(save_path, exist_ok=True)
        fig, ax = plt.subplots()
        ax.imshow(current_state, cmap='binary')
        ax.set_title(f"Rule: {rule_no}")
        plt.savefig(os.path.join(save_path, f'Rule{rule_no}.png'))
        plt.close()


def main():
    is_rand = True
    max_t = 50  # 最大ステップ数
    rule_no = 30

    rule = Rule(rule_no)
    automaton = CellularAutomaton(size=50, is_rand=is_rand)
    automaton.run(rule, max_t)
    current_state = automaton.get_current_state()
    ECAPlotter.plot_and_save(current_state, rule_no, 'eca_results')

if __name__ == "__main__":
    main()
