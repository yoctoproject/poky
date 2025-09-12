require ${BPN}.inc

PACKAGECONFIG = " \
	gallium \
	video-codecs \
	${@bb.utils.filter('DISTRO_FEATURES', 'x11 vulkan wayland glvnd', d)} \
	${@bb.utils.contains('DISTRO_FEATURES', 'opengl', 'opengl egl gles gbm virgl', '', d)} \
	${@bb.utils.contains('DISTRO_FEATURES', 'vulkan', 'zink', '', d)} \
	xmlconfig \
"

PACKAGECONFIG:append:x86 = " libclc gallium-llvm intel amd nouveau svga"
PACKAGECONFIG:append:x86-64 = " libclc gallium-llvm intel amd nouveau svga"
PACKAGECONFIG:append:i686 = " libclc gallium-llvm intel amd nouveau svga"
PACKAGECONFIG:append:class-native = " libclc gallium-llvm amd nouveau svga"

GLPROVIDES = " \
    ${@bb.utils.contains('PACKAGECONFIG', 'opengl', 'virtual/libgl', '', d)} \
    ${@bb.utils.contains('PACKAGECONFIG', 'gles', 'virtual/libgles1 virtual/libgles2 virtual/libgles3', '', d)} \
    ${@bb.utils.contains('PACKAGECONFIG', 'egl', 'virtual/egl', '', d)} \
"
PROVIDES = " \
    ${@bb.utils.contains('PACKAGECONFIG', 'glvnd', '', d.getVar('GLPROVIDES'), d)} \
    ${@bb.utils.contains('PACKAGECONFIG', 'gbm', 'virtual/libgbm', '', d)} \
    virtual/mesa \
"

BBCLASSEXTEND = "native nativesdk"
