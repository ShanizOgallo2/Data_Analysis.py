import sys
import numpy as np

def main():
    a = np.array([[3,2],
                  [1,9]])

    b =np.array([[7,5],
                 [4,8]])
    print(a)
    print(b)

    addition_result = a + b
    print("Elementwise addition result: ", addition_result)

    multiplication_result = a * b
    print("Elementwise multiplication result: ", multiplication_result)

    matmul_result = a @ b
    print("Matrix multiplication result: ", matmul_result)

    return 0

if __name__ == "__main__":
    sys.exit(main())