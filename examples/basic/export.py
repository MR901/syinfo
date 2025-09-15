"""Basic example: export system info in JSON/YAML/CSV."""

import syinfo as si


def main():
    print("JSON:\n", si.export_system_info("json")[:200], "...")
    try:
        print("\nYAML:\n", si.export_system_info("yaml")[:200], "...")
    except Exception as e:
        print("YAML export not available:", e)
    print("\nCSV:\n", si.export_system_info("csv")[:200], "...")


if __name__ == "__main__":
    main()


