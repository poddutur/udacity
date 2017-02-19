from utils import boxes, peers, unitlist


def grid_values(grid):
    values = []
    all_numbers = '123456789'
    for box in grid:
        if box in all_numbers:
            values.append(box)
        elif box == '.':
            values.append(all_numbers)
    assert len(values) == 81
    return dict(zip(boxes, values))


def eliminate(values):
    solved_values_keys = [box
                          for box in values.keys() if len(values[box]) == 1]
    for sovled_value_key in solved_values_keys:
        eliminate_number = values[sovled_value_key]
        for peer in peers[sovled_value_key]:
            values[peer] = values[peer].replace(eliminate_number, '')
    return values


def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            number_of_places = [box for box in unit if digit in values[unit]]
            if len(number_of_places) == 1:
                values[number_of_places[0]] = digit
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for
                                    box in values.keys()
                                    if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box
                                   for box in values.keys()
                                   if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[box]) == 1 for box in boxes):
        return values

    min_length, min_box = min((len(values[box]), box) for box in boxes if
                              len(values[box] > 1))
    for value in values[min_box]:
        new_values = values.copy()
        new_values[min_box] = value
        attempt = search(new_values)
        if attempt:
            return attempt
