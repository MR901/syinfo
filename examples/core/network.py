"""Core example: Network information and (optional) device discovery."""

from syinfo import NetworkInfo


def main():
    info = NetworkInfo.get_all(search_period=0, search_device_vendor_too=False)
    NetworkInfo.print(info)


if __name__ == "__main__":
    main()



