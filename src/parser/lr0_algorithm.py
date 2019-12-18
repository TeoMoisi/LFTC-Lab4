from copy import deepcopy
from functools import reduce
from typing import List

from src.model.grammar import Grammar
from src.parser.actions import *


class LR0Algorithm:
    def __init__(self, text_file: str):
        self.grammar = Grammar()
        self.grammar.read_grammar_file(text_file)
        self.states = []  # list of states, each state has a list of lists lhs, rhs, i (i=dot)
        self.transitions_table = {}  # key: state, value: list of Action

    def check_conflicts(self, action, state_nr, next_state_nr, printing=False):
        if printing:
            print(self.transitions_table[state_nr])

        if state_nr in self.transitions_table:
            for existent in self.transitions_table[state_nr]:
                if existent.name == "reduce":
                    if action.name == "reduce":
                        raise Exception("Reduce reduce conflict in state " + str(state_nr) + " current state: " + str(next_state_nr))
                    if action.name == "shift":
                        raise Exception("Shift reduce conflict in state " + str(state_nr) + " current state: " + str(next_state_nr))
                elif existent.name == "shift":
                    if action.name == "reduce":
                        raise Exception("Shift reduce conflict in state " + str(state_nr) + " current state: " + str(next_state_nr))

    def closure(self, states_set):
        result = states_set
        for state in result:
            rhs = state[1]
            dot = state[2]

            if dot >= len(rhs) or rhs[dot] not in self.grammar.N:
                continue

            symbol = rhs[dot]
            # print("SYMBOL:", symbol)
            for right in self.grammar.get_productions_for_non_terminal(symbol):
                if [symbol, right[0], 0] not in result:
                    result.append([symbol, right[0], 0])

        return result

    def goto(self, state, symbol):
        result = []
        for analysis_element in state:
            rhs = analysis_element[1]
            dot = analysis_element[2]

            if dot >= len(rhs):
                continue

            current = rhs[dot]
            if current == symbol:
                elem = deepcopy(analysis_element)
                elem[2] += 1  # move the dot
                result.append(elem)

        return self.closure(result)

    def canonical_collection(self):
        s0 = self.closure([
            ["S\'", [self.grammar.S], 0]
        ])
        self.states.append(s0)

        i = 0
        for state in self.states:
            symbols_done = []
            for analysis_element in state:
                lhs = analysis_element[0]
                rhs = analysis_element[1]
                dot = analysis_element[2]

                action = None
                if dot >= len(rhs):  # the dot is at the end of rhs
                    if lhs == "S\'":  # accept
                        action = AcceptAction(i)
                        
                    else:  # reduce
                        productions = self.grammar.get_productions_for_non_terminal(lhs)
                        production_number = -1
                        for production in productions:
                            if production[0] == rhs:
                                production_number = production[1]
                                break

                        action = ReduceAction(i, production_number)

                else:  # shift
                    symbol = rhs[dot]
                    if symbol in symbols_done:
                        continue

                    next_state = self.goto(state, symbol)
                    symbols_done.append(symbol)

                    # am calculat goto, acum gasesc numarul state-ului nou ca sa il pun in tabel

                    try:
                        new_state_number = self.states.index(next_state)
                    except ValueError:
                        new_state_number = len(self.states)
                        self.states.append(next_state)

                    action = ShiftAction(i, new_state_number, symbol)
                if i == 2 and new_state_number == 23:
                    self.check_conflicts(action, i, new_state_number, True)
                if i not in self.transitions_table.keys():
                    self.transitions_table[i] = [action]
                else:
                    self.check_conflicts(action, i, new_state_number)
                    self.transitions_table[i].append(action)

            i += 1

        # # print the transitions (just for debugging)
        # for key in self.transitions_table.keys():
        #     for transition in self.transitions_table[key]:
        #         s = str(key) + " -> " + transition.name
        #         if transition.name == "shift":
        #             s += " with symbol " + transition.symbol + " to " + str(transition.next)
        #         elif transition.name == "reduce":
        #             s += " with production " + str(transition.production_number)
        #         print(s)

    def find_production(self, prod_nr):
        prod = [(x, tuple[0]) for x in self.grammar.P for tuple in self.grammar.P[x] if tuple[1] == prod_nr]
        return prod[0]

    def find_action_with_symbol(self, actions, symbol):
        for action in actions:
            if action.symbol == symbol:
                return action
        return -1

    def get_reverse_index(self, list, elem):
        for i in range(len(list) - 1, -1, -1):
            if list[i] == elem:
                return i
        return -1

    def check_input(self, sequence: List[str]):
        working = [0]
        input = sequence
        output = []
        accept = False
        error = False

        while not accept and not error:
            if len(working) == 0:
                error = True
                break
            head_working = working[-1]
            if len(input) == 0:
                head_input = "eps"
            else:
                head_input = input[0]

            transitions_table = self.transitions_table[head_working]
            if len(transitions_table) == 0:
                error = True
                break

            if transitions_table[0].name == "accept":
                print("accept " + str(head_working))
                accept = True
                break

            if transitions_table[0].name == "reduce":
                print("reduce "+str(head_working))
                prod_nr = transitions_table[0].production_number
                production = self.find_production(prod_nr)
                lhs, rhs = production[0], production[1]

                index_rhs = self.get_reverse_index(working, rhs[0])
                if index_rhs == -1:
                    error = True
                    break
                working = working[:index_rhs]+[lhs]
                action = self.find_action_with_symbol(self.transitions_table[working[-2]], lhs)
                if action == -1:
                    error = True
                    break
                working.append(action.next)

                output = [prod_nr] + output

            if transitions_table[0].name == "shift":
                if head_input != "eps":
                    input = input[1:]
                action = self.find_action_with_symbol(transitions_table, head_input)
                if action == -1:
                    error = True
                    break
                print("shift " + str(head_working) + " with " + head_input + " to "+str(action.next))
                working += [head_input, action.next]

        if accept:
            return output
        elif error:
            raise Exception("Grammar doesn't accept the given sequence!" + str(output))

    def print_derivations(self, used_productions):
        first_production = self.find_production(used_productions[0])
        derivations: List[str] = [
            first_production[0],
            self.string_rhs(first_production[1])
        ]
        for i in range(1, len(used_productions)):
            production_number = used_productions[i]
            current_production = self.find_production(production_number)
            rhs = self.string_rhs(current_production[1])
            next_derivation = derivations[-1][:]
            next_derivation = next_derivation.replace(current_production[0], rhs, 1)
            derivations.append(next_derivation)

        derivation_string: str = reduce(lambda x, y: x + " -> " + y, derivations)
        print(derivation_string)

    def string_rhs(self, rhs_list):
        return reduce(lambda x, y: x + y, rhs_list)
