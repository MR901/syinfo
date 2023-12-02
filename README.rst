
sys_info
==========

A python package to get system and network information.


How to install  
--------------  

.. code-block:: shell

	(root_dir) $ pip install .

  
How to use  
----------  
  
.. code-block:: python

	from sys_info.utils import Execute, HumanReadable
	from sys_info.search_network import search_devices_on_network, get_vendor
	from sys_info.device_info import DeviceInfo
	from sys_info.network_info import NetworkInfo
	from sys_info.main import SysInfo

	device_info = SysInfo.get_all()
	print(SysInfo.print(device_info))

	network_info = NetworkInfo.get_all()
	print(NetworkInfo.print(network_info))


.. code-block:: shell

	======================================== System Information ========================================
	.
	├── System Information
	│   ├── Mac Address ........ 3c:e9:f7:5c:60:f7
	│   ├── System Type......... laptop
	│   ├── Static Hostname .... mohit-laptop
	│   ├── Icon Name .......... computer-laptop
	│   ├── Operating Software
	│   │   ├── Full name........... Ubuntu 20.04.6 LTS
	│   │   ├── Distribution........ Ubuntu
	│   │   ├── Platform............ Linux-5.15.0-88-generic-x86_64-with-glibc2.31
	│   │   ├── Version............. 20.04.6 LTS (Focal Fossa)
	│   │   ├── Update history...... #98~20.04.1-Ubuntu SMP Mon Oct 9 16:43:45 UTC 2023
	│   │   ├── Id like............. debian
	│   │   ├── System.............. Linux
	│   │   ├── Kernel.............. Linux 5.15.0-88-generic
	│   │   ├── Architecture........ x86-64
	│   │   ├── Release............. 5.15.0-88-generic
	│   │   ├── Machine id.......... cd0923accbf548b6b12eb388e1acef66
	│   │   └── Boot id............. d0c4a450d68a4a01a898a108563a3ba7
	│   ├── Device Manufacturer
	│   │   ├── bios
	│   │   │   ├── date............ 06/25/2023
	│   │   │   ├── release......... 1.35
	│   │   │   ├── vendor.......... LENOVO
	│   │   │   └── version......... N3BET57W (1.35 )
	│   │   ├── board
	│   │   │   ├── asset_tag....... Not Available
	│   │   │   ├── name............ 21BTS03300
	│   │   │   ├── vendor.......... LENOVO
	│   │   │   └── version......... SDK0T76530 WIN
	│   │   ├── chassis
	│   │   │   ├── asset_tag....... No Asset Tag
	│   │   │   ├── type............ 10
	│   │   │   ├── vendor.......... LENOVO
	│   │   │   └── version......... None
	│   │   ├── ec
	│   │   │   └── firmware_release 1.15
	│   │   ├── modalias........ dmi:bvnLENOVO:bvrN3BET57W(1.35):bd06/25/2023:br1.35:efr1.15:svnLENOVO:pn21BTS03300:pvrThinkPadP16sGen1:rvnLENOVO:rn21BTS03300:rvrSDK0T76530WIN:cvnLENOVO:ct10:cvrNone:skuLENOVO_MT_21BT_BU_Think_FM_ThinkPadP16sGen1:
	│   │   ├── product
	│   │   │   ├── family.......... ThinkPad P16s Gen 1
	│   │   │   ├── name............ 21BTS03300
	│   │   │   ├── sku............. LENOVO_MT_21BT_BU_Think_FM_ThinkPad P16s Gen 1
	│   │   │   └── version......... ThinkPad P16s Gen 1
	│   │   ├── sys
	│   │   │   └── vendor.......... LENOVO
	│   │   └── uevent.......... MODALIAS=dmi:bvnLENOVO:bvrN3BET57W(1.35):bd06/25/2023:br1.35:efr1.15:svnLENOVO:pn21BTS03300:pvrThinkPadP16sGen1:rvnLENOVO:rn21BTS03300:rvrSDK0T76530WIN:cvnLENOVO:ct10:cvrNone:skuLENOVO_MT_21BT_BU_Think_FM_ThinkPadP16sGen1:
	│   └── Py Version ..... 3.11.4
	├── Time
	│   ├── Current Time
	│   │   ├── Timestamp ...... 1701065174.4
	│   │   └── Date/Time ...... 2023/11/27 11:36:14
	│   ├── Boot Time
	│   │   ├── Timestamp ...... 1700744255.0
	│   │   └── Date/Time ...... 2023/11/23 18:27:35
	│   └── Uptime Time
	│       ├── Seconds ........ 320919.4
	│       └── Date/Time ...... 3 day, 17 hr, 8 min, 39 sec, 400.0 ms
	├── CPU
	│   ├── Cores
	│   │   ├── Physical ....... 12
	│   │   └── Total .......... 16
	│   ├── Frequency
	│   │   ├── Min ............ 400.00 Mhz
	│   │   ├── Max ............ 4050.00 Mhz
	│   │   └── Current ........ 2562.49 Mhz
	│   ├── CPU Usage
	│   │   ├── Total........... 7.6 %
	│   │   └── CPU Usage Per Core
	│   │       ├── Core  1 ........ 18.4 %
	│   │       ├── Core  2 ........  3.1 %
	│   │       ├── Core  3 ........  5.2 %
	│   │       ├── Core  4 ........  0.0 %
	│   │       ├── Core  5 ........ 13.0 %
	│   │       ├── Core  6 ........  1.0 %
	│   │       ├── Core  7 ........ 14.3 %
	│   │       ├── Core  8 ........  0.0 %
	│   │       ├── Core  9 ........  9.8 %
	│   │       ├── Core 10 ........ 10.7 %
	│   │       ├── Core 11 ........  5.1 %
	│   │       ├── Core 12 ........  2.0 %
	│   │       ├── Core 13 ........  6.0 %
	│   │       ├── Core 14 ........  5.9 %
	│   │       ├── Core 15 ........  2.0 %
	│   │       └── Core 16 ........  3.1 %
	│   └── CPU Design
	│       ├── processor....... 0 / 1 / 2 / 3 / 4 / 5 / 6 / 7 / 8 / 9 / 10 / 11 / 12 / 13 / 14 / 15
	│       ├── vendor_id....... GenuineIntel
	│       ├── cpu family...... 6
	│       ├── model........... 154
	│       ├── model name...... 12th Gen Intel(R) Core(TM) i7-1260P
	│       ├── stepping........ 3
	│       ├── microcode....... 1072
	│       ├── cpu MHz......... 665.516
	│       ├── cache size...... 18432 KB
	│       ├── physical id..... 0
	│       ├── siblings........ 16
	│       ├── core id......... 0
	│       ├── cpu cores....... 12
	│       ├── apicid.......... 0 / 1 / 8 / 9 / 16 / 17 / 24 / 25 / 32 / 34 / 36 / 38 / 40 / 42 / 44 / 46
	│       ├── initial apicid.. 0 / 1 / 8 / 9 / 16 / 17 / 24 / 25 / 32 / 34 / 36 / 38 / 40 / 42 / 44 / 46
	│       ├── fpu............. True
	│       ├── fpu_exception... True
	│       ├── cpuid level..... 32
	│       ├── wp.............. True
	│       ├── flags........... fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc cpuid aperfmperf tsc_known_freq pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb ssbd ibrs ibpb stibp ibrs_enhanced tpr_shadow vnmi flexpriority ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid rdseed adx smap clflushopt clwb intel_pt sha_ni xsaveopt xsavec xgetbv1 xsaves split_lock_detect avx_vnni dtherm ida arat pln pts hwp hwp_notify hwp_act_window hwp_epp hwp_pkg_req umip pku ospke waitpkg gfni vaes vpclmulqdq rdpid movdiri movdir64b fsrm md_clear serialize arch_lbr flush_l1d arch_capabilities
	│       ├── vmx flags....... vnmi preemption_timer posted_intr invvpid ept_x_only ept_ad ept_1gb flexpriority apicv tsc_offset vtpr mtf vapic ept vpid unrestricted_guest vapic_reg vid ple shadow_vmcs ept_mode_based_exec tsc_scaling usr_wait_pause
	│       ├── bugs............ spectre_v1 spectre_v2 spec_store_bypass swapgs eibrs_pbrsb
	│       ├── bogomips........ 4992.0
	│       ├── clflush size.... 64
	│       ├── cache_alignment. 64
	│       ├── address sizes... 39 bits physical, 48 bits virtual
	│       └── power management None
	├── Memory
	│   ├── Virtual
	│   │   ├── Used ........... 9.2 GB
	│   │   ├── Free ........... 20.3 GB
	│   │   ├── Total .......... 31.0 GB
	│   │   └── Percentage ..... 34.7 %
	│   ├── Swap
	│   │   ├── Used ........... 12.5 MB
	│   │   ├── Free ........... 2.0 GB
	│   │   ├── Total .......... 2.0 GB
	│   │   └── Percentage ..... 0.6 %
	│   └── Design
	│       ├── VmallocTotal
	│       │   ├── bytes........... 35184372087808
	│       │   └── human_readable.. 32.0 TB
	│       ├── Committed_AS
	│       │   ├── bytes........... 34392129536
	│       │   └── human_readable.. 32.0 GB
	│       ├── MemTotal
	│       │   ├── bytes........... 33334595584
	│       │   └── human_readable.. 31.0 GB
	│       ├── MemAvailable
	│       │   ├── bytes........... 21756289024
	│       │   └── human_readable.. 20.3 GB
	│       ├── CommitLimit
	│       │   ├── bytes........... 18814775296
	│       │   └── human_readable.. 17.5 GB
	│       ├── DirectMap2M
	│       │   ├── bytes........... 18171822080
	│       │   └── human_readable.. 16.9 GB
	│       ├── DirectMap1G
	│       │   ├── bytes........... 16106127360
	│       │   └── human_readable.. 15.0 GB
	│       ├── Inactive
	│       │   ├── bytes........... 15047880704
	│       │   └── human_readable.. 14.0 GB
	│       ├── Cached
	│       │   ├── bytes........... 12124954624
	│       │   └── human_readable.. 11.3 GB
	│       ├── MemFree
	│       │   ├── bytes........... 9801596928
	│       │   └── human_readable.. 9.1 GB
	│       ├── Inactive(anon)
	│       │   ├── bytes........... 9738534912
	│       │   └── human_readable.. 9.1 GB
	│       ├── AnonPages
	│       │   ├── bytes........... 9149292544
	│       │   └── human_readable.. 8.5 GB
	│       ├── Active
	│       │   ├── bytes........... 6410309632
	│       │   └── human_readable.. 6.0 GB
	│       ├── Active(file)
	│       │   ├── bytes........... 6236733440
	│       │   └── human_readable.. 5.8 GB
	│       ├── Inactive(file)
	│       │   ├── bytes........... 5309345792
	│       │   └── human_readable.. 4.9 GB
	│       ├── SwapTotal
	│       │   ├── bytes........... 2147479552
	│       │   └── human_readable.. 2.0 GB
	│       ├── SwapFree
	│       │   ├── bytes........... 2134372352
	│       │   └── human_readable.. 2.0 GB
	│       ├── Shmem
	│       │   ├── bytes........... 1238302720
	│       │   └── human_readable.. 1.2 GB
	│       ├── Slab
	│       │   ├── bytes........... 1221406720
	│       │   └── human_readable.. 1.1 GB
	│       ├── Mapped
	│       │   ├── bytes........... 1102733312
	│       │   └── human_readable.. 1.0 GB
	│       ├── KReclaimable
	│       │   ├── bytes........... 886018048
	│       │   └── human_readable.. 845.0 MB
	│       ├── SReclaimable
	│       │   ├── bytes........... 886018048
	│       │   └── human_readable.. 845.0 MB
	│       ├── DirectMap4k
	│       │   ├── bytes........... 839122944
	│       │   └── human_readable.. 800.2 MB
	│       ├── Buffers
	│       │   ├── bytes........... 657612800
	│       │   └── human_readable.. 627.1 MB
	│       ├── Unevictable
	│       │   ├── bytes........... 473690112
	│       │   └── human_readable.. 451.7 MB
	│       ├── SUnreclaim
	│       │   ├── bytes........... 335388672
	│       │   └── human_readable.. 319.9 MB
	│       ├── Active(anon)
	│       │   ├── bytes........... 173576192
	│       │   └── human_readable.. 165.5 MB
	│       ├── PageTables
	│       │   ├── bytes........... 105754624
	│       │   └── human_readable.. 100.9 MB
	│       ├── VmallocUsed
	│       │   ├── bytes........... 86339584
	│       │   └── human_readable.. 82.3 MB
	│       ├── KernelStack
	│       │   ├── bytes........... 36241408
	│       │   └── human_readable.. 34.6 MB
	│       ├── Percpu
	│       │   ├── bytes........... 20381696
	│       │   └── human_readable.. 19.4 MB
	│       ├── Hugepagesize
	│       │   ├── bytes........... 2097152
	│       │   └── human_readable.. 2.0 MB
	│       ├── SwapCached
	│       │   ├── bytes........... 258048
	│       │   └── human_readable.. 252.0 KB
	│       ├── Mlocked
	│       │   ├── bytes........... 49152
	│       │   └── human_readable.. 48.0 KB
	│       ├── Dirty
	│       │   ├── bytes........... 0
	│       │   └── human_readable.. 0.0 B
	│       ├── Writeback
	│       │   ├── bytes........... 0
	│       │   └── human_readable.. 0.0 B
	│       ├── NFS_Unstable
	│       │   ├── bytes........... 0
	│       │   └── human_readable.. 0.0 B
	│       ├── Bounce
	│       │   ├── bytes........... 0
	│       │   └── human_readable.. 0.0 B
	│       ├── WritebackTmp
	│       │   ├── bytes........... 0
	│       │   └── human_readable.. 0.0 B
	│       ├── VmallocChunk
	│       │   ├── bytes........... 0
	│       │   └── human_readable.. 0.0 B
	│       ├── HardwareCorrupted
	│       │   ├── bytes........... 0
	│       │   └── human_readable.. 0.0 B
	│       ├── AnonHugePages
	│       │   ├── bytes........... 0
	│       │   └── human_readable.. 0.0 B
	│       ├── ShmemHugePages
	│       │   ├── bytes........... 0
	│       │   └── human_readable.. 0.0 B
	│       ├── ShmemPmdMapped
	│       │   ├── bytes........... 0
	│       │   └── human_readable.. 0.0 B
	│       ├── FileHugePages
	│       │   ├── bytes........... 0
	│       │   └── human_readable.. 0.0 B
	│       ├── FilePmdMapped
	│       │   ├── bytes........... 0
	│       │   └── human_readable.. 0.0 B
	│       ├── HugePages_Total
	│       │   ├── bytes........... 0
	│       │   └── human_readable.. 0.0 B
	│       ├── HugePages_Free
	│       │   ├── bytes........... 0
	│       │   └── human_readable.. 0.0 B
	│       ├── HugePages_Rsvd
	│       │   ├── bytes........... 0
	│       │   └── human_readable.. 0.0 B
	│       ├── HugePages_Surp
	│       │   ├── bytes........... 0
	│       │   └── human_readable.. 0.0 B
	│       └── Hugetlb
	│           ├── bytes........... 0
	│           └── human_readable.. 0.0 B
	├── Disk
	│   ├── Since Boot
	│   │   ├── Total Read ..... 10.5 GB
	│   │   └── Total Write .... 43.8 GB
	│   └── Drives
	│       ├── /dev/nvme0n1p5
	│       │   ├── Mountpoint ..... /
	│       │   ├── File System .... ext4
	│       │   └── Space
	│       │       ├── Used .......... 491.9 GB
	│       │       ├── Free .......... 82.3 GB
	│       │       ├── Total ......... 605.0 GB
	│       │       └── Percent ....... 85.7 %
	│       ├── /dev/loop0
	│       │   ├── Mountpoint ..... /snap/bare/5
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 128.0 KB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 128.0 KB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop1
	│       │   ├── Mountpoint ..... /snap/code/146
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 303.4 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 303.4 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop2
	│       │   ├── Mountpoint ..... /snap/bitwarden/100
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 86.2 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 86.2 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop3
	│       │   ├── Mountpoint ..... /snap/code/145
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 303.4 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 303.4 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop4
	│       │   ├── Mountpoint ..... /snap/bitwarden/99
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 86.2 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 86.2 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop5
	│       │   ├── Mountpoint ..... /snap/core18/2796
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 55.8 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 55.8 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop6
	│       │   ├── Mountpoint ..... /snap/core20/2015
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 63.5 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 63.5 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop7
	│       │   ├── Mountpoint ..... /snap/core18/2790
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 55.8 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 55.8 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop9
	│       │   ├── Mountpoint ..... /snap/core20/1974
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 63.5 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 63.5 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop13
	│       │   ├── Mountpoint ..... /snap/vlc/3721
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 321.1 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 321.1 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop26
	│       │   ├── Mountpoint ..... /snap/snapd/20092
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 40.9 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 40.9 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop12
	│       │   ├── Mountpoint ..... /snap/xdman/60
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 43.5 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 43.5 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop16
	│       │   ├── Mountpoint ..... /snap/snap-store/959
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 12.4 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 12.4 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop32
	│       │   ├── Mountpoint ..... /snap/gnome-3-34-1804/93
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 218.5 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 218.5 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop29
	│       │   ├── Mountpoint ..... /snap/slack/113
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 117.2 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 117.2 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop28
	│       │   ├── Mountpoint ..... /snap/slack/110
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 117.5 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 117.5 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop11
	│       │   ├── Mountpoint ..... /snap/gnome-3-28-1804/198
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 164.9 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 164.9 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop14
	│       │   ├── Mountpoint ..... /snap/drawio/192
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 138.0 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 138.0 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop10
	│       │   ├── Mountpoint ..... /snap/core22/864
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 74.0 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 74.0 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop18
	│       │   ├── Mountpoint ..... /snap/sublime-text/122
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 64.0 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 64.0 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop31
	│       │   ├── Mountpoint ..... /snap/drawio/191
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 137.9 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 137.9 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop27
	│       │   ├── Mountpoint ..... /snap/gnome-3-38-2004/119
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 346.4 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 346.4 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop25
	│       │   ├── Mountpoint ..... /snap/gtk-common-themes/1535
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 91.8 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 91.8 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop17
	│       │   ├── Mountpoint ..... /snap/rpi-imager/465
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 205.0 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 205.0 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop23
	│       │   ├── Mountpoint ..... /snap/rpi-imager/520
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 205.0 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 205.0 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop19
	│       │   ├── Mountpoint ..... /snap/node/7823
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 31.6 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 31.6 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop30
	│       │   ├── Mountpoint ..... /snap/snapd/20290
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 40.9 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 40.9 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop8
	│       │   ├── Mountpoint ..... /snap/core22/858
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 73.9 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 73.9 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop34
	│       │   ├── Mountpoint ..... /snap/node/7707
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 31.6 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 31.6 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop36
	│       │   ├── Mountpoint ..... /snap/xdman/56
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 43.5 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 43.5 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop15
	│       │   ├── Mountpoint ..... /snap/gnome-42-2204/141
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 497.0 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 497.0 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop24
	│       │   ├── Mountpoint ..... /snap/postman/234
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 167.1 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 167.1 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop20
	│       │   ├── Mountpoint ..... /snap/snap-store/638
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 46.0 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 46.0 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop21
	│       │   ├── Mountpoint ..... /snap/postman/231
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 167.1 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 167.1 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop37
	│       │   ├── Mountpoint ..... /snap/gnome-42-2204/132
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 497.0 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 497.0 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop35
	│       │   ├── Mountpoint ..... /snap/vlc/3078
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 320.5 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 320.5 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/loop33
	│       │   ├── Mountpoint ..... /snap/gnome-3-38-2004/143
	│       │   ├── File System .... squashfs
	│       │   └── Space
	│       │       ├── Used .......... 349.8 MB
	│       │       ├── Free .......... 0.0 B
	│       │       ├── Total ......... 349.8 MB
	│       │       └── Percent ....... 100.0 %
	│       ├── /dev/nvme0n1p1
	│       │   ├── Mountpoint ..... /boot/efi
	│       │   ├── File System .... vfat
	│       │   └── Space
	│       │       ├── Used .......... 62.0 MB
	│       │       ├── Free .......... 194.0 MB
	│       │       ├── Total ......... 256.0 MB
	│       │       └── Percent ....... 24.2 %
	│       └── /dev/loop38
	│           ├── Mountpoint ..... /snap/sublime-text/134
	│           ├── File System .... squashfs
	│           └── Space
	│               ├── Used .......... 64.0 MB
	│               ├── Free .......... 0.0 B
	│               ├── Total ......... 64.0 MB
	│               └── Percent ....... 100.0 %
	======================================== GPU Details ========================================
	No GPU Detected
	None


