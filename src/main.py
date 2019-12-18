from src.parser.lr0_algorithm import LR0Algorithm
from src.scanner.LexicalAnalysis import LexicalAnalysis


class Main:
    @staticmethod
    def step1():
        # print("state: " + str(state))
        # print("analysis_element: " + str(analysis_element))
        # print("next state: " + str(next_state))
        # print('\n')
        alg = LR0Algorithm("input/simple_grammar.txt")
        alg.canonical_collection()
        used_productions = alg.check_input(["a", "b", "b", "c"])
        alg.print_derivations(used_productions)

    @staticmethod
    def step2():
        arr = [
        '2',
        '40',
        '0',
        '37',
        '5',
        '38',
        '0',
        '24'
        '1',
        '38',
        '10',
        '31',
        '0',
        '32',
        '38'
        ]
        # lexical_analysis = LexicalAnalysis()
        # lexical_analysis.perform_lexical_analysis()
        # pif = [str(x[0]) for x in lexical_analysis.PIF]
        # print(pif)
        alg = LR0Algorithm("input/grammar.txt")
        alg.canonical_collection()
        try:
            used_productions = alg.check_input(arr)
            alg.print_derivations(used_productions)
        except Exception as e:
            print(str(e))



if __name__ == '__main__':
    # Main.step1()
    Main.step2()

