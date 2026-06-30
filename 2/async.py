import Pyro4
import time


def main():
    generate_report_uri = "PYRONAME:example.generatereport"
    generate_report_proxy = Pyro4.Proxy(generate_report_uri)
    print("Calling the method synchronously")
    start = time.time()
    value = generate_report_proxy.generateReport()
    end = time.time()
    print(value)
    print(f"The call to generateReport took {end - start} seconds")

    print("Calling the method asynchronously")
    Pyro4.asyncproxy(generate_report_proxy)
    print("Sending request ...")
    future = generate_report_proxy.generateReport()

    for i in range(10):
        print(f"Performing other work: {i}")

    result = future.value
    print(result)


if __name__ == "__main__":
    main()
