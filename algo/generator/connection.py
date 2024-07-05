import enum

class Connection(enum.Enum):
    CONJUNCTION = '^'     # and
    DISJUNCTION = 'v'     # or
    IMPLICATION = '->'    # conditional
    BICONDITIONAL = '<->' # equivalence