DESCRIPTION = "3rd party skins for Enigma2"
MAINTAINER = "TBA"
RDEPENDS = ""
PACKAGES = "${PN}-meta ${PN}"
PACKAGES_DYNAMIC = "3rd-skins-*"

inherit gitpkgv

PV = "git${SRCPV}"
PKGV = "git${GITPKGV}"
PR = "r0"
SRCREV="${AUTOREV}"
BRANCH = "master"

SRC_URI = "git://github.com/bigroma73/3rd-skins.git;protocol=git;branch=${BRANCH}"

# note that enigma2-skins is just an empty package to satisfy silly dependencies.
ALLOW_EMPTY = "1"
FILES_${PN} = "/usr/share/enigma2 /usr/share/fonts /usr/lib/enigma2/python"
FILES_${PN}-meta = "${datadir}/meta"
RDEPENDS_${PN}-meta = ""

inherit autotools

S = "${WORKDIR}/git"

python populate_packages_prepend () {
	if bb.data.expand('${REL_MINOR}', d) != "4":
		enigma2_skindir = bb.data.expand('${datadir}/enigma2', d)
		do_split_packages(d, enigma2_skindir, '(.*?)/.*', '3rd-skins-%s', 'Enigma2 Skin: %s', recursive=True, match_path=True, prepend=True)
}
