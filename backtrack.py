import copy

class CSP:
    def __init__(self, variables, domains, size):
        self.variables = variables  # variables to be constrained
        self.domains = domains  # domain of each variable
        self.size = size  # domain of each variable
        self.constraints = {}
        self.count = 0

    def check_neighbours(self, assignment, value):
        # Check if the value is directly neighbouring another variable
        for key in assignment:
            # value is cell number
            # check left cell
            if (assignment[key] == value - 1) and (value - 1 % self.size != 0):
                return False
            # check right cell
            if (assignment[key] == value + 1) and (value + 1 % self.size != 1):
                return False
            # check top cell
            if (assignment[key] == value - self.size) or (value - self.size <= 0):
                return False
            # check top left cell
            if (assignment[key] == value - self.size - 1) or (value - self.size <= 0):
                return False
            # check top right cell
            if (assignment[key] == value - self.size + 1) or (value - self.size <= 0):
                return False

            # check bottom cell
            if (assignment[key] == value + self.size) or (value + self.size > self.size * self.size):
                return False
            # check bottom left
            if (assignment[key] == value + self.size - 1) or (value + self.size > self.size * self.size):
                return False
            # check bottom right
            if (assignment[key] == value + self.size + 1) or (value + self.size > self.size * self.size):
                return False


        return True

    def check_column(self, assignment, value):
        count = 0

        for key in assignment:
            if (assignment[key] % self.size) == (value % self.size):
                count += 1
            if count == 2:
                return False
        return True

    def check_row(self, assignment, value):
        count = 0
        for key in assignment:
            if int((assignment[key] - 1) / self.size) == int((value - 1) / self.size):
                count += 1
            if count == 2:
                return False
        return True

    # need to pass variable for block check
    def consistent(self, value, variable, assignment):
        result = True
        # Check if any variable in the assignment has the same value
        for key in assignment:
            if assignment[key] == value:
                return False

        neighbours_valid = self.check_neighbours(assignment, value)

        if not neighbours_valid:
            return False

        column_valid = self.check_column(assignment, value)
        # check column
        if not column_valid:
            return False

        row_valid = self.check_row(assignment, value)
        # check column
        if not row_valid:
            return False

        return result

    def select_variable(self, assignment, heuristic):
        if heuristic == "most_constrained":
            return self.most_constrained(assignment)
        elif heuristic == "most_constraining":
            return self.most_constraining(assignment)
        elif heuristic == "hybrid":
            return self.hybrid(assignment)

    def most_constrained(self, assignment):
        count = 2147483647
        most_constrained = -1

        reduced_domains = copy.deepcopy(self.domains)

        for var in self.variables:
            if var not in assignment:
                for key in assignment:
                    assigned_value = assignment[key]  # variable
                    if assigned_value in reduced_domains[var]:
                        reduced_domains[var].remove(assigned_value)

        for key in reduced_domains:
            if key not in assignment:
                if len(reduced_domains[key]) < count:
                    count = len(reduced_domains[key])
                    most_constrained = key


        return most_constrained

    def most_constraining(self, assignment):
        pass

    def hybrid(self, assignment):
        pass

    def backtracking(self, assignment, heuristic):
        result = {}
        # base case
        if len(assignment) == len(self.variables):
            result = assignment
        else:
            # assignment is a dict
            # domain is a dict
            variable = self.select_variable(assignment, heuristic)
            # d[v] //edit so FC
            if variable == -1:
                return assignment

            for value in self.domains[variable]:
                if self.consistent(value, variable, assignment):
                    assignment[variable] = value
                    result = self.backtracking(assignment, heuristic)

                    if result is not None:
                        return assignment
                    else:
                        assignment.pop(variable)

            return assignment

        return result


# Returns a list of variables, and domains.
def read_file():
    file = open("input")
    lines = file.readlines()
    # List of variables.
    variables = [x + 1 for x in range(len(lines) * 2)]
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
        domains[variables[count + 1]] = domain
        count += 2
    size = int(count / 2)
    return variables, domains, size


def main():
    variables, domains, size = read_file()
    csp = CSP(variables, domains, size)
    resyi = csp.backtracking({}, "most_constrained")
    print(resyi)


    hars = {"z":[1,2]}
    if "h" not in hars:
        print("not in")

main()