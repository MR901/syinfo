"""Basic example: combined system info (device + network)."""

from syinfo import SystemInfo


def main():
    # Gather full system info (device + network)
    s = SystemInfo.get_all(search_period=0, search_device_vendor_too=False)

    # Print some key fields
    host = s.get("dev_info", {}).get("static_hostname", "Unknown")
    cpu_physical = s.get("cpu_info", {}).get("cores", {}).get("physical", "-")
    cpu_total = s.get("cpu_info", {}).get("cores", {}).get("total", "-")
    print("Hostname:", host)
    print("CPU cores (physical/total):", cpu_physical, "/", cpu_total)

    # Pretty tree output for the combined information
    SystemInfo.print(s)


if __name__ == "__main__":
    main()


