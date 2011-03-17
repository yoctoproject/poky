IMAGE_FEATURES += "apps-console-core "

IMAGE_INSTALL = "\
    task-poky-boot \
    task-poky-basic \
    "

#    ${POKY_BASE_INSTALL} 

inherit poky-image
