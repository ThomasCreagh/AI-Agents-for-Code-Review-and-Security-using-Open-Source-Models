def add_numbers(a, b):
    # Simple addition of two numbers
    result = a + b
    return result

def subtract_numbers(a, b):
    # Subtracts second number from first
    return a - b

def multiply_numbers(a, b):
    # Multiplies two numbers together
    product = a * b
    if product > 100:
        return "Large number"
    return product

def calculate_all(x, y):
    # Performs all operations and returns multiple values
    add_result = add_numbers(x, y)
    sub_result = subtract_numbers(x, y)
    mult_result = multiply_numbers(x, y)
    return add_result, sub_result, mult_result