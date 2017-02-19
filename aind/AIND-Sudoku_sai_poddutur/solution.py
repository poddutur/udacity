assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    # to find naked twins sort the sting values in the boxes
    # make copy of values such that every string is arranged in ascending order of digits
    # this is required as later we are going to compare strings
    sorted_values = values.copy()
    for k in sorted_values.keys():
        int_list_value = [int(x) for x in sorted_values[k]]
        int_list_value.sort()
        sorted_values[k] = ''.join([str(x) for x in int_list_value])

    # get common boxes in each unit
    for unit in unitlist:
        # create a dict of common string (value) as key and boxes list as value
        common_value_box = dict()
        for box in unit:
            if sorted_values[box] in common_value_box.keys():
                common_value_box[sorted_values[box]].append(box)
            else:
                common_value_box[sorted_values[box]] = list()
                common_value_box[sorted_values[box]].append(box)

        # for each string value in the unit check if there are more than one box
        # which contain the same string
        for common_value in common_value_box.keys():
            if (len(common_value_box[common_value]) > 1) & (len(common_value_box[common_value]) == len(common_value)):
                # get all other boxes from which the common digits need to be removed
                other_boxes = [box for box in unit if box not in common_value_box[common_value]]
                # for each other box and for each digit in the common value / string remove them
                for other_box in other_boxes:
                    for digit in common_value:
                        values = assign_value(values=values, box=other_box, value=values[other_box].replace(digit, ''))

    return values


def cross(A, B):
    # making all two length combinations from elements of two stings"
    return [s + t for s in A for t in B]


boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_units = [[x[0] + x[1] for x in list(zip(rows, cols))], [x[0] + x[1] for x in list(zip(rows[::-1], cols))]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def grid_values(grid):
    values = dict()
    box_values = []
    all_numbers = '123456789'
    # create all the keys for the return dict
    assert(len(boxes)) == 81
    # for each square in the grid append if a number
    # else if it is empty append all numbers
    for box in grid:
        if box in all_numbers:
            box_values.append(box)
        elif box == '.':
            box_values.append(all_numbers)
    # check if the length is 9*9 & convert into dict
    assert len(box_values) == 81
    for i in range(0, len(boxes)):
        values[boxes[i]] = box_values[i]
    return values


def display(values):
    width = 1 + max(len(values[s]) for s in values.keys())
    # create the line which comes after section of 3 rows
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        # print the row with the acutal values
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    return


def eliminate(values):
    # get all solved boxes
    solved_boxes = [box for box in boxes if len(values[box]) == 1]
    # for each solved digit remove it from peers
    for solved_box in solved_boxes:
        digit_to_be_removed = values[solved_box]
        for peer_box in peers[solved_box]:
            values = assign_value(values=values, box=peer_box, value=values[peer_box].replace(digit_to_be_removed, ''))
    return values


def only_choice(values):
    # get number of places a digit occurs per unit
    for unit in unitlist:
        digits = '123456789'
        for digit in digits:
            numb_of_places = [box for box in unit if digit in values[box]]
            # if the number of places a digit occurs is 1, solve the place with digit
            if len(numb_of_places) == 1:
                values = assign_value(values=values, box=numb_of_places[0], value=digit)
    return values


def reduce_puzzle(values):
    stalled = False
    # keep going as long as we make progress in solving the puzzle
    # i.e number of solved boxes reduces
    while not stalled:
        num_solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # constraint propogation step
        # first elimination by checking peers
        values = eliminate(values)
        # filling in only choice boxes
        values = only_choice(values)
        # check for naked twins and remove necessary
        values = naked_twins(values)

        num_solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = num_solved_values_before == num_solved_values_after
        # the puzzle cannot be solved as one of the boxes has no possible values
        if len([box for box in values.keys() if len(values[box]) == 0]) > 0:
            return False
    return values


def search(values):
    # first reduce the puzzle and check if it can it cannot be solved
    values = reduce_puzzle(values)
    if values is False:
        return False
    # return puzzle if it is completely solved
    if all(len(values[box]) == 1 for box in boxes):
        return values
    # pick the box with min possibilities
    min_length, min_box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)
    # for each possibility search and if attempt succeeds return the attempt
    for possible_digit in values[min_box]:
        new_values = values.copy()
        new_values = assign_value(values=new_values, box=min_box, value=possible_digit)
        attempt = search(new_values)
        if attempt:
            return attempt


def solve(grid):
    # create puzzle dictionary
    values = grid_values(grid)
    return search(values)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    assert len(row_units) == 9
    assert len(column_units) == 9
    assert len(square_units) == 9
    assert len(diagonal_units) == 2
    for box in boxes:
        if box == 'E5':
            assert len(units[box]) == 5
        elif box in list(set(diagonal_units[0] + diagonal_units[1])):
            assert len(units[box]) == 4
        else:
            assert len(units[box]) == 3

    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass

    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
