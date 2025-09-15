"""Basic example: device information in simplified and tree formats."""

import syinfo as si


def main():
    info = si.get_hardware_info()
    print("CPU model:", info["cpu"]["model"])
    print("RAM total:", info["memory"]["total"])
    # Tree print (device only)
    si.print_system_tree(si.get_complete_info(include_network=False))


if __name__ == "__main__":
    main()


