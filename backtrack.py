#
# BACKTRACKING
# COMP 4190 Assignment 1
# Harsh Patel -7846258, Zil Patel - 7876456
#
import copy
import time
from multiprocessing import Process


class CSP:
    def __init__(self, variables, domains, size):
        self.variables = variables  # variables to be constrained
        self.domains = domains  # domain of each variable
        self.size = size  # domain of each variable
        self.constraints = {}
        self.count = 0
        self.nodes_visited = 0

    # check_neighbours(self, assignment, value)
    # Checks if all the neighbors of the value is valid in the assignment
    #
    # assignment - dictionary containing the currently assigned values
    # value - value to be added to the assignment
    # returns a boolean, true if all valid
    def check_neighbours(self, assignment, value):
        # Check if the value is directly neighbouring another variable
        for key in assignment:
            # value is cell number

            # check left cell
            if (value - 1) % self.size != 0:
                if assignment[key] == value - 1:
                    return False
            # check right cell
            if (value + 1) % self.size != 1:
                if assignment[key] == value + 1:
                    return False

            # check top cell, if top most cell don't check as it is out of bound
            if not (value - self.size <= 0):
                if assignment[key] == value - self.size:
                    return False
                # check top left cell if left most cell don't check top left don't check as it is out of bound
                if (value - self.size - 1) % self.size != 0:
                    if assignment[key] == value - self.size - 1:
                        return False
                # check top right cell, if right most don't check as it is out of bound
                if (value - self.size + 1) % self.size != 1:
                    if assignment[key] == value - self.size + 1:
                        return False

            # check bottom cell , if bottom row don't check as it is out of bound
            if (value + self.size) <= (self.size * self.size):
                if assignment[key] == value + self.size:
                    return False

                # check bottom left, if left most cell don't check as it is out of bound
                if (value + self.size - 1) % self.size != 0:
                    if assignment[key] == value + self.size - 1:
                        return False
                # check bottom right, right most cell don't check as it is out of bound
                if (value + self.size + 1) % self.size != 1:
                    if assignment[key] == value + self.size + 1:
                        return False

        return True

    # check_column(self, assignment, value)
    # Checks if the column has 2 assigned values
    #
    # assignment - dictionary containing the currently assigned values
    # value - value to be added to the assignment
    # returns a boolean, true if 1 or less assigned
    def check_column(self, assignment, value):
        count = 0

        for key in assignment:
            if (assignment[key] % self.size) == (value % self.size):
                count += 1
            if count == 2:
                return False
        return True

    # check_row(self, assignment, value)
    # Checks if the row has 2 assigned values
    #
    # assignment - dictionary containing the currently assigned values
    # value - value to be added to the assignment
    # returns a boolean, true if 1 or less assigned
    def check_row(self, assignment, value):
        count = 0
        for key in assignment:
            if ((assignment[key] - 1) // self.size) == ((value - 1) // self.size):
                count += 1
            if count == 2:
                return False
        return True

    # consistent(self, value, assignment):
    # Checks if the value is consistent with it's neighbours, row and column
    #
    # assignment - dictionary containing the currently assigned values
    # value - value to be added to the assignment
    # returns a boolean, true if consistent.
    def consistent(self, value, assignment):
        result = True
        # Check if any variable in the assignment has the same value
        for key in assignment:
            if assignment[key] == value:
                return False
        # Check if neighbours are valid.
        neighbours_valid = self.check_neighbours(assignment, value)

        # If neighbours are not valid return false.
        if not neighbours_valid:
            return False

        # Check if columns are valid.
        column_valid = self.check_column(assignment, value)
        # If column not valid return false.
        if not column_valid:
            return False

        # Check if rows are valid.
        row_valid = self.check_row(assignment, value)
        # If row not valid return false.
        if not row_valid:
            return False

        return result

    # select_variable(self, assignment, heuristic):
    # Selects which heuristic to pass in.
    #
    # assignment - dictionary containing the currently assigned values
    # heuristic - value to be added to the assignment
    def select_variable(self, assignment, heuristic):
        if heuristic == "most_constrained":
            return self.most_constrained(assignment)
        elif heuristic == "most_constraining":
            return self.most_constraining(assignment)
        elif heuristic == "hybrid":
            return self.hybrid(assignment)

    # reduce_domains(self, assignment)
    # reduces the domains of variables depending on the current assignment
    #
    # assignment - dictionary containing the currently assigned values
    # returns a dictionary that contains reduced domains
    def reduce_domains(self, assignment):
        # copy the domains of the variables
        reduced_domains = copy.deepcopy(self.domains)

        # for every variable not in assigment. Take each assigned value and remove value from domain
        for var in self.variables:
            if var not in assignment:
                for key in assignment:
                    assigned_value = assignment[key]  # variable
                    if assigned_value in reduced_domains[var]:
                        reduced_domains[var].remove(assigned_value)
                    # checking if assigned values are not neighbours to domain
                    # check and remove right
                    if (assigned_value + 1) % self.size != 1 and assigned_value + 1 in reduced_domains[var]:
                        reduced_domains[var].remove(assigned_value + 1)
                    # check and remove left
                    if (assigned_value - 1) % self.size != 0 and assigned_value - 1 in reduced_domains[var]:
                        reduced_domains[var].remove(assigned_value - 1)
                    # check and remove down
                    if (assigned_value + self.size) <= self.size * self.size and assigned_value + self.size in \
                            reduced_domains[var]:
                        reduced_domains[var].remove(assigned_value + self.size)
                    # check and remove top
                    if (assigned_value - self.size) > 0 and (assigned_value - self.size) in reduced_domains[var]:
                        reduced_domains[var].remove(assigned_value - self.size)
                    # check and remove top left
                    if (assigned_value - self.size - 1) % self.size != 0 and (assigned_value - self.size - 1) in \
                            reduced_domains[var]:
                        reduced_domains[var].remove(assigned_value - self.size - 1)
                    # check and remove top right
                    if (assigned_value - self.size + 1) % self.size != 1 and (assigned_value - self.size + 1) in \
                            reduced_domains[var]:
                        reduced_domains[var].remove(assigned_value - self.size + 1)
                    # check and remove bottom left
                    if (assigned_value + self.size - 1) % self.size != 0 and (assigned_value + self.size - 1) in \
                            reduced_domains[var]:
                        reduced_domains[var].remove(assigned_value + self.size - 1)
                    # check and remove bottom right
                    if (assigned_value + self.size + 1) % self.size != 1 and (assigned_value + self.size + 1) in \
                            reduced_domains[var]:
                        reduced_domains[var].remove(assigned_value + self.size + 1)

        # check and remove rows
        for var in self.variables:
            if var not in assignment:
                for value in reduced_domains[var]:
                    count_row = 0
                    for key in assignment:
                        assigned_value = assignment[key]  # variable
                        if ((assigned_value - 1) // self.size) == ((value - 1) // self.size):
                            count_row += 1
                        if count_row == 2 and value in reduced_domains[var]:
                            reduced_domains[var].remove(value)

        # check and remove columns
        for var in self.variables:
            if var not in assignment:
                for value in reduced_domains[var]:
                    count_column = 0
                    for key in assignment:
                        assigned_value = assignment[key]  # variable
                        if (assigned_value % self.size) == (value % self.size):
                            count_column += 1
                        if count_column == 2 and value in reduced_domains[var]:
                            reduced_domains[var].remove(value)

        return reduced_domains

    # most_constrained(self, assignment)
    # select the next node that has the fewest possible options left
    #
    # assignment - dictionary containing the currently assigned values
    # returns the most constrained variable
    def most_constrained(self, assignment):
        # count => checking the fewest possible options left.
        count = 2147483647
        most_constrained = -1

        reduced_domains = self.reduce_domains(assignment)

        for key in reduced_domains:
            if key not in assignment:
                if len(reduced_domains[key]) < count:
                    count = len(reduced_domains[key])
                    most_constrained = key

        return most_constrained

    # total_length(self, domains)
    # calculates the length of all the domains
    #
    # domains - used to calculate length
    # returns the total length of the domains passed
    def total_length(self, domains):
        result = 0
        for var in domains:
            result += len(domains[var])
        return result

    # get_neighbours(self, value):
    # Gets the list of neighbours
    #
    # value - checks the value's neighbours
    # returns the list of neighbours
    def get_neighbours(self, value):
        neighbours = [value]

        # right
        if (value + 1) % self.size != 1:
            neighbours.append(value + 1)

        # check and remove left
        if (value - 1) % self.size != 0:
            neighbours.append(value - 1)

        # check and remove down
        if (value + self.size) <= self.size * self.size:
            neighbours.append((value + self.size))

        # check and remove top
        if (value - self.size) > 0:
            neighbours.append((value - self.size))

        # check and remove top left
        if (value - self.size - 1) % self.size != 0:
            neighbours.append((value - self.size - 1))

        # check and remove top right
        if (value - self.size + 1) % self.size != 1:
            neighbours.append((value - self.size + 1))

        # check and remove bottom left
        if (value + self.size - 1) % self.size != 0:
            neighbours.append((value + self.size - 1))

        # check and remove bottom right
        if (value + self.size + 1) % self.size != 1:
            neighbours.append((value + self.size + 1))

        return neighbours

    # most_constraining(self, assignment)
    # select the next node that constraints the other nodes the most
    #
    # assignment - dictionary containing the currently assigned values
    # returns the most constraining variable
    def most_constraining(self, assignment):
        most_constraining = -1
        max_count = -1
        # Stores the list of lengths to check domains.
        list_of_lengths = {}

        # Reduces the domains for the assignment for checking.
        local_domains = self.reduce_domains(assignment)
        # Gets the list of neighbours.
        list_of_neighbours = {}

        # Go through all variables and get the neighbours.
        for variable in self.variables:
            if variable not in assignment:
                local_var = variable
                if len(local_domains[local_var]) != 0:
                    first_val = local_domains[local_var][0]

                    list_of_neighbours[variable] = self.get_neighbours(first_val)

        # Check for the number of variables that are constrained.
        count = 0
        for variable in list_of_neighbours:
            for value in list_of_neighbours[variable]:
                for var in self.variables:
                    if var not in assignment and var != variable:
                        if value in self.domains[var]:
                            count += 1

            list_of_lengths[variable] = count

        # Get the most constraining value.
        for key in list_of_lengths:
            if list_of_lengths[key] > max_count:
                most_constraining = key
                max_count = list_of_lengths[key]

        # Return the most constraining.
        local_assignment = assignment.copy()
        if most_constraining == -1:
            return most_constraining
        else:
            local_assignment[most_constraining] = self.domains[most_constraining][0]

        return most_constraining

    # hybrid(self, assignment):
    # Mixture of both most constraining and most constrained.
    #
    # assignment - dictionary containing the currently assigned values
    # returns the hybrid variable.
    def hybrid(self, assignment):
        hybrid_var = -1
        max_count = -1

        # Stores the list of lengths to check domains.
        list_of_lengths = {}

        # Reduces the domains for the assignment for checking.
        local_domains = self.reduce_domains(assignment)
        # Gets the list of neighbours.
        list_of_neighbours = {}

        # Go through all variables and get the neighbours.
        for variable in self.variables:
            if variable not in assignment:
                local_var = variable
                if len(local_domains[local_var]) != 0:
                    first_val = local_domains[local_var][0]

                    list_of_neighbours[variable] = self.get_neighbours(first_val)

        # Check for the number of variables that are constrained.
        count = 0
        for variable in list_of_neighbours:
            for value in list_of_neighbours[variable]:
                for var in self.variables:
                    if var not in assignment and var != variable:
                        if value in self.domains[var]:
                            count += 1

            list_of_lengths[variable] = count

        most_constrained_length = 2147483647
        # Get the hybrid value.
        for key in list_of_lengths:
            if list_of_lengths[key] > max_count and len(local_domains[key]) < most_constrained_length:
                hybrid_var = key
                max_count = list_of_lengths[key]
                most_constrained_length = len(local_domains[key])

        # Return hybrid selected variable.
        list_of_reduced_domains = {}
        local_assignment = assignment.copy()
        if hybrid_var == -1:
            return hybrid_var
        else:
            local_assignment[hybrid_var] = self.domains[hybrid_var][0]
        list_of_reduced_domains = self.reduce_domains(local_assignment)

        return hybrid_var

    # backtracking(self, assignment, heuristic):
    # Backtracking algorithm tht solves the heuristic.
    #
    # assignment - dictionary containing the currently assigned values
    # heuristic - heuristic to be used for algorithm
    # returns None if no solution, returns true if solution is correct.
    def backtracking(self, assignment, heuristic):
        # base case
        if len(assignment) == len(self.variables):
            return assignment
        else:
            # assignment is a dict
            # domain is a dict
            variable = self.select_variable(assignment, heuristic)
            if variable == -1:
                return None

            for value in self.domains[variable]:
                self.nodes_visited += 1
                # Check the consistency of value, if consistent then do recursion.
                if self.consistent(value, assignment):
                    assignment[variable] = value
                    result = self.backtracking(assignment, heuristic)

                    if result is not None:
                        return assignment  # final assignment.

                    assignment.pop(variable)
            return None

    # print_output(assignment)
    # print the output of the solution
    #
    # assignment - dictionary containing the final solution to a puzzle
    # returns a string with the appropriate output
    def print_output(self, assignment):
        output = ""

        # if no assignment then no solution
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

            # if assignment value should not exist in the grid then return no solution
            for var in assignment:
                if assignment[var] > self.size * self.size:
                    output = "No solution"

        print(output)
        print("\nNumber of Nodes:", self.nodes_visited)


# read_file
#
# Returns a list of variables, and domains.
def read_file(read_files):
    for file_name in read_files:
        file = open(file_name)
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
            # CHECK EDGE CASES
        size = int(count / 2)

        solve_csp(variables, domains, size)

# READING FILES AND PASSING HEURISTICS
def run_constrained(variables, domains, size):
    csp = CSP(variables, domains, size)
    constrained = csp.backtracking({}, "most_constrained")
    csp.print_output(constrained)

def run_constraining(variables, domains, size):
    csp = CSP(variables, domains, size)
    constraining = csp.backtracking({}, "most_constraining")
    csp.print_output(constraining)

def run_hybrid(variables, domains, size):
    csp = CSP(variables, domains, size)
    hybrid = csp.backtracking({}, "hybrid")
    csp.print_output(hybrid)

def solve_csp(variables, domains, size):
    solve = Process(target=run_constrained, args=(variables, domains, size))
    # Start the process
    solve.start()
    print("\nHeuristic 1: Most Constrained")
    start_time = time.time()
    solve.join(timeout=600) # time out after 10 min (600 seconds)
    print("Time taken: %s seconds" % (time.time() - start_time))
    solve.terminate()
    if (time.time() - start_time) >= 599:
        print("TIMED OUT!!")

    solve = Process(target=run_constraining, args=(variables, domains, size))
    # Start the process
    solve.start()
    print("\nHeuristic 2: Most Constraining")
    start_time = time.time()
    solve.join(timeout=600) # time out after 10 min (600 seconds)
    print("Time taken: %s seconds"  % (time.time() - start_time))
    if (time.time() - start_time) >= 599:
        print("TIMED OUT!!")

    solve.terminate()

    solve = Process(target=run_hybrid, args=(variables, domains, size))
    # Start the process
    solve.start()
    print("\nHeuristic 3: Hybrid")
    start_time = time.time()
    solve.join(timeout=600) # time out after 10 min (600 seconds)
    print("Time taken: %s seconds"  % (time.time() - start_time))
    solve.terminate()
    if (time.time() - start_time) >= 599:
        print("TIMED OUT!!")


def start():
    print("BACKTRACKING:")
    read_file(["input2"])


if __name__ == '__main__':
    start()