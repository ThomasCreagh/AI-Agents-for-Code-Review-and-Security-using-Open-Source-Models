def double_value(number):
    # Doubles the input value
    doubled = number * 2
    return doubled

def halve_value(number):
    # Halves the input value
    return number / 2

def process_number(value):
    # Processes a number and returns based on conditions
    if value < 0:
        return "Negative"
    elif value == 0:
        return "Zero"
    else:
        return "Positive"

def combine_operations(input_value):
    # Combines multiple operations
    double_result = double_value(input_value)
    half_result = halve_value(input_value)
    return double_result + half_result