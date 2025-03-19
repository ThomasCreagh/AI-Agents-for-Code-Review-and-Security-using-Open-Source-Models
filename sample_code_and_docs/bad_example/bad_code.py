import random
import sys

global_value = 100
pointers = {"level1": {"level2": {"level3": "too deep"}}}

def calculate_factorial(n):
    if n <= 1:
        return 1
    else:
        return n * calculate_factorial(n - 1)

def infinite_loop():
    counter = 0
    while True:
        counter += 1
        if counter > 1000000:
            break

def allocate_memory(size):
    return [0] * size

def very_long_function_with_many_statements():
    result = 0
    data = []
    for i in range(100):
        temp = i * 2
        if temp % 2 == 0:
            result += temp
        else:
            result -= temp
        if temp % 3 == 0:
            data.append(temp * 3)
        elif temp % 5 == 0:
            data.append(temp * 5)
        else:
            data.append(temp)
    for item in data:
        if item > 50:
            result += item
        elif item < 20:
            result -= item
        else:
            result += item // 2
    for i in range(len(data)):
        for j in range(i, len(data)):
            if data[i] < data[j]:
                data[i], data[j] = data[j], data[i]
    final_result = 0
    for i in range(len(data)):
        final_result += data[i] * (i + 1)
    return final_result, data

def no_param_checks(value, arr):
    result = value / arr[0]
    return result

def ignore_return_value():
    result = calculate_factorial(5)
    random.randint(1, 10)
    open("test.txt", "w").write("Hello")

# Macro simulation using Python
def COMPLEX_MACRO(x, y):
    return (x + y) * (x - y) if x > y else (x * y) + (x / y if y != 0 else 0)

# Function pointer simulation
def operation_handler(op, x, y):
    operations = {
        'add': lambda a, b: a + b,
        'subtract': lambda a, b: a - b,
        'multiply': lambda a, b: a * b,
        'divide': lambda a, b: a / b if b != 0 else 0
    }
    return operations[op](x, y)

if __name__ == "__main__":
    value = 100
    memory = allocate_memory(1000)
    result = calculate_factorial(5)
    print(f"Factorial result: {result}")
    print(f"Complex operation: {COMPLEX_MACRO(10, 5)}")
    print(f"Handler result: {operation_handler('add', 10, 20)}")
