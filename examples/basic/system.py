"""Basic example: combined system info (device + network optional)."""

import syinfo as si


def main():
    # Simplified system info
    s = si.get_system_info()
    print("Hostname:", s["hostname"]) 
    print("System:", s["system_name"]) 
    print("CPU model:", s["cpu_model"]) 

    # Detailed tree (no network)
    si.print_system_tree(si.get_complete_info(include_network=False))


if __name__ == "__main__":
    main()


