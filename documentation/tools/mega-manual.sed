# Processes ref-manual and yocto-project-qs manual (<word>-<word>-<word> style)
s/\"ulink\" href=\"http:\/\/www.yoctoproject.org\/docs\/1.5\/[a-z]*-[a-z]*-[a-z]*\/[a-z]*-[a-z]*-[a-z]*.html#/\"link\" href=\"#/g

# Processes all other manuals (<word>-<word> style)
s/\"ulink\" href=\"http:\/\/www.yoctoproject.org\/docs\/1.5\/[a-z]*-[a-z]*\/[a-z]*-[a-z]*.html#/\"link\" href=\"#/g

# Process cases where just an external manual is referenced without an id anchor
s/<a class=\"ulink\" href=\"http:\/\/www.yoctoproject.org\/docs\/1.5\/yocto-project-qs\/yocto-project-qs.html\" target=\"_top\">Yocto Project Quick Start<\/a>/Yocto Project Quick Start/g
s/<a class=\"ulink\" href=\"http:\/\/www.yoctoproject.org\/docs\/1.5\/dev-manual\/dev-manual.html\" target=\"_top\">Yocto Project Development Manual<\/a>/Yocto Project Development Manual/g
s/<a class=\"ulink\" href=\"http:\/\/www.yoctoproject.org\/docs\/1.5\/adt-manual\/adt-manual.html\" target=\"_top\">Yocto Project Application Developer's Guide<\/a>/Yocto Project Application Developer's Guide/g
s/<a class=\"ulink\" href=\"http:\/\/www.yoctoproject.org\/docs\/1.5\/bsp-guide\/bsp-guide.html\" target=\"_top\">Yocto Project Board Support Package (BSP) Developer's Guide<\/a>/Yocto Project Board Support Package (BSP) Developer's Guide/g
s/<a class=\"ulink\" href=\"http:\/\/www.yoctoproject.org\/docs\/1.5\/kernel-manual\/kernel-manual.html\" target=\"_top\">Yocto Project Kernel Architecture and Use Manual<\/a>/Yocto Project Kernel Architecture and Use Manual/g
s/<a class=\"ulink\" href=\"http:\/\/www.yoctoproject.org\/docs\/1.5\/kernel-ref\/kernel-ref.html\" target=\"_top\">Yocto Project Kernel Development Manual<\/a>/Yocto Project Kernel Development Manual/g
s/<a class=\"ulink\" href=\"http:\/\/www.yoctoproject.org\/docs\/1.5\/ref-manual\/ref-manual.html\" target=\"_top\">Yocto Project Reference Manual<\/a>/Yocto Project Reference Manual/g
