assignments = []
import collections

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]


digits = "123456789"
cols = '123456789'
rows = 'ABCDEFGHI'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        naked_candidates = collections.defaultdict(list)
        # build a {"35" - > B2 B3} dictionary
        for box in unit:
            naked_candidates[values[box]].append(box)
        # identify naked candidate:
        for k, v in naked_candidates.items():
            if len(k) == 2 and len(v) == 2:
                for box in unit:
                    if box not in v and len(values[box]) > 1:
                        values[box] = "".join([d for d in values[box] if d not in k])
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    return {box: value if value != '.' else digits for box, value in zip(boxes, "".join(grid))}


def display(values):
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    for k, v in values.items():
        if len(v) > 1:
            not_possible = set(values[box] for unit in filter(lambda u: k in u, unitlist) for box in unit if len(values[box]) == 1)
            values[k] = ''.join(num for num in v if num not in not_possible)
    return values


def only_choice(values):
    for unit in unitlist:
        for d in digits:
            d_possible = [box for box in unit if d in values[box]]
            if len(d_possible) == 1:
                values[d_possible[0]] = d
    return values


def count_solved(values):
    return sum([1 for v in values.values() if len(v) == 1])


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_before = count_solved(values)
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        ## TO DO, add naked_twins here
        solved_after = count_solved(values)
        stalled = solved_before == solved_after
        if len([1 for v in values.values() if len(v) == 0]):
            return False
    return values


def search(values):
    values = reduce_puzzle(values)
    if not values:
        return False
    elif count_solved(values) == 81:
        return values
    else:
        # recursively search
        min_choice = len(digits)
        min_boxes = []
        for box, choice in filter(lambda item: len(item[1]) > 1, values.items()):
            if len(choice) < min_choice:
                min_boxes = [box]
                min_choice = len(choice)
            elif len(choice) == min_choice:
                min_boxes.append(box)
        chosen_box = min_boxes[0]
        for digit in values[chosen_box]:
            new_values = dict(values)
            new_values[chosen_box] = digit
            result = search(new_values)
            if result:
                return result


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
