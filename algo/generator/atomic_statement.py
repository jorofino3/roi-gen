from generator.argument import Argument
import numpy as np

class AtomicStatement():

    def __init__(self, argument: Argument, negated: bool = False):
        self.argument = argument
        self.negated = negated

    def __str__(self) -> str:
       base = f'{self.argument.value}'
       return f'~{base}' if self.negated else base
    
    def __eq__(self, other):
        if isinstance(other, AtomicStatement):
            return (self.argument == other.argument) and (self.negated == other.negated)
        return False
    
    def __hash__(self):
        return hash((self.argument, self.negated))
