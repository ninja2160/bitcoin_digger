from decimal import Decimal, getcontext
import math

class LongNumberCalculator:
    def __init__(self, precision=100):
        # Set the precision for decimal operations
        getcontext().prec = precision
    
    def add(self, num1, num2):
        return num1 + num2
    
    def subtract(self, num1, num2):
        return num1 - num2
    
    def multiply(self, num1, num2):
        return num1 * num2
    
    def divide(self, num1, num2):
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        return num1 / num2
    
    def power(self, base, exponent):
        return base ** exponent
    
    def modulus(self, num1, num2):
        return num1 % num2
    
    def sqrt(self, num):
        if num < 0:
            raise ValueError("Cannot calculate the square root of a negative number")
        return Decimal(num).sqrt()
    
    def log(self, num, base=10):
        if num <= 0:
            raise ValueError("Logarithm of non-positive number is undefined")
        return Decimal(math.log(num, base))
    
    def factorial(self, num):
        if num < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        return math.factorial(num)
    
    def gcd(self, num1, num2):
        return math.gcd(num1, num2)
    
# Usage example
calculator = LongNumberCalculator(precision=200)

# Large numbers
num1 = Decimal('1929868153955269923726183083478131797547292737984581739710086052358636024906')
num2 = Decimal('37')

# Performing operations

print("Multiplication:", calculator.multiply(num1, num2))

