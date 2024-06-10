from exoscale.api.v2 import Client
from dotenv import load_dotenv
import os
from rich import print

load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
zone = "ch-gva-2"
client = Client(api_key, api_secret, zone=zone)

instance_name = "my-sdk-instance"


instance_types = client.list_instance_types()
print(instance_types)
instance_type = {"id": input("Enter the id of the instance type to create : ")}

template_ids = client.list_templates(visibility="public")
print(template_ids)
template = {"id": input("Enter the id of the template to use : ")}

ssh_keys = client.list_ssh_keys()
print(", ".join(list(map(lambda key: key["name"],ssh_keys["ssh-keys"]))))
ssh_key={"name": input("Enter the name of the ssh key to use: ")}

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

print(f"Security group rule:\n{sg_rule}\n")

attach_sg = client.attach_instance_to_security_group(
    id=security_group_id,
    instance={"id": instance_id}
)
print(f"Security group applied:\n{attach_sg}\n")