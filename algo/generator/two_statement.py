from generator.connection import Connection
from generator.atomic_statement import AtomicStatement

class TwoStatement():

    def __init__(self, first: AtomicStatement, connection: Connection, second: AtomicStatement):
        self.first = first
        self.second = second
        self.connection = connection

    
    def __str__(self) -> str:
        return f'({str(self.first)} {self.connection.value} {str(self.second)})'