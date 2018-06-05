
do_configure_prepend() {
	QT_CONFIG_FLAGS += " \
		-no-sse2 \
	"
}