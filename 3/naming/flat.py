# Flat Naming System 
 
name_server = { "server1": "192.168.1.2", "server2": "192.168.1.3" }
 # Query 
server = name_server.get("server1", None) 
print(f"IP address of server1: {server}")