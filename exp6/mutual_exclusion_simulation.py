from lamport_clock import LamportClock
from logger import global_log, log_event


class ProcessNode(LamportClock):
    def __init__(self, pid, clock):
        super().__init__(pid)
        self.clock = clock

    def tick(self):
        self.time = max(self.time, self.clock.time) + 1
        self.clock.time = self.time
        return self.time

    def event(self, name):
        t = self.tick()
        log_event(self.process_id, name, t)
        return t

    def internal(self, n=2):
        for _ in range(n):
            self.event("Internal Event")

    def request(self):
        t = self.event("Requested Resource")
        return {"process_id": self.process_id, "timestamp": t}

    def release(self):
        return self.event("Released Resource")


class ResourceManager:
    def __init__(self, name):
        self.resource = name
        self.owner = None
        self.waiting = []
        self.clock = LamportClock("Global")

    def request_access(self, process):
        req = process.request()

        if not self.owner:
            self.owner = process.process_id
            log_event(process.process_id, f"Granted {
                      self.resource}", req["timestamp"])
            print(f"{process.process_id} gets {
                  self.resource} at logical time {req['timestamp']}")
        else:
            self.waiting.append(req)
            log_event(process.process_id,
                      "Waiting for Resource", req["timestamp"])
            print(f"{process.process_id} waits for {
                  self.resource} at logical time {req['timestamp']}")

    def release_access(self, process):
        if self.owner != process.process_id:
            return

        process.internal()
        t = process.release()
        self.owner = None
        self.clock.time = max(self.clock.time, t) + 1

        if self.waiting:
            req = self.waiting.pop(0)
            self.owner = req["process_id"]
            log_event(req["process_id"], f"Granted {
                      self.resource}", req["timestamp"])
            print(f"{req['process_id']} gets {
                  self.resource} at logical time {req['timestamp']}")

    def simulate(self, p):
        print("Simulating shared resource access")
        self.request_access(p[0])
        p[0].internal()
        self.request_access(p[1])
        self.release_access(p[0])
        self.request_access(p[2])
        self.release_access(p[1])


if __name__ == "__main__":
    global_log.clear()

    manager = ResourceManager("Printer")
    processes = [
        ProcessNode("P1", manager.clock),
        ProcessNode("P2", manager.clock),
        ProcessNode("P3", manager.clock),
    ]

    manager.simulate(processes)

    print("\nSorted Event Log")
    global_log.sort(key=lambda e: (e["Timestamp"], e["Process ID"]))

    for e in global_log:
        print(f"Timestamp: {e['Timestamp']} | Node: {
              e['Process ID']} | Event: {e['Event Type']}")
