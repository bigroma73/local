DESCRIPTION = "dvbapp2-plugin-extensions-easyplipanel"
SECTION = "base"
PRIORITY = "optional"
LICENSE = "GPL"
MAINTAINER = "2boom"
DEPENDS = "enigma2"
RDEPENDS = "busybox-cron ntpdate enigma2"

PV = "2.7c"
#PR="2.7b"

SRC_URI="file://easyplipanel.tar.gz \
"

S = "${WORKDIR}"
FILES_${PN} = "/usr"
PLUGIN_DIR="/usr/lib/enigma2/python/Plugins/Extensions"

#PACKAGE_ARCH = "all"

do_install() {
	install -d ${D}/usr/keys
	for f in ${WORKDIR}/usr/keys/*; do
		f1=$(basename ${f})
        install -m 0644 ${WORKDIR}/usr/keys/${f1} ${D}/usr/keys/${f1};
    done
	install -d ${D}${PLUGIN_DIR}/PliPanel/locale/ru/LC_MESSAGES
	install -m 0644 ${WORKDIR}${PLUGIN_DIR}/locale/ru/LC_MESSAGES/PliPanel.mo \
					${D}${PLUGIN_DIR}/PliPanel/locale/ru/LC_MESSAGES/PliPanel.mo
	install -d ${D}${PLUGIN_DIR}/PliPanel/images
	for f in ${WORKDIR}${PLUGIN_DIR}/images/*; do
		f1=$(basename ${f})
		install -m 0644 ${WORKDIR}${PLUGIN_DIR}/images/${f1} ${D}${PLUGIN_DIR}/PliPanel/images/${f1};
	done
	for f in ${WORKDIR}${PLUGIN_DIR}/PliPanel/*; do
		f1=$(basename ${f})
		install -m 0644 ${WORKDIR}${PLUGIN_DIR}/PliPanel/${f1} ${D}${PLUGIN_DIR}/PliPanel/${f1};
	done
	install -d ${D}/usr/script
	for f in ${WORKDIR}/usr/script/*; do
		f1=$(basename ${f})
        install -m 0644 ${WORKDIR}/usr/script/${f1} ${D}/usr/script/${f1};
    done
}

do_configure() {
}

do_compile() {
}
