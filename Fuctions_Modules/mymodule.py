
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

# Only runs when this file is executed directly
if __name__ == "__main__":
    print("Running tests inside math_utils module...")
    print("Add: ", add(2, 3))          # 5
    print("Multiply: ", multiply(2, 3)) # 6
