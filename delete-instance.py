from exoscale.api.v2 import Client
from dotenv import load_dotenv
import os
from rich import print



load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
zone = "ch-gva-2"
client = Client(api_key, api_secret, zone=zone)

instance_id = input("Enter the instance id that you want to delete: ")

# Prompts the user to input the ID of the instance they want to delete.

client.remove_instance_protection(id=instance_id)
print(f"Protection removed from instance:\n{instance_id}\n")

# Removes delete protection from the specified instance.
# Prints a message confirming the removal of protection from the instance.

client.delete_instance(id=instance_id)
print(f"Instance {instance_id} deleted successfully")

# Deletes the specified instance.
# Prints a message confirming the successful deletion of the instance.