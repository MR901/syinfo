# !pip install py-cpuinfo
import cpuinfo
import multiprocessing
import os
import platform
import psutil
import sys

from syinfo.device_info import DeviceInfo
from syinfo.network_info import NetworkInfo


class SysInfo:
    """Get the system (hardware+software+network) related information."""

    @staticmethod
    def print(info, return_msg=False):
        """Print system information."""
        _msg = DeviceInfo.print(info, True)
        _msg += "\n\n"
        _msg += NetworkInfo.print(info, True)
        if return_msg:
            return _msg
        else:
            print(_msg)

    @staticmethod
    def get_all(search_period=10, search_device_vendor_too=True):
        """Aggregate all the information related to the device and network."""
        device_info = DeviceInfo.get_all()
        network_info = NetworkInfo.get_all(search_period, search_device_vendor_too)
        device_info["network_info"] = network_info["network_info"]
        return device_info


def print_brief_sys_info():
    """Print system/device configuration."""
    physical_mem = psutil.virtual_memory()
    total_phy_mem = str(round(physical_mem.total / (1024.**3), 2)) + " GB"
    total_phy_avail = str(round(physical_mem.available / (1024.**3), 2)) + " GB"

    swap_mem = psutil.swap_memory()
    total_swp_mem = str(round(swap_mem.total / (1024.**3), 2)) + " GB"
    total_swp_free = str(round(swap_mem.free / (1024.**3), 2)) + " GB"

    _msg  = f"■{'━'*100:100s}■"
    _msg += "\n┃{0}┃".format(" "*43+"\033[1m SYSTEM INFO \033[0m"+" "*44)
    _msg += f"\n■{'─'*100:100s}■"
    _msg += "\n┃  {0:26s}: {1:78s}┃".format("\033[1mMachine Name\033[0m", platform.node())
    _msg += "\n┃  {0:26s}: {1:78s}┃".format("\033[1mOperating System\033[0m", platform.platform())
    _msg += "\n┃  {0:26s}: {1:78s}┃".format("\033[1mPython Version\033[0m", "{0}.{1}.{2}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2]))
    _msg += "\n┃  {0:26s}: {1:78s}┃".format("\033[1mCurrent WD\033[0m", os.getcwd())
    _msg += "\n┃  {0:26s}  {1:78s}┃".format("\033[1mHardware\033[0m", "")
    _msg += "\n┃          {0:26s}  {1:70s}┃".format("\033[1mCPU\033[0m", "")
    _msg += "\n┃                  {0:26s}: {1:62s}┃".format("\033[1mBrand\033[0m", cpuinfo.get_cpu_info()["brand_raw"])
    _msg += "\n┃                  {0:26s}: {1:62s}┃".format("\033[1m# of cores\033[0m", str(multiprocessing.cpu_count()))
    _msg += "\n┃          {0:26s}  {1:70s}┃".format("\033[1mRAM\033[0m", "")
    _msg += "\n┃                  {0:26s}: {1:62s}┃".format("\033[1mTotal\033[0m", total_phy_mem)
    _msg += "\n┃                  {0:26s}: {1:62s}┃".format("\033[1mAvailable\033[0m", total_phy_avail)
    _msg += "\n┃          {0:26s}  {1:70s}┃".format("\033[1mWap Memory\033[0m", "")
    _msg += "\n┃                  {0:26s}: {1:62s}┃".format("\033[1mTotal\033[0m", total_swp_mem)
    _msg += "\n┃                  {0:26s}: {1:62s}┃".format("\033[1mFree\033[0m", total_swp_free)
    _msg += f"\n■{'━'*100:100s}■"
    print(_msg)
