FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

PR := "${PR}.1"

COMPATIBLE_MACHINE_{{=machine}} = "{{=machine}}"

{{ input type:"boolean" name:"need_new_kbranch" prio:"20" msg:"Do you need a new machine branch for this BSP (the alternative is to re-use an existing branch)? [y/n]" default:"y" }}

{{ if need_new_kbranch == "y": }}
{{ input type:"choicelist" name:"new_kbranch" gen:"bsp.kernel.all_branches" branches_base:"yocto/standard:yocto/standard/common-pc-64" prio:"20" msg:"Please choose a machine branch to base this BSP on:" default:"yocto/standard/common-pc-64/base" }}

{{ if need_new_kbranch == "n": }}
{{ input type:"choicelist" name:"existing_kbranch" gen:"bsp.kernel.all_branches" branches_base:"yocto/standard:yocto/standard/common-pc-64" prio:"20" msg:"Please choose a machine branch to base this BSP on:" default:"yocto/standard/common-pc-64/base" }}

{{ if need_new_kbranch == "y": }}
KBRANCH_{{=machine}}  = "{{=strip_base(new_kbranch)}}/{{=machine}}"
{{ if need_new_kbranch == "n": }}
KBRANCH_{{=machine}}  = "{{=existing_kbranch}}"

KMACHINE_{{=machine}}  = "{{=machine}}"

{{ input type:"boolean" name:"smp" prio:"30" msg:"Do you need SMP support? (y/n)" default:"y"}}
{{ if smp == "y": }}
KERNEL_FEATURES_append_{{=machine}} += " cfg/smp.scc"

{{ if need_new_kbranch == "y": }}
YOCTO_KERNEL_EXTERNAL_BRANCH_{{=machine}}  = "{{=strip_base(new_kbranch)}}/{{=machine}}"
{{ if need_new_kbranch == "n": }}
YOCTO_KERNEL_EXTERNAL_BRANCH_{{=machine}}  = "{{=existing_kbranch}}"

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
