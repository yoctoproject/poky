FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

# atom-pc support
COMPATIBLE_MACHINE_atom-pc = "atom-pc"
KMACHINE_atom-pc = "atom-pc"
KBRANCH_atom-pc = "yocto/standard/preempt-rt/base"
SRCREV_machine_pn-linux-yocto-rt_atom-pc = "2f9d925f5681eaae7f341cc1270c739e8b329c03"

# mpc8315e-rdb support
COMPATIBLE_MACHINE_mpc8315e-rdb = "mpc8315e-rdb"
KMACHINE_mpc8315e-rdb = "fsl-mpc8315e-rdb"
KBRANCH_mpc8315e-rdb = "yocto/standard/preempt-rt/base"
SRCREV_machine_pn-linux-yocto-rt_mpc8315e-rdb = "2f9d925f5681eaae7f341cc1270c739e8b329c03"

# beagleboard support - 3.0 support has not yet been completed, build failure
#COMPATIBLE_MACHINE_beagleboard = "beagleboard"
#KMACHINE_beagleboard = "beagleboard"
#KBRANCH_beagleboard = "yocto/standard/preempt-rt/base"
#SRCREV_machine_pn-linux-yocto-rt_beagleboard = 

# routerstationpro support - preempt-rt kernel build failure
COMPATIBLE_MACHINE_routerstationpro = "routerstationpro"
KMACHINE_routerstationpro = "routerstationpro"
KBRANCH_routerstationpro = "yocto/standard/preempt-rt/routerstationpro"
SRCREV_machine_pn-linux-yocto-rt_routerstationpro = "855fb36f410e5ed1b42a2cb9d4f10c55e5a510c1"
