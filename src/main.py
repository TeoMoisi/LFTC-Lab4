from src.parser.lr0_algorithm import LR0Algorithm


class Main:
    @staticmethod
    def step1():
        # print("state: " + str(state))
        # print("analysis_element: " + str(analysis_element))
        # print("next state: " + str(next_state))
        # print('\n')
        alg = LR0Algorithm("input/grammar.txt")
        alg.canonical_collection()
        used_productions = alg.check_input(["a", "b", "b", "c"])
        alg.print_derivations(used_productions)


    @staticmethod
    def step2():
        pass


if __name__ == '__main__':
    Main.step1()
    Main.step2()

