"""Core example: Device information."""

from syinfo import DeviceInfo


def main():
    info = DeviceInfo.get_all()
    DeviceInfo.print(info)


if __name__ == "__main__":
    main()



