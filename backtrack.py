class CSP:
    def __init__(self, variables, domains):
        self.variables = variables  # variables to be constrained
        self.domains = domains  # domain of each variable
        self.constraints = {}
        self.count = 0

    def consistent(self, var, assignment):
        return True

    def select_variable(self,assignment,heuristic):
        if heuristic == "most_constrained":
            return self.most_constrained(assignment)
        elif heuristic == "most_constraining":
            return self.most_constraining(assignment)
        elif heuristic == "hybrid":
            return self.hybrid(assignment)

    def most_constrained(self,assignment):
        var = self.variables[self.count]
        self.count += 1
        return var

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
                        return assignment

                    else:
                        assignment.pop(variable)

            return None

        return result

# Returns a list of variables, and domains.
def read_file():
    file = open("input")
    lines = file.readlines()
    # List of variables.
    variables = [x+1 for x in range(len(lines)*2)]
    # Dictionary of domains
    domains = {}
    # Keeping track of Variables
    count = 0
    for line in lines:
        str_values = line.split("\\t")[1].rstrip().split(",")
        domain = []
        for value in str_values:
            domain.append(int(value))
        domains[variables[count]] = domain
        domains[variables[count+1]] = domain
        count += 2

    return variables, domains

def main():
    variables, domains = read_file()
    csp = CSP(variables,domains)
    resyi = csp.backtracking({}, "most_constrained")
    print(resyi)
main()