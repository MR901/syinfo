"""Basic example: network information and device discovery (optional)."""

import syinfo as si


def main():
    try:
        info = si.get_network_info(scan_devices=False)
        print("Hostname:", info.get("hostname"))
        print("Public IP:", info.get("current_addresses", {}).get("public_ip"))
        # To scan devices (may require privileges / optional extras):
        # info = si.get_network_info(scan_devices=True, scan_timeout=5)
    except Exception as e:
        print("Network features not available:", e)


if __name__ == "__main__":
    main()


