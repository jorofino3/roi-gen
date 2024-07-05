import subprocess
import sys
from typing import Any


class Solver():

    def __init__(self):
        self.command = ["java", "-cp", "solver/bin", "Solver"]

    def solve(self, premises):

        new_command = self.command[:]

        for premise in premises:
            new_command.append(premise)
        
        res = subprocess.run(new_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        premises = res.stdout.split("\n")

        return premises