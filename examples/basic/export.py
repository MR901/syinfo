"""Basic example: export information using DeviceInfo/SystemInfo."""

from syinfo import DeviceInfo, SystemInfo


def main():
    # Export device-only info
    print("JSON (device):\n", DeviceInfo.export("json")[:200], "...")
    try:
        print("\nYAML (device):\n", DeviceInfo.export("yaml")[:200], "...")
    except Exception as e:
        print("YAML export not available:", e)

    # Export combined system info (device + network without scanning)
    print("\nJSON (system):\n", SystemInfo.export("json")[:200], "...")


if __name__ == "__main__":
    main()


