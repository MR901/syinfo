"""Basic example: network information and (optional) device discovery."""

from syinfo import NetworkInfo


def main():
    info = NetworkInfo.get_all(search_period=0, search_device_vendor_too=False)
    net = info.get("network_info", {})
    print("Hostname:", net.get("hostname"))
    print("Public IP:", net.get("current_addresses", {}).get("public_ip"))

    # To scan devices (may require sudo):
    # info = NetworkInfo.get_all(search_period=5, search_device_vendor_too=True)


if __name__ == "__main__":
    main()


