import client
import messageManager
from server import ServerManager



def main():

    port = 8080  # Vous pouvez choisir un autre port si nécessaire
    server = ServerManager(port)
    print(f"Running server on port {port}")
    server.run()


if __name__ == "__main__":
    main()