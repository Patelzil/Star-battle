import backtrack

class CSP:
    def __init__(self, variables, domains, size):
        self.variables = variables  # variables to be constrained
        self.domains = domains  # domain of each variable
        self.size = size  # domain of each variable
        self.constraints = {}
        self.count = 0
        self.max_ass = 0


        # print_output(assignment)
        # print the output of the solution
        #
        # assignment - dictionary containing the final solution to a puzzle
        # returns a string with the appropriate output
        def print_output(self, assignment):
            output = ""
            print(self.max_ass)
            # check for no solution
            if assignment is None:
                output = "No solution"
            else:
                for num in range(1, self.size * self.size + 1):
                    if (num % self.size) == 1:
                        output += "\n|"
                    if num in assignment.values():
                        output += "X|"
                    else:
                        output += ".|"
            print(output)


# def read_file():
#     file = open("input")
#     lines = file.readlines()
#     # List of variables.
#     variables = [x + 1 for x in range(len(lines) * 2)]
#     # Dictionary of domains
#     domains = {}
#     # Keeping track of Variables
#     count = 0
#     for line in lines:
#         str_values = line.split("\\t")[1].rstrip().split(",")
#         domain = []
#         for value in str_values:
#             domain.append(int(value))
#         domains[variables[count]] = domain
#         domains[variables[count + 1]] = domain
#         count += 2
#         # CHECK EDGE CASES
#     size = int(count / 2)
#     return variables, domains, size


def main():
    variables, domains, size = backtrack.read_file()
    backtrack.main()


main()
