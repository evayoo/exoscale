from exoscale.api.v2 import Client
from dotenv import load_dotenv
import os
from rich import print

# Client from exoscale.api.v2 is used to interact with the Exoscale API.
# load_dotenv and os are used to load environment variables from a .env file.
# print from rich is used to format and display output in the terminal.

load_dotenv() # Loads the environment variables from a .env file into the script's environment.

# we are getting these values from the environment variables
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
zone = "ch-gva-2"
client = Client(api_key, api_secret, zone=zone)

# Retrieves API_KEY and API_SECRET from environment variables. 
# Creates a Client instance to interact with Exoscale using the API credentials.

instance_name = "my-instance"

#execute the code

instance_types = client.list_instance_types()
print(instance_types)
instance_type = {"id": input("Enter the id of the instance type to create : ")}

# Lists available instance types and prints them.
# Prompts the user to input the ID of the desired instance type.

template_ids = client.list_templates(visibility="public")
print(template_ids)
template = {"id": input("Enter the id of the template to use : ")}

# Lists public templates and prints them.
# Prompts the user to input the ID of the desired template.

ssh_keys = client.list_ssh_keys()
print(", ".join(list(map(lambda key: key["name"],ssh_keys["ssh-keys"]))))
ssh_key={"name": input("Enter the name of the ssh key to use: ")}

# Lists available SSH keys and prints their names.
# Prompts the user to input the name of the desired SSH key.

instance = client.create_instance(
    name=instance_name,
    instance_type=instance_type,
    template=template,
    ssh_key=ssh_key,
    disk_size=50,
)
print(f"instance info:\n{instance}\n")
instance_id = instance["reference"]["id"]
delete_protection = client.add_instance_protection(id=instance_id)
print(f"Delete protection info:\n{delete_protection}\n")

# Creates a new instance with the specified configuration.
# Adds delete protection to the newly created instance.

list_security_groups = client.list_security_groups()['security-groups']
security_group = None
for sg in list_security_groups:
    if sg['name'] == "allow-ping":
        security_group = sg
        sg_rule = None
        for rule in security_group['rules']:
            if rule['description'] == "Allow ICMP (ping) traffic":
                sg_rule = rule
                break
        security_group_id = security_group['id']
        if sg_rule is None:
            sg_rule = client.add_rule_to_security_group(
            id=security_group_id, 
            flow_direction="ingress",
            description="Allow ICMP (ping) traffic",
            network="0.0.0.0/0",
            protocol="icmp",
            icmp={"type": -1, "code": -1}
        )
        break

   # Lists all security groups and checks if a group named "allow-ping" exists.
# If it exists, it checks if it already has a rule to allow ICMP (ping) traffic. If not, it adds the rule.


if security_group is None:
    security_group = client.create_security_group(name="allow-ping")
    security_group_id = security_group['reference']['id']
    print(f"security group info:\n{security_group}\n")
    sg_rule = client.add_rule_to_security_group(
        id=security_group_id, 
        flow_direction="ingress",
        description="Allow ICMP (ping) traffic",
        network="0.0.0.0/0",
        protocol="icmp",
        icmp={"type": -1, "code": -1}
    )

    # If the "allow-ping" security group does not exist, it creates it and adds the ICMP (ping) rule.  

print(f"Security group rule:\n{sg_rule}\n")

attach_sg = client.attach_instance_to_security_group(
    id=security_group_id,
    instance={"id": instance_id}
)
print(f"Security group applied:\n{attach_sg}\n")

# Attaches the security group to the newly created instance.