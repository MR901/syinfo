"""Basic example: device information using the new public API."""

from syinfo import DeviceInfo


def main():
    # Collect device info
    info = DeviceInfo.get_all()

    # Print a couple of key fields (safe access with fallbacks)
    cpu_design = (info.get("cpu_info", {}) or {}).get("design", {}) or {}
    cpu_model = cpu_design.get("model name") or cpu_design.get("model") or "Unknown"
    mem_total = (
        (info.get("memory_info", {}) or {})
        .get("virtual", {})
        .get("readable", {})
        .get("total", "Unknown")
    )
    print("CPU model:", cpu_model)
    print("RAM total:", mem_total)

    # Pretty tree print (device only)
    DeviceInfo.print(info)


if __name__ == "__main__":
    main()


