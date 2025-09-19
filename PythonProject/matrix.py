import sys
import numpy as np

def get_matrix(name):
    print(f"\nEnter values for Matrix {name} (2x2):")
    matrix = []
    for i in range(2):
        while True:
            try:
                row = input(f"Enter row {i+1} (2 numbers separated by space): ").strip().split()
                row = [float(num) for num in row]
                if len(row) != 2:
                    raise ValueError("Each row must contain exactly 2 numbers.")
                matrix.append(row)
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")
    return np.array(matrix)

def main():
    # Step 1: Get user input
    a = get_matrix("A")
    b = get_matrix("B")

    # Step 2: Elementwise addition
    elementwise_add = a + b

    # Step 3: Elementwise multiplication
    elementwise_mul = a * b

    # Step 4: Matrix product
    matrix_product = a @ b  # or np.matmul(A, B)

    #Display the results
    print("\n====================== Results ======================")
    print("Matrix A:\n", a)
    print("\nMatrix B:\n", b)
    print("\nElementwise Addition (a + b):\n", elementwise_add)
    print("\nElementwise Multiplication (a * b):\n", elementwise_mul)
    print("\nMatrix Product (a @ b):\n", matrix_product)
    print("=====================================================\n")

    return 0

if __name__ == "__main__":
    sys.exit(main())