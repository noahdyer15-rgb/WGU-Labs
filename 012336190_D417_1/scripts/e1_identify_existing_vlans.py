from netmiko import ConnectHandler
import yaml
from datetime import datetime

INVENTORY = "inventory/switch_source.yml"
SSH_KEY = "/root/.ssh/id_rsa"
USERNAME = "admin"

def get_switches():
    with open(INVENTORY, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["switches"]

def main():
    print(f"Run time: {datetime.now().isoformat(timespec='seconds')}")
    switches = get_switches()

    for sw in switches:
        print("=" * 70)
        print(f"{sw['name']} ({sw['ip']})")

        device = {
            "device_type": "extreme_exos",
            "host": sw["ip"],
            "username": USERNAME,
            "use_keys": True,
            "key_file": SSH_KEY,
            "allow_agent": False,
        }

        conn = ConnectHandler(**device)
        output = conn.send_command("show vlan")
        conn.disconnect()

        print(output)

if __name__ == "__main__":
    main()
