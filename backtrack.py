class CSP:
    def __init__(self, variables, domains):
        self.variables = variables  # variables to be constrained
        self.domains = domains  # domain of each variable
        self.constraints = {}

    def consistent(self, var, assignment):
        pass

    def select_variable(self,assignment,heuristic):
        if heuristic == "most_constrained":
            return self.most_constrained(assignment)
        elif heuristic == "most_constraining":
            return self.most_constraining(assignment)
        elif heuristic == "hybrid":
            return self.hybrid(assignment)

    def most_constrained(self,assignment):
        pass

    def most_constraining(self,assignment):
        pass

    def hybrid(self,assignment):
        pass

    def backtracking(self, assignment,heuristic):
        result = {}
        # base case
        if len(assignment) == len(self.variables):
            result = assignment
        else:
            # assignment is a dict
            # domain is a dict
            variable = self.select_variable(assignment,heuristic)
            # d[v] //edit so FC
            for value in self.domains[variable]:
                if self.consistent(value, assignment):
                    assignment[variable] = value
                    result = self.backtracking(assignment, heuristic)

                    if result is not None:
                        result = assignment

                    else:
                        assignment.pop(variable)

            return None

        return result