.. code-block:: shell

	└── Network Information
	    ├── Hostname........ mohit-laptop
	    ├── Mac Address..... 3c:e9:f7:5c:60:f7
	    ├── Internet Available True
	    ├── Data transfer since boot
	    │   ├── Sent
	    │   │   ├── Data (Bytes) ... 1789279003
	    │   │   └── Data ........... 1.7 GB
	    │   └── Received
	    │       ├── Data (Bytes) ... 9705240447
	    │       └── Data ........... 9.0 GB
	    ├── Physical & Virtual Interfaces
	    │   ├── Brief
	    │   │   ├── lo
	    │   │   │   ├── ip_address...... 127.0.0.1
	    │   │   │   ├── nwtmask......... None
	    │   │   │   ├── broadcast_ip.... None
	    │   │   │   ├── mac_address..... 00:00:00:00:00:00
	    │   │   │   └── broadcast_mac... None
	    │   │   ├── wlp0s20f3
	    │   │   │   ├── ip_address...... 192.168.1.45
	    │   │   │   ├── nwtmask......... None
	    │   │   │   ├── broadcast_ip.... 192.168.1.255
	    │   │   │   ├── mac_address..... 3c:e9:f7:5c:60:f7
	    │   │   │   └── broadcast_mac... ff:ff:ff:ff:ff:ff
	    │   │   └── enp0s31f6
	    │   │       ├── mac_address..... 9c:2d:cd:7f:99:e8
	    │   │       ├── nwtmask......... None
	    │   │       └── broadcast_mac... ff:ff:ff:ff:ff:ff
	    │   └── Detailed
	    │       ├──  0 ──┐
	    │       │        ├── general
	    │       │        │   ├── device.......... wlp0s20f3
	    │       │        │   ├── type............ wifi
	    │       │        │   ├── hwaddr.......... 3C:E9:F7:5C:60:F7
	    │       │        │   ├── mtu............. 1500
	    │       │        │   ├── state........... 100 (connected)
	    │       │        │   ├── connection...... RR-Sumit_2G
	    │       │        │   └── con-path........ /org/freedesktop/NetworkManager/ActiveConnection/15
	    │       │        ├── ip4
	    │       │        │   ├── address[1]...... 192.168.1.45/24
	    │       │        │   ├── gateway......... 192.168.1.1
	    │       │        │   ├── route[1]........ dst = 0.0.0.0/0, nh = 192.168.1.1, mt = 600
	    │       │        │   ├── route[2]........ dst = 192.168.1.0/24, nh = 0.0.0.0, mt = 600
	    │       │        │   ├── route[3]........ dst = 169.254.0.0/16, nh = 0.0.0.0, mt = 1000
	    │       │        │   ├── dns[1].......... 205.254.184.15
	    │       │        │   ├── dns[2].......... 103.56.228.140
	    │       │        │   └── domain[1]....... hgu_lan
	    │       │        └── ip6
	    │       │            ├── address[1]...... fe80::4d74:9fc2:4b6f:fcd3/64
	    │       │            ├── gateway......... --
	    │       │            └── route[1]........ dst = fe80::/64, nh = ::, mt = 600
	    │       ├──  1 ──┐
	    │       │        └── general
	    │       │            ├── device.......... p2p-dev-wlp0s20f3
	    │       │            ├── type............ wifi-p2p
	    │       │            ├── hwaddr.......... (unknown)
	    │       │            ├── mtu............. 0
	    │       │            ├── state........... 30 (disconnected)
	    │       │            ├── connection...... --
	    │       │            └── con-path........ --
	    │       ├──  2 ──┐
	    │       │        ├── general
	    │       │        │   ├── device.......... enp0s31f6
	    │       │        │   ├── type............ ethernet
	    │       │        │   ├── hwaddr.......... 9C:2D:CD:7F:99:E8
	    │       │        │   ├── mtu............. 1500
	    │       │        │   ├── state........... 20 (unavailable)
	    │       │        │   ├── connection...... --
	    │       │        │   └── con-path........ --
	    │       │        └── wired-properties
	    │       │            └── carrier......... False
	    │       └──  3 ──┐
	    │                ├── general
	    │                │   ├── device.......... lo
	    │                │   ├── type............ loopback
	    │                │   ├── hwaddr.......... 00:00:00:00:00:00
	    │                │   ├── mtu............. 65536
	    │                │   ├── state........... 10 (unmanaged)
	    │                │   ├── connection...... --
	    │                │   └── con-path........ --
	    │                ├── ip4
	    │                │   ├── address[1]...... 127.0.0.1/8
	    │                │   └── gateway......... --
	    │                └── ip6
	    │                    ├── address[1]...... ::1/128
	    │                    ├── gateway......... --
	    │                    └── route[1]........ dst = ::1/128, nh = ::, mt = 256
	    ├── Wifi Connection
	    │   ├── Wifi name....... RR-Sumit_2G
	    │   ├── Password........ 8120002045
	    │   ├── Security........ sudo needed
	    │   ├── Interface....... wlp0s20f3
	    │   ├── Frequency....... 2.447 GHz
	    │   ├── Channel......... 8
	    │   ├── Signal strength. -43 DBm
	    │   ├── Signal quality.. [6/7] excellent signal
	    │   └── Options
	    │       ├──  0 ──┐
	    │       │        ├── Network......... www.excitel.com
	    │       │        ├── Mode............ Infra
	    │       │        ├── Channel......... 8
	    │       │        ├── Rate............ 130 Mbit/s
	    │       │        ├── Signal.......... 97
	    │       │        ├── Bars............ ▂▄▆█
	    │       │        ├── Security........ WPA1 WPA2
	    │       │        ├── In-use.......... True
	    │       │        └── Mac............. B4:F9:49:48:5A:D8
	    │       ├──  1 ──┐
	    │       │        ├── Network......... RR-Sumit_2G
	    │       │        ├── Mode............ Infra
	    │       │        ├── Channel......... 8
	    │       │        ├── Rate............ 130 Mbit/s
	    │       │        ├── Signal.......... 77
	    │       │        ├── Bars............ ▂▄▆_
	    │       │        ├── Security........ WPA1 WPA2
	    │       │        ├── In-use.......... True
	    │       │        └── Mac............. B4:F9:49:48:5A:D5
	    │       ├──  2 ──┐
	    │       │        ├── Network......... RR-Sumit_5G
	    │       │        ├── Mode............ Infra
	    │       │        ├── Channel......... 149
	    │       │        ├── Rate............ 270 Mbit/s
	    │       │        ├── Signal.......... 77
	    │       │        ├── Bars............ ▂▄▆_
	    │       │        ├── Security........ WPA1 WPA2
	    │       │        ├── In-use.......... True
	    │       │        └── Mac............. B4:F9:49:48:5A:D1
	    │       ├──  3 ──┐
	    │       │        ├── Network......... Atharav-4G
	    │       │        ├── Mode............ Infra
	    │       │        ├── Channel......... 1
	    │       │        ├── Rate............ 130 Mbit/s
	    │       │        ├── Signal.......... 64
	    │       │        ├── Bars............ ▂▄▆_
	    │       │        ├── Security........ WPA1 WPA2
	    │       │        ├── In-use.......... True
	    │       │        └── Mac............. B4:F9:49:70:B5:55
	    │       ├──  4 ──┐
	    │       │        ├── Network......... www.excitel.com
	    │       │        ├── Mode............ Infra
	    │       │        ├── Channel......... 1
	    │       │        ├── Rate............ 130 Mbit/s
	    │       │        ├── Signal.......... 62
	    │       │        ├── Bars............ ▂▄▆_
	    │       │        ├── Security........ WPA1 WPA2
	    │       │        ├── In-use.......... True
	    │       │        └── Mac............. B4:F9:49:70:B5:58
	    │       ├──  5 ──┐
	    │       │        ├── Network......... Kanswal-4G
	    │       │        ├── Mode............ Infra
	    │       │        ├── Channel......... 8
	    │       │        ├── Rate............ 130 Mbit/s
	    │       │        ├── Signal.......... 45
	    │       │        ├── Bars............ ▂▄__
	    │       │        ├── Security........ WPA1 WPA2
	    │       │        ├── In-use.......... True
	    │       │        └── Mac............. 54:47:E8:0C:76:85
	    │       ├──  6 ──┐
	    │       │        ├── Network......... www.excitel.com
	    │       │        ├── Mode............ Infra
	    │       │        ├── Channel......... 8
	    │       │        ├── Rate............ 130 Mbit/s
	    │       │        ├── Signal.......... 45
	    │       │        ├── Bars............ ▂▄__
	    │       │        ├── Security........ WPA1 WPA2
	    │       │        ├── In-use.......... True
	    │       │        └── Mac............. 54:47:E8:0C:76:88
	    │       ├──  7 ──┐
	    │       │        ├── Network......... Atharav-5G
	    │       │        ├── Mode............ Infra
	    │       │        ├── Channel......... 157
	    │       │        ├── Rate............ 270 Mbit/s
	    │       │        ├── Signal.......... 45
	    │       │        ├── Bars............ ▂▄__
	    │       │        ├── Security........ WPA1 WPA2
	    │       │        ├── In-use.......... True
	    │       │        └── Mac............. B4:F9:49:70:B5:51
	    │       ├──  8 ──┐
	    │       │        ├── Network......... Sunilreetu_4G
	    │       │        ├── Mode............ Infra
	    │       │        ├── Channel......... 11
	    │       │        ├── Rate............ 270 Mbit/s
	    │       │        ├── Signal.......... 29
	    │       │        ├── Bars............ ▂___
	    │       │        ├── Security........ WPA1
	    │       │        ├── In-use.......... True
	    │       │        └── Mac............. 64:FB:92:47:2A:4E
	    │       ├──  9 ──┐
	    │       │        ├── Network......... www.excitel.com
	    │       │        ├── Mode............ Infra
	    │       │        ├── Channel......... 11
	    │       │        ├── Rate............ 270 Mbit/s
	    │       │        ├── Signal.......... 25
	    │       │        ├── Bars............ ▂___
	    │       │        ├── Security........ WPA1
	    │       │        ├── In-use.......... True
	    │       │        └── Mac............. 66:FB:92:57:2A:4E
	    │       └── 10 ──┐
	    │                ├── Network......... S.V BroaDBanD
	    │                ├── Mode............ Infra
	    │                ├── Channel......... 6
	    │                ├── Rate............ 270 Mbit/s
	    │                ├── Signal.......... 14
	    │                ├── Bars............ ▂___
	    │                ├── Security........ WPA1 WPA2
	    │                ├── In-use.......... True
	    │                └── Mac............. 04:95:E6:EA:6D:D8
	    ├── Devices Available on Network
	    │   ├── 192.168.1.45
	    │   │   ├── mac_address..... 3c:e9:f7:5c:60:f7
	    │   │   ├── device_name..... LENOVO_MT_21BT_BU_Think_FM_ThinkPad P16s Gen 1
	    │   │   ├── identifier...... current device
	    │   │   └── vendor.......... Intel Corporate
	    │   ├── 192.168.1.1
	    │   │   ├── mac_address..... b4:f9:49:48:5a:d0
	    │   │   ├── identifier...... router
	    │   │   └── device_vendor... optilink networks pvt ltd
	    │   ├── 192.168.1.34
	    │   │   ├── mac_address..... 00:31:92:df:40:69
	    │   │   ├── identifier...... unknown
	    │   │   └── device_vendor... TP-Link Corporation Limited
	    │   ├── 192.168.1.33
	    │   │   ├── mac_address..... 10:27:f5:af:0a:4b
	    │   │   ├── identifier...... unknown
	    │   │   └── device_vendor... TP-Link Corporation Limited
	    │   └── 192.168.1.41
	    │       ├── mac_address..... 72:68:cc:84:d7:1f
	    │       ├── identifier...... unknown
	    │       └── device_vendor... unknown
	    ├── Current Addresses
	    │   ├── Isp............. Excitel Broadband Private Limited
	    │   ├── Public ip....... 120.88.35.4
	    │   ├── Ip address host. 127.0.1.1
	    │   ├── Ip address...... 192.168.1.45
	    │   ├── Gateway......... 192.168.1.1
	    │   ├── Dns 1........... 205.254.184.15
	    │   └── Dns 2........... 103.56.228.140
	    └── Demographic Information
	        ├── Country......... India
	        ├── City............ Delhi
	        ├── Region.......... National Capital Territory of Delhi
	        ├── Latitude........ 28.6542
	        ├── Longitude....... 77.2373
	        ├── Zip code........ 110001
	        ├── Maps............ https://www.google.com/maps/search/?api=1&query=28.6542,77.2373
	        └── Meta
	            ├── country_code.... IN
	            ├── region_code..... DL
	            ├── countryCapital.. New Delhi
	            ├── time_zone....... Asia/Kolkata
	            ├── callingCode..... 91
	            ├── currency........ INR
	            ├── currencySymbol.. ₹
	            ├── emojiFlag....... 🇮🇳
	            ├── flagUrl......... https://ip-api.io/images/flags/in.svg
	            ├── public_ip....... 120.88.35.4
	            ├── is_in_european_union False
	            ├── metro_code...... 0
	            └── suspiciousFactors {'isProxy': False, 'isSpam': False, 'isSuspicious': False, 'isTorNode': False}




Create Documentation
--------------------  

from pyfiglet import Figlet
f = Figlet(font='slant')
print(f.renderText('text to render'))
