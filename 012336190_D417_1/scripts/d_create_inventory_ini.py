import configparser
from pathlib import Path
import yaml

SRC = Path("inventory/switch_source.yml")
OUT = Path("inventory/switches.ini")

GROUP_NAME = "access_closet_1"


def bool_to_ini(value) -> str:
    """Normalize YAML boolean-ish values to INI-friendly strings."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    s = str(value).strip().lower()
    if s in {"true", "yes", "y", "1"}:
        return "true"
    if s in {"false", "no", "n", "0"}:
        return "false"
    return str(value)


def main() -> None:
    if not SRC.exists():
        raise FileNotFoundError(f"Missing source file: {SRC}")

    data = yaml.safe_load(SRC.read_text(encoding="utf-8")) or {}
    switches = data.get("switches", [])

    if not switches:
        raise ValueError("No switches found in inventory/switch_source.yml under key: switches")

    cfg = configparser.ConfigParser(allow_no_value=True)
    cfg.optionxform = str  # preserve case for hostnames/keys

    if not cfg.has_section(GROUP_NAME):
        cfg.add_section(GROUP_NAME)

    for sw in switches:
        name = sw.get("name")
        ip = sw.get("ip")

        if not name or not ip:
            raise ValueError(f"Each switch must have 'name' and 'ip'. Problem entry: {sw}")

        # Build one-line host vars (INI inventory style)
        hostvars = [
            f"ansible_host={ip}",
            f"ram=\"{sw.get('ram', '')}\"",
            f"vcpus=\"{sw.get('vcpus', '')}\"",
            f"qemu_binary=\"{sw.get('qemu_binary', '')}\"",
            f"boot_priority=\"{sw.get('boot_priority', '')}\"",
            f"on_close=\"{sw.get('on_close', '')}\"",
            f"console_type=\"{sw.get('console_type', '')}\"",
            f"adapters=\"{sw.get('adapters', '')}\"",
            f"base_mac=\"{sw.get('base_mac', '')}\"",
            f"nic_type=\"{sw.get('nic_type', '')}\"",
            f"replicate_link_state={bool_to_ini(sw.get('replicate_link_state', ''))}",
        ]

        cfg.set(GROUP_NAME, name, " ".join(hostvars))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        cfg.write(f)

    print(f"[OK] Wrote INI inventory: {OUT}")
    print(f"[OK] Group: [{GROUP_NAME}] | Hosts: {len(switches)}")


if __name__ == "__main__":
    main()
