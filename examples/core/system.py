"""Core example: Combined system information (device + network brief)."""

from syinfo import SystemInfo


def main():
    info = SystemInfo.get_all(search_period=0, search_device_vendor_too=False)
    SystemInfo.print(info)


if __name__ == "__main__":
    main()



