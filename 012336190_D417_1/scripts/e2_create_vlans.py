from netmiko import ConnectHandler
import yaml
from datetime import datetime

INVENTORY = "inventory/switch_source.yml"
SSH_KEY = "/root/.ssh/id_rsa"
USERNAME = "admin"

# VLANs required by the scenario
REQUIRED_VLANS = ["user_Network", "ACCT_Network", "MGMT_Network", "IT_Network"]

def get_switches():
    with open(INVENTORY, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["switches"]

def main():
    print(f"Run time: {datetime.now().isoformat(timespec='seconds')}")
    switches = get_switches()

    for sw in switches:
        print("=" * 70)
        print(f"{sw['name']} ({sw['ip']}) - creating VLANs")

        device = {
            "device_type": "extreme_exos",
            "host": sw["ip"],
            "username": USERNAME,
            "use_keys": True,
            "key_file": SSH_KEY,
            "allow_agent": False,
        }

        conn = ConnectHandler(**device)

        # Create VLANs (safe to run repeatedly; errors will show if they already exist)
        for vlan in REQUIRED_VLANS:
            cmd = f"create vlan {vlan}"
            out = conn.send_command_timing(cmd)
            print(f"{cmd} -> {out.strip()}")

        conn.send_command_timing("save")
        conn.disconnect()

        print("[OK] Saved configuration")

if __name__ == "__main__":
    main()
