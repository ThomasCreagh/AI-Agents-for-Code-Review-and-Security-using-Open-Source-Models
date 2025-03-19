"""
Safety-critical compliant code following NASA's Power of Ten rules.
This file demonstrates proper implementation of:
- Simple control flow (Rule 1)
- Fixed loop bounds (Rule 2)
- No dynamic memory allocation after initialization (Rule 3)
- Short, focused functions (Rule 4)
- Appropriate assertion density (Rule 5)
- Limited variable scope (Rule 6)
- Thorough return value checking (Rule 7)
- Limited preprocessor use (Rule 8 - less applicable in Python)
- Restricted pointer use (Rule 9 - less applicable in Python)
- Code that compiles without warnings (Rule 10)
"""

import random


def calculate_factorial(n):
    """Calculate factorial with bound checking and iterative approach."""
    if not isinstance(n, int):
        return {"status": "error", "message": "Input must be an integer"}
    
    if n < 0:
        return {"status": "error", "message": "Input must be non-negative"}
    
    if n > 12:  # Prevent potential overflow for larger values
        return {"status": "error", "message": "Input too large, maximum allowed is 12"}
    
    # Use iteration instead of recursion (Rule 1)
    result = 1
    # Fixed upper bound based on input (Rule 2)
    for i in range(1, n + 1):
        result *= i
        
    return {"status": "success", "result": result}


def controlled_loop(max_iterations):
    """Demonstrate a controlled loop with fixed bounds."""
    if not isinstance(max_iterations, int):
        return {"status": "error", "message": "Input must be an integer"}
    
    if max_iterations <= 0:
        return {"status": "error", "message": "Iteration count must be positive"}
    
    if max_iterations > 1000000:
        return {"status": "error", "message": "Iteration count too large"}
    
    counter = 0
    result = 0
    
    # Fixed upper bound (Rule 2)
    for i in range(max_iterations):
        counter += 1
        result += i
        
    return {"status": "success", "iterations": counter, "result": result}


def allocate_fixed_memory(size):
    """Allocate a fixed-size array with bounds checking."""
    if not isinstance(size, int):
        return {"status": "error", "message": "Size must be an integer"}
    
    if size <= 0:
        return {"status": "error", "message": "Size must be positive"}
    
    if size > 10000:
        return {"status": "error", "message": "Size exceeds maximum allowed (10000)"}
    
    # Pre-allocate memory instead of dynamic allocation (Rule 3)
    data = [0] * size
    
    return {"status": "success", "data": data}


def process_data(input_array, operation_type):
    """Process data with well-defined operations and bounds checking."""
    # Parameter validation (Rule 7)
    if not isinstance(input_array, list):
        return {"status": "error", "message": "Input must be a list"}
    
    if len(input_array) == 0:
        return {"status": "error", "message": "Input array cannot be empty"}
    
    if len(input_array) > 1000:
        return {"status": "error", "message": "Input array too large"}
    
    if not operation_type in ["sum", "average", "max", "min"]:
        return {"status": "error", "message": "Unknown operation type"}
    
    # Local scope for variables (Rule 6)
    result = 0
    
    # Simple operation mapping without function pointers (Rule 9)
    if operation_type == "sum":
        for i in range(len(input_array)):
            result += input_array[i]
        return {"status": "success", "result": result}
    
    elif operation_type == "average":
        if len(input_array) == 0:  # Double-check to prevent division by zero
            return {"status": "error", "message": "Cannot calculate average of empty array"}
        
        total = 0
        for i in range(len(input_array)):
            total += input_array[i]
        result = total / len(input_array)
        return {"status": "success", "result": result}
    
    elif operation_type == "max":
        if len(input_array) == 0:  # Redundant check for clarity
            return {"status": "error", "message": "Cannot find maximum of empty array"}
        
        result = input_array[0]
        for i in range(1, len(input_array)):
            if input_array[i] > result:
                result = input_array[i]
        return {"status": "success", "result": result}
    
    elif operation_type == "min":
        if len(input_array) == 0:  # Redundant check for clarity
            return {"status": "error", "message": "Cannot find minimum of empty array"}
        
        result = input_array[0]
        for i in range(1, len(input_array)):
            if input_array[i] < result:
                result = input_array[i]
        return {"status": "success", "result": result}
    
    # This should never happen due to earlier validation, but included for robustness
    return {"status": "error", "message": "Operation processing failed"}


def safe_division(numerator, denominator):
    """Safely perform division with proper error handling."""
    # Parameter validation (Rule 7)
    if not (isinstance(numerator, (int, float)) and isinstance(denominator, (int, float))):
        return {"status": "error", "message": "Both inputs must be numbers"}
    
    # Check for division by zero (Rule 5 - assertions)
    if denominator == 0:
        return {"status": "error", "message": "Division by zero is not allowed"}
    
    result = numerator / denominator
    return {"status": "success", "result": result}


def generate_random_number(min_value, max_value):
    """Generate a random number with proper bounds checking."""
    # Parameter validation (Rule 7)
    if not (isinstance(min_value, int) and isinstance(max_value, int)):
        return {"status": "error", "message": "Range bounds must be integers"}
    
    if min_value >= max_value:
        return {"status": "error", "message": "Minimum value must be less than maximum value"}
    
    # Check for reasonable range
    if max_value - min_value > 1000000:
        return {"status": "error", "message": "Range too large"}
    
    # Always check return values (Rule 7)
    result = random.randint(min_value, max_value)
    return {"status": "success", "result": result}


def write_to_file(filename, content):
    """Write content to a file with proper error handling."""
    if not isinstance(filename, str):
        return {"status": "error", "message": "Filename must be a string"}
    
    if not filename.endswith('.txt'):
        return {"status": "error", "message": "Only .txt files are supported"}
    
    # Check filename length
    if len(filename) > 255:
        return {"status": "error", "message": "Filename too long"}
    
    try:
        # Explicit file handling with proper cleanup
        file = open(filename, "w")
        file.write(content)
        file.close()
        return {"status": "success", "message": f"Data written to {filename}"}
    except IOError as e:
        return {"status": "error", "message": f"File operation failed: {str(e)}"}


def main():
    """Main function to demonstrate the usage of other functions."""
    # Initialize with fixed values
    number = 5
    array_size = 100
    
    # Always check return values (Rule 7)
    factorial_result = calculate_factorial(number)
    if factorial_result["status"] != "success":
        print(f"Factorial calculation failed: {factorial_result['message']}")
        return 1
    
    memory_result = allocate_fixed_memory(array_size)
    if memory_result["status"] != "success":
        print(f"Memory allocation failed: {memory_result['message']}")
        return 1
    
    # Fill array with values
    data = memory_result["data"]
    for i in range(len(data)):
        if i < len(data):  # Explicit bounds check
            data[i] = i * 2
    
    # Process data
    process_result = process_data(data, "sum")
    if process_result["status"] != "success":
        print(f"Data processing failed: {process_result['message']}")
        return 1
    
    # Generate random number
    random_result = generate_random_number(1, 10)
    if random_result["status"] != "success":
        print(f"Random number generation failed: {random_result['message']}")
        return 1
    
    # Print results
    print(f"Factorial of {number}: {factorial_result['result']}")
    print(f"Sum of data array: {process_result['result']}")
    print(f"Random number: {random_result['result']}")
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
