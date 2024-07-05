from generator.atomic_statement import AtomicStatement
from generator.two_statement import TwoStatement
from generator.connection import Connection
from generator.argument import Argument

from enum import Enum

from typing import Optional, List
from random import choice, sample

class Generator:

    class Difficulty(Enum):
        EASY = "Easy"
        MEDIUM = "Medium"
        HARD = "Hard"

    def __init__(self, difficulty: Difficulty):
        self.difficulty = difficulty

    def generate_problem(self) -> list:
        
        if self.difficulty == Generator.Difficulty.EASY:
            # easy will have 2 total statements, 2 symbols
            s1 = self.__generate_two()
            s2 = self.__generate_atomic()

            while not self.__valid(s1, s2):
                s1 = self.__generate_two()
                s2 = self.__generate_atomic()

            return [s1, s2]

        if self.difficulty == Generator.Difficulty.MEDIUM:
            # medium will have 3 total statements, 3 symbols

            s1 = self.__generate_two()
            s2 = self.__generate_two()
            s3 = self.__generate_atomic()

            while not self.__valid(s1, s2, s3):
                s1 = self.__generate_two()
                s2 = self.__generate_two()
                s3 = self.__generate_atomic()

            return [s1, s2, s3]

        elif self.difficulty == Generator.Difficulty.HARD:
            # hard will have a total of 3 total statements, 5 symbols

            s1 = self.__generate_two()
            s2 = self.__generate_two()
            s3 = choice([self.__generate_atomic(), self.__generate_two()])

            while not self.__valid(s1, s2, s3):
                s1 = self.__generate_two()
                s2 = self.__generate_two()
                s3 = choice([self.__generate_atomic(), self.__generate_two()])

            return [s1, s2, s3]

    def __valid(self, *args):
        '''
        args should be a list of either AtomicStatement or TwoStatement
        '''
        s = set()

        for statement in args:
            if isinstance(statement, AtomicStatement):
                s.add(str(statement))
            elif isinstance(statement, TwoStatement):
                s.add(str(statement.first))
                s.add(str(statement.second))

        for atomic in s:
            if '~' in atomic:
                atomic = atomic[1]
            else:
                atomic = '~' + atomic

            if atomic in s:
                return False
            
        s2 = set()

        for statement in args:
            if str(statement) in s2:
                return False
            else:
                s2.add(str(statement))
        
        return True

    
    def __generate_two(self) -> TwoStatement:
        boolean_choices = [True, False]
        args = self.__generate_argument(2)
        arg1 = args[0]
        arg2 = args[1]

        as1 = AtomicStatement(arg1, choice(boolean_choices))
        connection = choice(list(Connection))
        as2 = AtomicStatement(arg2, choice(boolean_choices))

        return TwoStatement(as1, connection, as2)

    def __generate_atomic(self) -> AtomicStatement:
        boolean_choices = [True, False]
        return AtomicStatement(self.__generate_argument()[0], choice(boolean_choices))

    def __generate_argument(self, num: int = 1) -> List[Argument]:
        match self.difficulty:
            case Generator.Difficulty.EASY:
                upper = 2
            case Generator.Difficulty.MEDIUM:
                upper = 3
            case Generator.Difficulty.HARD:
                upper = 5

        return sample(list(Argument)[:upper], k=num)
    



        