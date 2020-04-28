## Full tbot log

This log is from starting tbot [testcase](https://github.com/EmbLux-Kft/tbot-tbot2go/blob/wandboard-devel-messe/tc/wandboard/tc_wandboard.py#L208)

Tasks:
- checkout current mainline U-Boot source
- configure the toolchain
- configure U-Boot for the wandboard
- compile U-Boot
- copy the resulting files to the lab hosts tftp directory
- install the images on the wandboard
- checks if the new versions boot
- test.py from U-Boot to test the installed U-Boot
- after all, report the results to our Testserver.

```bash
hs@lab-1:tbot-tbot2go  [wandboard-devel-messe] $ tbot @argswandboardlab1 wandboard_ub_build_install_test
tbot starting ...
├─Flags:
│ 'lab-1-build'
├─Calling wandboard_ub_build_install_test ...
│   ├─Calling wandboard_ub_build ...
│   │   ├─[local] ssh -o BatchMode=yes -i /home/hs/.ssh/id_rsa -p 22 hs@192.168.1.109
│   │   ├─[lab1] systemctl is-active nfs-server.service --no-pager
│   │   │    ## active
│   │   ├─[lab1] systemctl is-active tftp.socket --no-pager
│   │   │    ## active
│   │   ├─Calling uboot_build ...
│   │   │   ├─[local] ssh -o BatchMode=yes -i /home/hs/.ssh/id_rsa -p 22 hs@192.168.1.109
│   │   │   ├─Calling uboot_checkout ...
│   │   │   │   ├─Builder: wandboard-builder
│   │   │   │   ├─[lab1] mkdir -p /work/hs/tbot-workdir
│   │   │   │   ├─[lab1] test -d /work/hs/tbot-workdir/uboot-wandboard-builder/.git
│   │   │   │   ├─[lab1] git -C /work/hs/tbot-workdir/uboot-wandboard-builder fetch
│   │   │   │   ├─[lab1] git -C /work/hs/tbot-workdir/uboot-wandboard-builder rev-parse 'master@{u}'
│   │   │   │   │    ## d16d37bcd4087b8ea0f66cb76a73edad182d151a
│   │   │   │   ├─[lab1] git -C /work/hs/tbot-workdir/uboot-wandboard-builder reset --hard 'master@{u}'
│   │   │   │   │    ## HEAD ist jetzt bei d16d37bcd4 Merge tag 'video-for-v2020.07-rc1' of https://gitlab.denx.de/u-boot/custodians/u-boot-video
│   │   │   │   ├─[lab1] git -C /work/hs/tbot-workdir/uboot-wandboard-builder clean -fdx
│   │   │   │   │    ## Lösche .SPL.cmd
│   │   │   │   │    ## Lösche .config
│   │   │   │   │    ## Lösche .config.old
│   │   │   │   │    ## Lösche .fit-dtb.blob.cmd
│   │   │   │   │    ## Lösche .u-boot-dtb.img.cmd
│   │   │   │   │    ## Lösche .u-boot-fit-dtb.bin.cmd
│   │   │   │   │    ## Lösche .u-boot-nodtb.bin.cmd
│   │   │   │   │    ## Lösche .u-boot-with-spl.imx.cmd
│   │   │   │   │    ## Lösche .u-boot.bin.cmd
│   │   │   │   │    ## Lösche .u-boot.cmd
│   │   │   │   │    ## Lösche .u-boot.img.cmd
│   │   │   │   │    ## Lösche .u-boot.lds.cmd
│   │   │   │   │    ## Lösche .u-boot.srec.cmd
│   │   │   │   │    ## Lösche .u-boot.sym.cmd
│   │   │   │   │    ## Lösche .u-boot.uim.cmd
│   │   │   │   │    ## Lösche SPL
[...]
│   │   │   │   │    ## Lösche u-boot.cfg
│   │   │   │   │    ## Lösche u-boot.cfg.configs
│   │   │   │   │    ## Lösche u-boot.dtb
│   │   │   │   │    ## Lösche u-boot.img
│   │   │   │   │    ## Lösche u-boot.lds
│   │   │   │   │    ## Lösche u-boot.map
│   │   │   │   │    ## Lösche u-boot.srec
│   │   │   │   │    ## Lösche u-boot.sym
│   │   │   │   │    ## Lösche u-boot.uim
│   │   │   │   ├─[lab1] git -C /work/hs/tbot-workdir/uboot-wandboard-builder checkout master
│   │   │   │   │    ## Bereits auf 'master'
│   │   │   │   │    ## Ihr Branch ist auf demselben Stand wie 'origin/master'.
│   │   │   │   ├─[lab1] git -C /work/hs/tbot-workdir/uboot-wandboard-builder rev-parse HEAD
│   │   │   │   │    ## d16d37bcd4087b8ea0f66cb76a73edad182d151a
│   │   │   │   └─Done. (1.444s)
│   │   │   ├─[lab1] bash --norc --noprofile
│   │   │   ├─[lab1] test -e /work/hs/tbot-workdir/toolchain
│   │   │   ├─[lab1] cd /work/hs/tbot-workdir/toolchain
│   │   │   ├─[lab1] pwd
│   │   │   │    ## /work/hs/tbot-workdir/toolchain
│   │   │   ├─[lab1] test -d /work/hs/tbot-workdir/toolchain/gcc-linaro-7.3.1-2018.05-x86_64_arm-linux-gnueabi/bin
│   │   │   ├─[lab1] printenv PATH | grep --color=never /work/hs/tbot-workdir/toolchain/gcc-linaro-7.3.1-2018.05-x86_64_arm-linux-gnueabi/bin
│   │   │   ├─Add toolchain to PATH /work/hs/tbot-workdir/toolchain/gcc-linaro-7.3.1-2018.05-x86_64_arm-linux-gnueabi/bin
│   │   │   ├─[lab1] export PATH=/work/hs/tbot-workdir/toolchain/gcc-linaro-7.3.1-2018.05-x86_64_arm-linux-gnueabi/bin:$PATH
│   │   │   ├─[lab1] printenv PATH
│   │   │   │    ## /work/hs/tbot-workdir/toolchain/gcc-linaro-7.3.1-2018.05-x86_64_arm-linux-gnueabi/bin:/home/hs/.local/bin:/home/hs/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
│   │   │   ├─[lab1] export ARCH=arm
│   │   │   ├─[lab1] export CROSS_COMPILE=arm-linux-gnueabi-
│   │   │   ├─[lab1] printenv ARCH
│   │   │   │    ## arm
│   │   │   ├─[lab1] printenv CROSS_COMPILE
│   │   │   │    ## arm-linux-gnueabi-
│   │   │   ├─[lab1] cd /work/hs/tbot-workdir/uboot-wandboard-builder
│   │   │   ├─Cleaning previous build ...
│   │   │   ├─[lab1] make mrproper
│   │   │   ├─[lab1] test -e /work/hs/tbot-workdir/uboot-wandboard-builder/.config
│   │   │   ├─Configuring build ...
│   │   │   ├─[lab1] make wandboard_defconfig
│   │   │   │    ##   HOSTCC  scripts/basic/fixdep
│   │   │   │    ##   HOSTCC  scripts/kconfig/conf.o
│   │   │   │    ##   YACC    scripts/kconfig/zconf.tab.c
│   │   │   │    ##   LEX     scripts/kconfig/zconf.lex.c
│   │   │   │    ##   HOSTCC  scripts/kconfig/zconf.tab.o
│   │   │   │    ##   HOSTLD  scripts/kconfig/conf
│   │   │   │    ## #
│   │   │   │    ## # configuration written to .config
│   │   │   │    ## #
│   │   │   ├─Patching U-Boot config ...
│   │   │   ├─Calling kconfig_set_value ...
│   │   │   │   ├─Setting CONFIG_LOCALVERSION to "-tbot" ...
│   │   │   │   ├─[lab1] sed -i '/^\(# \)\?CONFIG_LOCALVERSION\(=".*"\| is not set\)$/cCONFIG_LOCALVERSION="-tbot"' /work/hs/tbot-workdir/uboot-wandboard-builder/.config
│   │   │   │   └─Done. (0.006s)
│   │   │   ├─Calling uboot_make ...
│   │   │   │   ├─[lab1] nproc --all
│   │   │   │   │    ## 4
│   │   │   │   ├─[lab1] make -j 4 all
│   │   │   │   │    ## scripts/kconfig/conf  --syncconfig Kconfig
│   │   │   │   │    ##   UPD     include/config.h
│   │   │   │   │    ##   CFG     u-boot.cfg
│   │   │   │   │    ##   GEN     include/autoconf.mk.dep
│   │   │   │   │    ##   CFG     spl/u-boot.cfg
│   │   │   │   │    ##   GEN     spl/include/autoconf.mk
[...]
│   │   │   │   │    ##   LD      spl/u-boot-spl
│   │   │   │   │    ##   OBJCOPY spl/u-boot-spl-nodtb.bin
│   │   │   │   │    ##   COPY    spl/u-boot-spl.bin
│   │   │   │   │    ##   CFGS    spl/u-boot-spl.cfgout
│   │   │   │   │    ##   MKIMAGE SPL
│   │   │   │   │    ##   MKIMAGE u-boot.uim
│   │   │   │   │    ##   MKIMAGE SPL
│   │   │   │   │    ##   CAT     u-boot-with-spl.imx
│   │   │   │   │    ##   CFGCHK  u-boot.cfg
│   │   │   │   ├─[lab1] grep CONFIG_SYS_ARCH u-boot.cfg
│   │   │   │   │    ## #define CONFIG_SYS_ARCH "arm"
│   │   │   │   ├─[lab1] grep CONFIG_SYS_SOC u-boot.cfg
│   │   │   │   │    ## #define CONFIG_SYS_SOC "mx6"
│   │   │   │   ├─[lab1] grep CONFIG_SYS_CPU u-boot.cfg
│   │   │   │   │    ## #define CONFIG_SYS_CPU "armv7"
│   │   │   │   └─Done. (35.086s)
│   │   │   └─Done. (40.677s)
│   │   ├─Calling copy ...
│   │   │   ├─[lab1] cp /work/hs/tbot-workdir/uboot-wandboard-builder/System.map /var/lib/tftpboot/wandboard/tbot/System.map
│   │   │   └─Done. (0.003s)
│   │   ├─[lab1] chmod 666 /var/lib/tftpboot/wandboard/tbot/System.map
│   │   ├─Calling copy ...
│   │   │   ├─[lab1] cp /work/hs/tbot-workdir/uboot-wandboard-builder/u-boot.img /var/lib/tftpboot/wandboard/tbot/u-boot.img
│   │   │   └─Done. (0.003s)
│   │   ├─[lab1] chmod 666 /var/lib/tftpboot/wandboard/tbot/u-boot.img
│   │   ├─[lab1] ls -al /var/lib/tftpboot/wandboard/tbot/u-boot.img | cut -d ' ' -f 5
│   │   │    ## 561012
│   │   ├─Calling copy ...
│   │   │   ├─[lab1] cp /work/hs/tbot-workdir/uboot-wandboard-builder/u-boot.bin /var/lib/tftpboot/wandboard/tbot/u-boot.bin
│   │   │   └─Done. (0.003s)
│   │   ├─[lab1] chmod 666 /var/lib/tftpboot/wandboard/tbot/u-boot.bin
│   │   ├─Calling copy ...
│   │   │   ├─[lab1] cp /work/hs/tbot-workdir/uboot-wandboard-builder/u-boot.cfg /var/lib/tftpboot/wandboard/tbot/u-boot.cfg
│   │   │   └─Done. (0.002s)
│   │   ├─[lab1] chmod 666 /var/lib/tftpboot/wandboard/tbot/u-boot.cfg
│   │   ├─Calling copy ...
│   │   │   ├─[lab1] cp /work/hs/tbot-workdir/uboot-wandboard-builder/SPL /var/lib/tftpboot/wandboard/tbot/SPL
│   │   │   └─Done. (0.003s)
│   │   ├─[lab1] chmod 666 /var/lib/tftpboot/wandboard/tbot/SPL
│   │   ├─[lab1] ls -al /var/lib/tftpboot/wandboard/tbot/SPL | cut -d ' ' -f 5
│   │   │    ## 48128
│   │   └─Done. (41.072s)
│   ├─Calling wandboard_ub_install ...
│   │   ├─[local] ssh -o BatchMode=yes -i /home/hs/.ssh/id_rsa -p 22 hs@192.168.1.109
│   │   ├─[local] ssh -o BatchMode=yes -i /home/hs/.ssh/id_rsa -p 22 hs@192.168.1.109
│   │   ├─[lab1] kermit /home/hs/kermrc_wandboard
│   │   ├─POWERON (wandboard)
│   │   ├─[lab1] sudo sispmctl -D 01:01:56:a2:f1 -o 3
│   │   │    ## Accessing Gembird #0 USB device 021
│   │   │    ## Switched outlet 3 on
│   │   ├─UBOOT (wandboard-uboot)
│   │   │    <> Connecting to /dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0, speed 115200
│   │   │    <>  Escape character: Ctrl-\ (ASCII 28, FS): enabled
│   │   │    <> Type the escape character followed by C to get back,
│   │   │    <> or followed by ? to see other options.
│   │   │    <> ----------------------------------------------------
│   │   │    <> 
│   │   │    <> U-Boot SPL 2020.04-tbot-00687-gd16d37bcd4 (Apr 28 2020 - 14:58:35 +0200)
│   │   │    <> Trying to boot from MMC1
│   │   │    <> 
│   │   │    <> 
│   │   │    <> U-Boot 2020.04-tbot-00687-gd16d37bcd4 (Apr 28 2020 - 14:58:35 +0200)
│   │   │    <> 
│   │   │    <> CPU:   Freescale i.MX6DL rev1.3 at 792 MHz
│   │   │    <> Reset cause: POR
│   │   │    <> DRAM:  1 GiB
│   │   │    <> PMIC:  PFUZE100 ID=0x10
│   │   │    <> MMC:   FSL_SDHC: 2, FSL_SDHC: 1, FSL_SDHC: 0
│   │   │    <> Loading Environment from MMC... *** Warning - bad CRC, using default environment
│   │   │    <> 
│   │   │    <> No panel detected: default to HDMI
│   │   │    <> Display: HDMI (1024x768)
│   │   │    <> In:    serial
│   │   │    <> Out:   serial
│   │   │    <> Err:   serial
│   │   │    <> Board: Wandboard rev D1
│   │   │    <> Net:   
│   │   │    <> Warning: ethernet@2188000 using MAC address from ROM
│   │   │    <> eth0: ethernet@2188000
│   │   │    <> Hit any key to stop autoboot:  0 
│   │   │    <> => 
│   │   ├─[wandboard-uboot] setenv serverip 192.168.3.1
│   │   ├─[wandboard-uboot] printenv serverip
│   │   │    ## serverip=192.168.3.1
│   │   ├─[wandboard-uboot] setenv netmask 255.255.255.0
│   │   ├─[wandboard-uboot] printenv netmask
│   │   │    ## netmask=255.255.255.0
│   │   ├─[wandboard-uboot] setenv ipaddr 192.168.3.21
│   │   ├─[wandboard-uboot] printenv ipaddr
│   │   │    ## ipaddr=192.168.3.21
│   │   ├─[wandboard-uboot] setenv spl_file wandboard/tbot/SPL
│   │   ├─[wandboard-uboot] printenv spl_file
│   │   │    ## spl_file=wandboard/tbot/SPL
│   │   ├─[wandboard-uboot] setenv ub_file wandboard/tbot/u-boot.img
│   │   ├─[wandboard-uboot] printenv ub_file
│   │   │    ## ub_file=wandboard/tbot/u-boot.img
│   │   ├─[wandboard-uboot] setenv cmp_addr_r 11000000
│   │   ├─[wandboard-uboot] printenv cmp_addr_r
│   │   │    ## cmp_addr_r=11000000
│   │   ├─[wandboard-uboot] setenv calc_size 'setexpr fw_sz ${filesize} / 0x200; setexpr fw_sz ${fw_sz} + 1'
│   │   ├─[wandboard-uboot] printenv calc_size
│   │   │    ## calc_size=setexpr fw_sz ${filesize} / 0x200; setexpr fw_sz ${fw_sz} + 1
│   │   ├─[wandboard-uboot] setenv load_spl 'tftp ${loadaddr} ${spl_file};run calc_size'
│   │   ├─[wandboard-uboot] printenv load_spl
│   │   │    ## load_spl=tftp ${loadaddr} ${spl_file};run calc_size
│   │   ├─[wandboard-uboot] setenv load_ub 'tftp ${loadaddr} ${ub_file};run calc_size'
│   │   ├─[wandboard-uboot] printenv load_ub
│   │   │    ## load_ub=tftp ${loadaddr} ${ub_file};run calc_size
│   │   ├─[wandboard-uboot] setenv upd_prep 'mmc dev 0'
│   │   ├─[wandboard-uboot] printenv upd_prep
│   │   │    ## upd_prep=mmc dev 0
│   │   ├─[wandboard-uboot] setenv upd_spl 'run upd_prep;mmc write ${loadaddr} 2 ${fw_sz}'
│   │   ├─[wandboard-uboot] printenv upd_spl
│   │   │    ## upd_spl=run upd_prep;mmc write ${loadaddr} 2 ${fw_sz}
│   │   ├─[wandboard-uboot] setenv upd_ub 'run upd_prep;mmc write ${loadaddr} 8a ${fw_sz}'
│   │   ├─[wandboard-uboot] printenv upd_ub
│   │   │    ## upd_ub=run upd_prep;mmc write ${loadaddr} 8a ${fw_sz}
│   │   ├─[wandboard-uboot] setenv cmp_spl 'run load_spl;mmc read ${cmp_addr_r} 2 ${fw_sz};cmp.b ${loadaddr} ${cmp_addr_r} ${filesize}'
│   │   ├─[wandboard-uboot] printenv cmp_spl
│   │   │    ## cmp_spl=run load_spl;mmc read ${cmp_addr_r} 2 ${fw_sz};cmp.b ${loadaddr} ${cmp_addr_r} ${filesize}
│   │   ├─[wandboard-uboot] setenv cmp_ub 'run load_ub;mmc read ${cmp_addr_r} 8a ${fw_sz};cmp.b ${loadaddr} ${cmp_addr_r} ${filesize}'
│   │   ├─[wandboard-uboot] printenv cmp_ub
│   │   │    ## cmp_ub=run load_ub;mmc read ${cmp_addr_r} 8a ${fw_sz};cmp.b ${loadaddr} ${cmp_addr_r} ${filesize}
│   │   ├─[wandboard-uboot] setenv optargs 'run addip'
│   │   ├─[wandboard-uboot] printenv optargs
│   │   │    ## optargs=run addip
│   │   ├─[wandboard-uboot] setenv hostname wandboard
│   │   ├─[wandboard-uboot] printenv hostname
│   │   │    ## hostname=wandboard
│   │   ├─[wandboard-uboot] setenv netdev eth0
│   │   ├─[wandboard-uboot] printenv netdev
│   │   │    ## netdev=eth0
│   │   ├─[wandboard-uboot] setenv addip 'setenv bootargs ${bootargs} ip=${ipaddr}:${serverip}:${gatewayip}:${netmask}:${hostname}:${netdev}::off panic=1'
│   │   ├─[wandboard-uboot] printenv addip
│   │   │    ## addip=setenv bootargs ${bootargs} ip=${ipaddr}:${serverip}:${gatewayip}:${netmask}:${hostname}:${netdev}::off panic=1
│   │   ├─[wandboard-uboot] setenv upd_all 'run load_spl upd_spl load_ub upd_ub'
│   │   ├─[wandboard-uboot] printenv upd_all
│   │   │    ## upd_all=run load_spl upd_spl load_ub upd_ub
│   │   ├─[wandboard-uboot] run load_spl
│   │   │    ## ethernet@2188000 Waiting for PHY auto negotiation to complete.... done
│   │   │    ## Using ethernet@2188000 device
│   │   │    ## TFTP from server 192.168.3.1; our IP address is 192.168.3.21
│   │   │    ## Filename 'wandboard/tbot/SPL'.
│   │   │    ## Load address: 0x12000000
│   │   │    ## Loading: ####
│   │   │    ##          2 MiB/s
│   │   │    ## done
│   │   │    ## Bytes transferred = 48128 (bc00 hex)
│   │   ├─[wandboard-uboot] run upd_spl
│   │   │    ## switch to partitions #0, OK
│   │   │    ## mmc0 is current device
│   │   │    ## 
│   │   │    ## MMC write: dev # 0, block # 2, count 95 ... 95 blocks written: OK
│   │   ├─[wandboard-uboot] run cmp_spl
│   │   │    ## Using ethernet@2188000 device
│   │   │    ## TFTP from server 192.168.3.1; our IP address is 192.168.3.21
│   │   │    ## Filename 'wandboard/tbot/SPL'.
│   │   │    ## Load address: 0x12000000
│   │   │    ## Loading: ####
│   │   │    ##          2.9 MiB/s
│   │   │    ## done
│   │   │    ## Bytes transferred = 48128 (bc00 hex)
│   │   │    ## 
│   │   │    ## MMC read: dev # 0, block # 2, count 95 ... 95 blocks read: OK
│   │   │    ## Total of 48128 byte(s) were the same
│   │   ├─[wandboard-uboot] run load_ub
│   │   │    ## Using ethernet@2188000 device
│   │   │    ## TFTP from server 192.168.3.1; our IP address is 192.168.3.21
│   │   │    ## Filename 'wandboard/tbot/u-boot.img'.
│   │   │    ## Load address: 0x12000000
│   │   │    ## Loading: #######################################
│   │   │    ##          2.6 MiB/s
│   │   │    ## done
│   │   │    ## Bytes transferred = 561012 (88f74 hex)
│   │   ├─[wandboard-uboot] run upd_ub
│   │   │    ## switch to partitions #0, OK
│   │   │    ## mmc0 is current device
│   │   │    ## 
│   │   │    ## MMC write: dev # 0, block # 138, count 1096 ... 1096 blocks written: OK
│   │   ├─[wandboard-uboot] run cmp_ub
│   │   │    ## Using ethernet@2188000 device
│   │   │    ## TFTP from server 192.168.3.1; our IP address is 192.168.3.21
│   │   │    ## Filename 'wandboard/tbot/u-boot.img'.
│   │   │    ## Load address: 0x12000000
│   │   │    ## Loading: #######################################
│   │   │    ##          2.6 MiB/s
│   │   │    ## done
│   │   │    ## Bytes transferred = 561012 (88f74 hex)
│   │   │    ## 
│   │   │    ## MMC read: dev # 0, block # 138, count 1096 ... 1096 blocks read: OK
│   │   │    ## Total of 561012 byte(s) were the same
│   │   ├─POWEROFF (wandboard)
│   │   ├─[lab1] sudo sispmctl -D 01:01:56:a2:f1 -f 3
│   │   │    ## Accessing Gembird #0 USB device 021
│   │   │    ## Switched outlet 3 off
│   │   └─Done. (12.420s)
│   ├─Calling wandboard_ub_check_version ...
│   │   ├─[local] ssh -o BatchMode=yes -i /home/hs/.ssh/id_rsa -p 22 hs@192.168.1.109
│   │   ├─[lab1] strings /var/lib/tftpboot/wandboard/tbot/u-boot.bin | grep --color=never "U-Boot 2"
│   │   │    ## U-Boot 2020.04-tbot-00687-gd16d37bcd4 (Apr 28 2020 - 15:17:18 +0200)
│   │   ├─found in image U-Boot version U-Boot 2020.04-tbot-00687-gd16d37bcd4 (Apr 28 2020 - 15:17:18 +0200)
│   │   ├─[lab1] strings /var/lib/tftpboot/wandboard/tbot/SPL | grep --color=never "U-Boot SPL"
│   │   │    ## U-Boot SPL 2020.04-tbot-00687-gd16d37bcd4 (Apr 28 2020 - 15:17:18 +0200)
│   │   ├─found in image U-Boot SPL version U-Boot SPL 2020.04-tbot-00687-gd16d37bcd4 (Apr 28 2020 - 15:17:18 +0200)
│   │   ├─[local] ssh -o BatchMode=yes -i /home/hs/.ssh/id_rsa -p 22 hs@192.168.1.109
│   │   ├─[lab1] kermit /home/hs/kermrc_wandboard
│   │   ├─POWERON (wandboard)
│   │   ├─[lab1] sudo sispmctl -D 01:01:56:a2:f1 -o 3
│   │   │    ## Accessing Gembird #0 USB device 021
│   │   │    ## Switched outlet 3 on
│   │   ├─UBOOT (wandboard-uboot)
│   │   │    <> Connecting to /dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0, speed 115200
│   │   │    <>  Escape character: Ctrl-\ (ASCII 28, FS): enabled
│   │   │    <> Type the escape character followed by C to get back,
│   │   │    <> or followed by ? to see other options.
│   │   │    <> ----------------------------------------------------
│   │   │    <> 
│   │   │    <> U-Boot SPL 2020.04-tbot-00687-gd16d37bcd4 (Apr 28 2020 - 15:17:18 +0200)
│   │   │    <> Trying to boot from MMC1
│   │   │    <> 
│   │   │    <> 
│   │   │    <> U-Boot 2020.04-tbot-00687-gd16d37bcd4 (Apr 28 2020 - 15:17:18 +0200)
│   │   │    <> 
│   │   │    <> CPU:   Freescale i.MX6DL rev1.3 at 792 MHz
│   │   │    <> Reset cause: POR
│   │   │    <> DRAM:  1 GiB
│   │   │    <> PMIC:  PFUZE100 ID=0x10
│   │   │    <> MMC:   FSL_SDHC: 2, FSL_SDHC: 1, FSL_SDHC: 0
│   │   │    <> Loading Environment from MMC... *** Warning - bad CRC, using default environment
│   │   │    <> 
│   │   │    <> No panel detected: default to HDMI
│   │   │    <> Display: HDMI (1024x768)
│   │   │    <> In:    serial
│   │   │    <> Out:   serial
│   │   │    <> Err:   serial
│   │   │    <> Board: Wandboard rev D1
│   │   │    <> Net:   
│   │   │    <> Warning: ethernet@2188000 using MAC address from ROM
│   │   │    <> eth0: ethernet@2188000
│   │   │    <> Hit any key to stop autoboot:  0 
│   │   │    <> => 
│   │   ├─found U-Boot SPL version U-Boot SPL 2020.04-tbot-00687-gd16d37bcd4 (Apr 28 2020 - 15:17:18 +0200) installed
│   │   ├─found U-Boot version U-Boot 2020.04-tbot-00687-gd16d37bcd4 (Apr 28 2020 - 15:17:18 +0200) installed
│   │   ├─POWEROFF (wandboard)
│   │   ├─[lab1] sudo sispmctl -D 01:01:56:a2:f1 -f 3
│   │   │    ## Accessing Gembird #0 USB device 021
│   │   │    ## Switched outlet 3 off
│   │   └─Done. (8.939s)
│   ├─Calling uboot_testpy ...
│   │   ├─[local] ssh -o BatchMode=yes -i /home/hs/.ssh/id_rsa -p 22 hs@192.168.1.109
│   │   ├─[local] ssh -o BatchMode=yes -i /home/hs/.ssh/id_rsa -p 22 hs@192.168.1.109
│   │   ├─[lab1] bash --norc --noprofile
│   │   ├─[local] ssh -o BatchMode=yes -i /home/hs/.ssh/id_rsa -p 22 hs@192.168.1.109
│   │   ├─[local] ssh -o BatchMode=yes -i /home/hs/.ssh/id_rsa -p 22 hs@192.168.1.109
│   │   ├─Calling uboot_setup_testhooks ...
│   │   │   ├─[lab1] mkdir -p /work/hs/tbot-workdir
│   │   │   ├─[lab1] test -d /work/hs/tbot-workdir/uboot-testpy-tbot
│   │   │   ├─Creating FIFOs ...
│   │   │   ├─[lab1] rm -rf /work/hs/tbot-workdir/uboot-testpy-tbot/fifo_console_send
│   │   │   ├─[lab1] mkfifo /work/hs/tbot-workdir/uboot-testpy-tbot/fifo_console_send
│   │   │   ├─[lab1] rm -rf /work/hs/tbot-workdir/uboot-testpy-tbot/fifo_console_recv
│   │   │   ├─[lab1] mkfifo /work/hs/tbot-workdir/uboot-testpy-tbot/fifo_console_recv
│   │   │   ├─[lab1] rm -rf /work/hs/tbot-workdir/uboot-testpy-tbot/fifo_commands
│   │   │   ├─[lab1] mkfifo /work/hs/tbot-workdir/uboot-testpy-tbot/fifo_commands
│   │   │   ├─[lab1] cat /work/hs/tbot-workdir/uboot-testpy-tbot/tbot-scripts.sha256
│   │   │   │    ## 2d30892b61eb713ce9413e06c4f2a0cd00d2a74b6b8c2ac6624e1e49909b1897
│   │   │   ├─Hooks are up to date, skipping deployment ...
│   │   │   ├─Adding hooks to $PATH ...
│   │   │   ├─[lab1] echo " ${PATH}"
│   │   │   │    ##  /home/hs/.local/bin:/home/hs/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
│   │   │   ├─[lab1] export PATH=/work/hs/tbot-workdir/uboot-testpy-tbot:/home/hs/.local/bin:/home/hs/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
│   │   │   ├─Open console & command channels ...
│   │   │   ├─[lab1] /work/hs/tbot-workdir/uboot-testpy-tbot/tbot-console
│   │   │   ├─[lab1] /work/hs/tbot-workdir/uboot-testpy-tbot/tbot-commands
│   │   │   └─Done. (0.025s)
│   │   ├─Calling uboot_checkout ...
│   │   │   ├─Builder: wandboard-builder
│   │   │   ├─[lab1] test -d /work/hs/tbot-workdir/uboot-wandboard-builder/.git
│   │   │   ├─[lab1] git -C /work/hs/tbot-workdir/uboot-wandboard-builder fetch
│   │   │   ├─[lab1] git -C /work/hs/tbot-workdir/uboot-wandboard-builder rev-parse HEAD
│   │   │   │    ## d16d37bcd4087b8ea0f66cb76a73edad182d151a
│   │   │   └─Done. (1.172s)
│   │   ├─[lab1] test -e /work/hs/tbot-workdir/uboot-wandboard-builder/.config
│   │   ├─[lab1] test -e /work/hs/tbot-workdir/uboot-wandboard-builder/include/autoconf.mk
│   │   ├─[local] ssh -o BatchMode=yes -i /home/hs/.ssh/id_rsa -p 22 hs@192.168.1.109
│   │   ├─[lab1] kermit /home/hs/kermrc_wandboard
│   │   ├─POWERON (wandboard)
│   │   ├─[lab1] sudo sispmctl -D 01:01:56:a2:f1 -o 3
│   │   │    ## Accessing Gembird #0 USB device 021
│   │   │    ## Switched outlet 3 on
│   │   ├─UBOOT (wandboard-uboot)
│   │   │    <> Connecting to /dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0, speed 115200
│   │   │    <>  Escape character: Ctrl-\ (ASCII 28, FS): enabled
│   │   │    <> Type the escape character followed by C to get back,
│   │   │    <> or followed by ? to see other options.
│   │   │    <> ----------------------------------------------------
│   │   │    <> 
│   │   │    <> U-Boot SPL 2020.04-tbot-00687-gd16d37bcd4 (Apr 28 2020 - 15:17:18 +0200)
│   │   │    <> Trying to boot from MMC1
│   │   │    <> 
│   │   │    <> 
│   │   │    <> U-Boot 2020.04-tbot-00687-gd16d37bcd4 (Apr 28 2020 - 15:17:18 +0200)
│   │   │    <> 
│   │   │    <> CPU:   Freescale i.MX6DL rev1.3 at 792 MHz
│   │   │    <> Reset cause: POR
│   │   │    <> DRAM:  1 GiB
│   │   │    <> PMIC:  PFUZE100 ID=0x10
│   │   │    <> MMC:   FSL_SDHC: 2, FSL_SDHC: 1, FSL_SDHC: 0
│   │   │    <> Loading Environment from MMC... *** Warning - bad CRC, using default environment
│   │   │    <> 
│   │   │    <> No panel detected: default to HDMI
│   │   │    <> Display: HDMI (1024x768)
│   │   │    <> In:    serial
│   │   │    <> Out:   serial
│   │   │    <> Err:   serial
│   │   │    <> Board: Wandboard rev D1
│   │   │    <> Net:   
│   │   │    <> Warning: ethernet@2188000 using MAC address from ROM
│   │   │    <> eth0: ethernet@2188000
│   │   │    <> Hit any key to stop autoboot:  0 
│   │   │    <> => 
│   │   ├─[lab1] cd /work/hs/tbot-workdir/uboot-wandboard-builder
│   │   ├─[lab1] ./test/py/test.py --build-dir . --board-type unknown
│   │   │    ## +u-boot-test-flash unknown na
│   │   │    ## ================================================== test session starts ===================================================
│   │   │    ## platform linux -- Python 3.8.2, pytest-5.2.1, py-1.8.0, pluggy-0.13.0
│   │   │    ## rootdir: /work/hs/tbot-workdir/uboot-wandboard-builder/test/py, inifile: pytest.ini
│   │   │    ## collected 304 items                                                                                                      
│   │   ├─[lab1] sudo sispmctl -D 01:01:56:a2:f1 -f 3
│   │   │    ## Accessing Gembird #0 USB device 021
│   │   │    ## Switched outlet 3 off
│   │   ├─[lab1] sudo sispmctl -D 01:01:56:a2:f1 -o 3
│   │   │    ## Accessing Gembird #0 USB device 021
│   │   │    ## Switched outlet 3 on
│   │   │    ## 
│   │   │    ## test/py/tests/test_000_version.py .                                                                                [  0%]
│   │   │    ## test/py/tests/test_bind.py ss                                                                                      [  0%]
│   │   │    ## test/py/tests/test_dfu.py s                                                                                        [  0%]
│   │   │    ## test/py/tests/test_dm.py s                                                                                         [  0%]
│   │   │    ## test/py/tests/test_efi_fit.py s                                                                                    [  0%]
│   │   │    ## test/py/tests/test_efi_loader.py .sssss                                                                            [  0%]
│   │   │    ## test/py/tests/test_efi_selftest.py sssss                                                                           [  0%]
│   │   │    ## test/py/tests/test_env.py ............                                                                             [  0%]
│   │   │    ## test/py/tests/test_fit.py s                                                                                        [  0%]
│   │   │    ## test/py/tests/test_fpga.py ssssssssssssssssssssssssssss                                                            [  0%]
│   │   │    ## test/py/tests/test_gpio.py ss                                                                                      [  0%]
│   │   │    ## test/py/tests/test_gpt.py sssssss                                                                                  [  0%]
│   │   │    ## test/py/tests/test_handoff.py s                                                                                    [  0%]
│   │   │    ## test/py/tests/test_help.py .                                                                                       [  0%]
│   │   │    ## test/py/tests/test_hush_if_test.py ......................................................................s         [  0%]
│   │   │    ## test/py/tests/test_log.py ss                                                                                       [  0%]
│   │   │    ## test/py/tests/test_md.py ..                                                                                        [  0%]
│   │   │    ## test/py/tests/test_mmc_rd.py ssss                                                                                  [  0%]
│   │   │    ## test/py/tests/test_mmc_wr.py s                                                                                     [  0%]
│   │   │    ## test/py/tests/test_net.py .sssss                                                                                   [  0%]
│   │   │    ## test/py/tests/test_ofplatdata.py ss                                                                                [  0%]
│   │   │    ## test/py/tests/test_pinmux.py ..ss.ss                                                                               [  0%]
│   │   │    ## test/py/tests/test_sandbox_exit.py ss                                                                              [  0%]
│   │   │    ## test/py/tests/test_sf.py ssss                                                                                      [  0%]
│   │   │    ## test/py/tests/test_shell_basics.py ....                                                                            [  0%]
│   │   │    ## test/py/tests/test_sleep.py .                                                                                      [  0%]
│   │   │    ## test/py/tests/test_tpm2.py sssssssssss                                                                             [  0%]
│   │   │    ## test/py/tests/test_ums.py s                                                                                        [  0%]
│   │   │    ## test/py/tests/test_unknown_cmd.py .                                                                                [  0%]
│   │   │    ## test/py/tests/test_ut.py ss                                                                                        [  0%]
│   │   │    ## test/py/tests/test_vboot.py sssss                                                                                  [  0%]
│   │   │    ## test/py/tests/test_android/test_ab.py s                                                                            [  0%]
│   │   │    ## test/py/tests/test_android/test_abootimg.py s                                                                      [  0%]
│   │   │    ## test/py/tests/test_android/test_avb.py ssssss                                                                      [  0%]
│   │   │    ## test/py/tests/test_efi_secboot/test_authvar.py sssss                                                               [  0%]
│   │   │    ## test/py/tests/test_efi_secboot/test_signed.py ss                                                                   [  0%]
│   │   │    ## test/py/tests/test_efi_secboot/test_unsigned.py sss                                                                [  0%]
│   │   │    ## test/py/tests/test_fs/test_basic.py sssssssssssssssssssssssssssssssssssssss                                        [  0%]
│   │   │    ## test/py/tests/test_fs/test_ext.py ssssssssssssssssssssss                                                           [  0%]
│   │   │    ## test/py/tests/test_fs/test_mkdir.py ssssssssssss                                                                   [  0%]
│   │   │    ## test/py/tests/test_fs/test_symlink.py ssss                                                                         [  0%]
│   │   │    ## test/py/tests/test_fs/test_unlink.py ssssssssssssss
│   │   │    ## 
│   │   │    ## ============================================ 97 passed, 207 skipped in 12.38s ============================================
│   │   ├─POWEROFF (wandboard)
│   │   ├─[lab1] sudo sispmctl -D 01:01:56:a2:f1 -f 3
│   │   │    ## Accessing Gembird #0 USB device 021
│   │   │    ## Switched outlet 3 off
│   │   └─Done. (24.593s)
│   └─Done. (87.028s)
├─────────────────────────────────────────
├─Log written to '/home/hs/data/Entwicklung/wandboard/tbot-tbot2go/log/lab1-wandboard-0169.json'
└─SUCCESS (88.801s)
hs@lab-1:tbot-tbot2go  [wandboard-devel-messe] $ ./push-testresult.py -p /home/hs/data/Entwicklung/tbot/
log/lab1-wandboard-0169.json -> results/pushresults/lab1-wandboard-0169.txt
hs@lab-1:tbot-tbot2go  [wandboard-devel-messe] $
```
