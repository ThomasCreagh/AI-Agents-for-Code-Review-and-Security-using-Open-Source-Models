def double_value(number):
    doubled = number * 2
    return doubled

def halve_value(number):
    return number / 2

def process_number(value):
    if value < 0:
        return "Negative"
    elif value == 0:
        return "Zero"
    else:
        return "Positive"

def combine_operations(input_value):
    double_result = double_value(input_value)
    half_result = halve_value(input_value)
    return double_result + half_result