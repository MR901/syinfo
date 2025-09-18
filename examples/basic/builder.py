"""Examples: Using the InfoBuilder fluent API."""

import asyncio

from syinfo import InfoBuilder


def example_basic_system():
    system = (InfoBuilder()
              .include_hardware()
              .enable_caching(ttl=300)
              .build())
    data = system.collect()
    print("Summary:", system.summary())
    print("Hostname:", data.get("dev_info", {}).get("static_hostname"))


def example_network_async():
    async def run():
        system = (InfoBuilder()
                  .include_hardware()
                  .include_network(timeout=0, include_vendor_info=False)
                  .build())
        data = await system.collect_async(scope="network")
        print("Network keys:", list(data.get("network_info", {}).keys())[:5])

    asyncio.run(run())


def example_monitor_creation():
    system = (InfoBuilder()
              .include_monitoring(interval=2)
              .build())
    mon = system.create_monitor()
    mon.start(duration=6)
    import time; time.sleep(7)
    results = mon.stop()
    print("Total points:", results.get("total_points"))


def example_logs_and_packages():
    # Logs
    sys_logs = (InfoBuilder()
                .include_logs(limit=3)
                .build())
    logs = sys_logs.analyze_logs()
    print("Log entries (<=3):", len(logs.get("log_entries", [])))

    # Packages
    sys_pkgs = (InfoBuilder()
               .include_packages(name_filter="python")
               .build())
    pkgs = sys_pkgs.analyze_packages()
    print("Packages found:", len(pkgs.get("packages", [])))


if __name__ == "__main__":
    example_basic_system()
    example_network_async()
    example_monitor_creation()
    example_logs_and_packages()


