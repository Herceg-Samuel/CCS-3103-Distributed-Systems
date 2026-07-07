import json
import os
from collections import OrderedDict
import ipaddress

DATABASE = "dns.json"
CACHE_SIZE = 5


# Load DNS Database
def load_database():
    if not os.path.exists(DATABASE):
        with open(DATABASE, "w") as f:
            json.dump({}, f, indent=4)

    with open(DATABASE, "r") as f:
        return json.load(f)



# Save DNS Database
def save_database():
    with open(DATABASE, "w") as f:
        json.dump(dns, f, indent=4)



# DNS Database
dns = load_database()

# Cache stores recent lookups
cache = OrderedDict()



# Cache Functions
def cache_lookup(path):
    if path in cache:
        print("[CACHE HIT]")
        cache.move_to_end(path)
        return cache[path]

    print("[CACHE MISS]")
    return None


def cache_store(path, ip):
    if path in cache:
        cache.move_to_end(path)

    cache[path] = ip

    if len(cache) > CACHE_SIZE:
        cache.popitem(last=False)



# Navigate Hierarchy
# Should return the parent dictionary
def traverse(path, create=False):
    """
    Example path:
    africa/kenya/nairobi/server1

    Returns:
    {
        "server1": "192.168.1.2",
        ...
    }

    Parent dictionary and final key.
    """

    parts = path.split("/")

    current = dns

    for part in parts[:-1]:

        if part not in current:

            if create:
                current[part] = {}
            else:
                return None, None

        current = current[part]

    return current, parts[-1]



# REGISTER
def register(path, ip):

    # Validating the IP address
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        print("Invalid IP address.")
        return

    parent, server = traverse(path, create=True)

    if server in parent:
        print("Record already exists.")
        return

    parent[server] = ip

    save_database()

    print("Record registered successfully.")



# LOOKUP
def lookup(path):

    cached = cache_lookup(path)

    if cached:
        print(f"IP Address: {cached}")
        return

    parent, server = traverse(path)

    if parent is None or server not in parent:
        print("Record not found.")
        return

    ip = parent[server]

    cache_store(path, ip)

    print(f"IP Address: {ip}")


# UPDATE
def update(path, new_ip):

    # Validate the new IP address
    try:
        ipaddress.ip_address(new_ip)
    except ValueError:
        print("Invalid IP address.")
        return

    parent, server = traverse(path)

    if parent is None or server not in parent:
        print("Record not found.")
        return

    parent[server] = new_ip

    # Update cache if this record was recently looked up
    if path in cache:
        cache[path] = new_ip
        cache.move_to_end(path)

    save_database()

    print("Record updated successfully.")


# DELETE
def delete(path):

    parent, server = traverse(path)

    if parent is None or server not in parent:
        print("Record not found.")
        return

    del parent[server]

    # Remove from cache if present
    cache.pop(path, None)

    save_database()

    print("Record deleted successfully.")



# LIST ALL RECORDS
def list_records(current=None, prefix=""):

    if current is None:
        current = dns

    for key, value in current.items():

        if isinstance(value, dict):
            list_records(value, prefix + key + "/")
        else:
            print(f"{prefix}{key} -> {value}")



# HELP
def help_menu():

    print("""
Available Commands
------------------

REGISTER <path> <ip>
    Example:
    REGISTER africa/kenya/nairobi/server1 192.168.1.2

LOOKUP <path>
    Example:
    LOOKUP africa/kenya/nairobi/server1

UPDATE <path> <new_ip>
    Example:
    UPDATE africa/kenya/nairobi/server1 192.168.1.100

DELETE <path>
    Example:
    DELETE africa/kenya/nairobi/server1

LIST
    Displays every record in the database.

HELP
    Displays this help menu.

EXIT
    Closes the program.
""")



# MAIN PROGRAM
print("Loading System ...")
print(" Simplified Hierarchical DNS Server ")
print("")

help_menu()

while True:

    command = input("\nDNS> ").strip()

    if not command:
        continue

    parts = command.split()

    action = parts[0].upper()

    try:

        if action == "REGISTER":

            if len(parts) != 3:
                print("Usage: REGISTER <path> <ip>")
                continue

            register(parts[1], parts[2])

        elif action == "LOOKUP":

            if len(parts) != 2:
                print("Usage: LOOKUP <path>")
                continue

            lookup(parts[1])

        elif action == "UPDATE":

            if len(parts) != 3:
                print("Usage: UPDATE <path> <new_ip>")
                continue

            update(parts[1], parts[2])

        elif action == "DELETE":

            if len(parts) != 2:
                print("Usage: DELETE <path>")
                continue

            delete(parts[1])

        elif action == "LIST":

            print("\nDNS Records")
            print("----------------------")
            list_records()

        elif action == "HELP":

            help_menu()

        elif action == "EXIT":

            print("Goodbye!")
            break

        else:

            print("Unknown command. Type HELP.")

    except Exception as e:

        print(f"Error: {e}")