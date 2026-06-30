import Pyro4

# Connect to the server using the URI 
greeting = Pyro4.Proxy("PYRONAME:example.greeting") 
calculator = Pyro4.Proxy("PYRONAME:example.calculator")
student = Pyro4.Proxy("PYRONAME:example.student")


# Call remote method
print(greeting.greet())

result = calculator.add(15, 10)
result2 = calculator.subtract(15, 10)
result3 = calculator.divide(15, 10)
print(f"Addition result: {result}")
print(f"Subtraction result: {result2}")