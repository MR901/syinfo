"""Package inventory examples using syinfo.analysis.packages."""

from syinfo.analysis.packages import PackageManager, PackageManagerType


def list_all_counts():
    pm = PackageManager()
    packages = pm.list_packages()
    print(f"Total installed (unique by name+manager): {len(packages)}")
    counts = {}
    for p in packages:
        counts[p.manager] = counts.get(p.manager, 0) + 1
    for mgr, cnt in sorted(counts.items()):
        print(f"{mgr}: {cnt}")


def filter_examples():
    pm = PackageManager()
    pip_django = pm.list_packages(manager=PackageManagerType.PIP, name_filter="django")
    print(f"pip django*: {len(pip_django)}")
    apt_python = pm.list_packages(manager=PackageManagerType.APT, name_filter="python")
    print(f"apt python*: {len(apt_python)}")


if __name__ == "__main__":
    print("-- Package Counts --")
    list_all_counts()
    print("\n-- Filters --")
    filter_examples()
