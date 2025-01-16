"""Main file

    PURPLE,       CYAN,   DARKCYAN,       BLUE,      GREEN,     YELLOW,        RED,      BOLD,     UNDER,      END =
"\033[95m", "\033[96m", "\033[36m", "\033[94m", "\033[92m", "\033[93m", "\033[91m", "\033[1m", "\033[4m", "\033[0m"
"""

import warnings
warnings.filterwarnings("ignore")

import sys
import json
import argparse
import textwrap
import platform

from syinfo.device_info import DeviceInfo
from syinfo.network_info import NetworkInfo
from syinfo.sys_info import SysInfo
from syinfo._version import __version__


def contact(msg=True):
    """Contact links."""
    _msg  = "\n  --  Email: \033[4m\033[94mmohitrajput901@gmail.com\033[0m"
    _msg += "\n  -- GitHub: \033[4m\033[94mhttps://github.com/MR901/syinfo\033[0m"
    if msg:
        print(_msg)
    return _msg


def main():
    """Main function.

    Return:
        json or print (default)
        device info
        network info
        sys info
    """
    wrapper = textwrap.TextWrapper(width=50)
    description = wrapper.fill(text="SyInfo")

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter, description=description,
        epilog=textwrap.dedent(contact(msg=False))
    )

    parser.add_argument(
        "-c", "--contact", action="store_true", help="show contact"
    )
    parser.add_argument(
        "-v", "--version", action="version", version=__version__, help="show current version"
    )
    parser.add_argument(
        "-d", "--device", action="store_true",
        help= "\033[93m" + "show information about your device." + "\033[0m"
    )
    parser.add_argument(
        "-n", "--network", action="store_true",
        help= "\033[94m" + "show information about your network." + "\033[0m"
    )
    parser.add_argument(
        "-s", "--system", action="store_true",
        help= "\033[92m" + "show combined information about your device and network." + "\033[0m"
    )
    parser.add_argument(
        "-t", "--time", type=int, metavar="", required=False, default=10,
        help="int supplement for `-n` or `-s` command (scanning `-t` seconds)"
    )
    parser.add_argument(
        "-o", "--disable-vendor-search", action="store_false",
        help="supplement for `-n` or `-s` command to stop searching for vendor for the device (mac)"
    )

    parser.add_argument(
        "-p", "--disable-print", action="store_true", help="disable printing of the information."
    )
    parser.add_argument(
        "-j", "--return-json", action="store_true", help="return output as json"
    )
    args = parser.parse_args()

    instance = None
    if args.contact:
        contact(msg=True)
    elif args.device:
        instance = DeviceInfo
        info = instance.get_all()
    elif args.network:
        instance = NetworkInfo
        info = instance.get_all(
            search_period=args.time,
            search_device_vendor_too=args.disable_vendor_search
        )
    elif args.system:
        instance = SysInfo
        info = instance.get_all(
            search_period=args.time,
            search_device_vendor_too=args.disable_vendor_search
        )
    elif len(sys.argv) == 1:
        parser.print_help()
        # help()
    else:
        parser.print_help()
        # help()

    if instance:
        if args.disable_print is False:
            instance.print(info)

        if args.return_json:
            print(json.dumps(info))


if __name__ == "__main__":
    main()
