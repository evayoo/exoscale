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

client.remove_instance_protection(id=instance_id)
print(f"Protection removed from instance:\n{instance_id}\n")

client.delete_instance(id=instance_id)
print(f"Instance {instance_id} deleted successfully")