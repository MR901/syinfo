"""General example: Export device and system info."""

from syinfo import DeviceInfo, SystemInfo


def main() -> None:
    print("Device JSON (first 200 chars):")
    print(DeviceInfo.export("json")[:200], "...")

    print("\nSystem JSON (first 200 chars):")
    print(SystemInfo.export("json")[:200], "...")


if __name__ == "__main__":
    main()



