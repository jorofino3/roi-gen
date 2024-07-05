import os
import subprocess
import json
from solver.solver import Solver
from generator.generator import Generator

class Executor():

    def __init__(self) -> None:

        self.solver = Solver()
        self.easy_generator = Generator(Generator.Difficulty.EASY)
        self.med_generator = Generator(Generator.Difficulty.MEDIUM)
        self.hard_generator = Generator(Generator.Difficulty.HARD)

    def is_atomic(self, statement):
        return len(statement) == 1

    def generate_problem(self, difficulty):

        premises = None

        if difficulty == 'easy':
            premises = self.easy_generator.generate_problem()
        elif difficulty == 'medium':
            premises =  self.med_generator.generate_problem()
        elif difficulty == 'hard':
            premises = self.hard_generator.generate_problem()

        if not premises:
            raise Exception("Invalid difficulty level")

        return [str(premise) for premise in premises]

    def attempt_solve(self, premises):

        generated_solution = self.solver.solve(premises)
        atomic_statements = {}
        atomic_premises = set()

        for line in premises:
            if self.is_atomic(line.strip()):
                atomic_premises.add(line)

        for line in generated_solution:
            split_line = line.split('|')
            # if the line only consists of \n then skip it
            if len(split_line) <= 1:
                continue

            statement, reason = split_line

            # statement will be in the form of x. statement
            statment_num = int(statement.split('.')[0].strip())
            statement = statement.split('.')[1].strip()
            reason = reason.strip()

            # if the reason is not a premise, then check if it is an atomic statement
            if reason != 'Premise':
                if self.is_atomic(statement) and statement not in atomic_statements and statement not in atomic_premises:
                    atomic_statements[statement] = statment_num
            
        return (generated_solution, atomic_statements)
                
    def generate(self, difficulty):

        premises = None
        solution = None
        atomic_statements = None
        res = []

        while (True):

            premises = self.generate_problem(difficulty)
            solution, atomic_statements = self.attempt_solve(premises)

            if len(atomic_statements) != 0:
                break
        
        conclusion = max(atomic_statements, key=atomic_statements.get) 

        statements = set()

        for line in solution:
            split_line = line.split('|')
            statement = split_line[0]
            statment_num = int(statement.split('.')[0].strip())

            if statement not in statements:
                res.append(line)
                statements.add(statement)

            if statment_num == atomic_statements[conclusion]:
                break
        
        return {
            "premises": premises,
            "conclusion": conclusion,
            "solution": res,
        }

def test():
    executor = Executor()
    print(json.dumps(executor.generate('medium')))

if __name__ == "__main__":
    test()