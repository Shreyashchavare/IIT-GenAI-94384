import arithmetic

if __name__ == "__main__":
    a = 10
    b = 5

    sum_result = arithmetic.add(a, b)
    diff_result = arithmetic.subtract(a, b)
    prod_result = arithmetic.multiply(a, b)
    quot_result = arithmetic.divide(a, b)

    print(f"Addition: {a} + {b} = {sum_result}")
    print(f"Subtraction: {a} - {b} = {diff_result}")
    print(f"Multiplication: {a} * {b} = {prod_result}")
    print(f"Division: {a} / {b} = {quot_result}")