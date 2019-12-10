class Action:
    def __init__(self, current, name):
        self.current = current
        self.name = name


class ShiftAction(Action):
    def __init__(self, current, next, symbol):
        super().__init__(current, "shift")
        self.next = next
        self.symbol = symbol

    def __str__(self):
        return "shift " + str(self.current) + " with " + self.symbol + " to " + str(self.next)


class ReduceAction(Action):
    def __init__(self, current, production_number):
        super().__init__(current, "reduce")
        self.production_number = production_number

    def __str__(self):
        return "reduce " + str(self.current) + " with production " + str(self.production_number)


class AcceptAction(Action):
    def __init__(self, current):
        super().__init__(current, "accept")

    def __str__(self):
        return "accept " + str(self.current)
