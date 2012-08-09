FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

PR := "${PR}.1"

COMPATIBLE_MACHINE_{{=machine}} = "{{=machine}}"

{{ input type:"boolean" name:"need_new_kbranch" prio:"20" msg:"Do you need a new machine branch for this BSP (the alternative is to re-use an existing branch)? [y/n]" default:"y" }}

{{ if need_new_kbranch == "y" and qemuarch == "arm": }}
{{ input type:"choicelist" name:"new_kbranch" gen:"bsp.kernel.all_branches" branches_base:"yocto/standard" prio:"20" msg:"Please choose a machine branch to base your new BSP branch on:" default:"yocto/standard/base" }}

{{ if need_new_kbranch == "n" and qemuarch == "arm": }}
{{ input type:"choicelist" name:"existing_kbranch" gen:"bsp.kernel.all_branches" branches_base:"yocto/standard" prio:"20" msg:"Please choose an existing machine branch to use for this BSP:" default:"yocto/standard/arm-versatile-926ejs" }}

{{ if need_new_kbranch == "y" and qemuarch == "powerpc": }}
{{ input type:"choicelist" name:"new_kbranch" nameappend:"powerpc" gen:"bsp.kernel.all_branches" branches_base:"yocto/standard" prio:"20" msg:"Please choose a machine branch to base this BSP on:" default:"yocto/standard/base" }}

{{ if need_new_kbranch == "n" and qemuarch == "powerpc": }}
{{ input type:"choicelist" name:"existing_kbranch" nameappend:"powerpc" gen:"bsp.kernel.all_branches" branches_base:"yocto/standard" prio:"20" msg:"Please choose a machine branch to base this BSP on:" default:"yocto/standard/qemu-ppc32" }}

{{ if need_new_kbranch == "y" and qemuarch == "i386": }}
{{ input type:"choicelist" name:"new_kbranch" nameappend:"i386" gen:"bsp.kernel.all_branches" branches_base:"yocto/standard:yocto/standard/common-pc" prio:"20" msg:"Please choose a machine branch to base this BSP on:" default:"yocto/standard/common-pc/base" }}

{{ if need_new_kbranch == "n" and qemuarch == "i386": }}
{{ input type:"choicelist" name:"existing_kbranch" nameappend:"i386" gen:"bsp.kernel.all_branches" branches_base:"yocto/standard:yocto/standard/common-pc" prio:"20" msg:"Please choose a machine branch to base this BSP on:" default:"yocto/standard/common-pc/base" }}

{{ if need_new_kbranch == "y" and qemuarch == "x86_64": }}
{{ input type:"choicelist" name:"new_kbranch" nameappend:"x86_64" gen:"bsp.kernel.all_branches" branches_base:"yocto/standard:yocto/standard/common-pc-64"  prio:"20" msg:"Please choose a machine branch to base this BSP on:" default:"yocto/standard/common-pc-64/base" }}

{{ if need_new_kbranch == "n" and qemuarch == "x86_64": }}
{{ input type:"choicelist" name:"existing_kbranch" nameappend:"x86_64" gen:"bsp.kernel.all_branches" branches_base:"yocto/standard:yocto/standard/common-pc-64"  prio:"20" msg:"Please choose a machine branch to base this BSP on:" default:"yocto/standard/common-pc-64/base" }}

{{ if need_new_kbranch == "y" and qemuarch == "mips": }}
{{ input type:"choicelist" name:"new_kbranch" nameappend:"mips" gen:"bsp.kernel.all_branches" branches_base:"yocto/standard" prio:"20" msg:"Please choose a machine branch to base this BSP on:" default:"yocto/standard/base" }}

{{ if need_new_kbranch == "n" and qemuarch == "mips": }}
{{ input type:"choicelist" name:"existing_kbranch" nameappend:"mips" gen:"bsp.kernel.all_branches" branches_base:"yocto/standard" prio:"20" msg:"Please choose a machine branch to base this BSP on:" default:"yocto/standard/mti-malta32-be" }}

{{ if need_new_kbranch == "y": }}
KBRANCH_{{=machine}}  = "{{=strip_base(new_kbranch)}}/{{=machine}}"
{{ if need_new_kbranch == "n": }}
KBRANCH_{{=machine}}  = "{{=existing_kbranch}}"

{{ if need_new_kbranch == "y": }}
YOCTO_KERNEL_EXTERNAL_BRANCH_{{=machine}}  = "{{=strip_base(new_kbranch)}}/{{=machine}}"

KMACHINE_{{=machine}}  = "{{=machine}}"

{{ input type:"boolean" name:"smp" prio:"30" msg:"Would you like SMP support? (y/n)" default:"y"}}
{{ if smp == "y": }}
KERNEL_FEATURES_append_{{=machine}} += " cfg/smp.scc"

SRC_URI += "file://{{=machine}}-standard.scc \
            file://{{=machine}}.scc \
            file://{{=machine}}.cfg \
            file://user-config.cfg \
            file://user-patches.scc \
           "

# uncomment and replace these SRCREVs with the real commit ids once you've had
# the appropriate changes committed to the upstream linux-yocto repo
#SRCREV_machine_pn-linux-yocto_{{=machine}} ?= "417fc778a86e81303bab5883b919ee422ec51c04"
#SRCREV_meta_pn-linux-yocto_{{=machine}} ?= "138bf5b502607fe40315c0d76822318d77d97e01"
