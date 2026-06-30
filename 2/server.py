import Pyro4

@Pyro4.expose 
class Greeting: 
    def say_hello(self, name): 
        return f"Hello, {name}!"

@Pyro4.expose
class CalculatorService:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero!")
        return a / b
    
@Pyro4.expose
class StudentService:
    def getStudent(self):
        return "Alice"
        
# Setup the daemon and the name server 
daemon = Pyro4.Daemon() 
ns = Pyro4.locateNS() 

# Register the greeting object 
greeting_uri = daemon.register(Greeting)
calculator_uri = daemon.register(CalculatorService)
student_uri = daemon.register(StudentService)

ns.register("example.greeting", greeting_uri)
ns.register("example.calculator", calculator_uri)
ns.register("example.student", student_uri)

print("Server is ready...") 

daemon.requestLoop() 