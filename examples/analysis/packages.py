"""Analysis example: Minimal packages inventory demo."""

from syinfo.analysis.packages import PackageManager, PackageManagerType


def main() -> None:
    pm = PackageManager()
    # Show first few from all managers
    packages = pm.list_packages(as_dict=False)
    print(f"Total packages detected: {len(packages)}")
    for pkg in packages[:5]:
        print(f"{pkg.manager:6} | {pkg.name:30} | {pkg.version or 'N/A'}")

    # Filter example (pip python*)
    pip_python = pm.list_packages(manager=PackageManagerType.PIP, name_filter="python", as_dict=False)
    print(f"\nPIP packages matching 'python': {len(pip_python)}")
    for pkg in pip_python[:5]:
        print(f"pip    | {pkg.name:30} | {pkg.version or 'N/A'}")


if __name__ == "__main__":
    main()



