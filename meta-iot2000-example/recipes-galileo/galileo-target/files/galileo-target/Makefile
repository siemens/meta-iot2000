
ifdef CROSS_COMPILE
CC := $(CROSS_COMPILE)gcc
endif

ifndef BOARD_NAME
BOARD_NAME=galileo
endif

GALILEO_TGT_LOADER= clloader
GALILEO_TGT_RESET_HANDLER= galileo_sketch_reset

SRC =  crctab.c clloader.c  lsyslog.c   protname.c  rbsb.c   timing.c  zm.c  zperr.c  tcp.c zreadline.c  xstrtoul.c canit.c long-options.c 

RST_SRC = ./galileo-reset/galileo-reset.c

IDIR =.

ifdef CROSS_COMPILE
CFLAGS=-I$(IDIR) -I$(IDIR)/../ -I../lib  -D_XOPEN_SOURCE  -DLOCALEDIR=\"/usr/local/share/locale\" -DNFGVMIN -DHAVE_CONFIG_H -DCLANTON_LOADER -g -Wall  -std=c99 -m32 -Os -march=pentium -ffunction-sections  
else
CFLAGS=-I$(IDIR) -I$(IDIR)/../ -I../lib   -D_XOPEN_SOURCE  -DNFGVMIN -DHAVE_CONFIG_H -DCLANTON_LOADER -g -Wall  -std=c99  -Os  -ffunction-sections
endif

all: clloader galileo_sketch_reset

ODIR=.
LIBS=

DEPEND = $(SRC:.c=.d)

_OBJ = $(SRC:.c=.o)
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

$(ODIR)/%.o: %.c $(DEPEND)
	$(CC) -c -o $@ $< $(CFLAGS) $(CFLAGS_EXTRA)

clloader: $(OBJ)
	$(CC) -o $@ $^ $(LDFLAGS) $(LIBS)




RST_ODIR=.
RST_DEPEND = $(RST_SRC:.c=.d)
_RST_OBJ = $(RST_SRC:.c=.o)
RST_OBJ = $(patsubst %,$(RST_ODIR)/%,$(_RST_OBJ))

$(RST_ODIR)/%.o: %.c $(RST_DEPEND)
	$(CC) -c -o $@ $< $(CFLAGS) $(CFLAGS_EXTRA)

galileo_sketch_reset: $(RST_OBJ)
	$(CC) -o $@ $^ $(LDFLAGS) $(LIBS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~ *.d
	rm -f $(RST_ODIR)/*.o *~ core $(INCDIR)/*~ *.d
	${RM} $(GALILEO_TGT_LOADER) -f
	${RM} $(GALILEO_TGT_RESET_HANDLER) -f
	${RM} -r $(DESTDIR)

%.d: %.c
	@echo DEPEND $<; \
        rm -f $@; \
        $(CC) -MM $(CPPFLAGS) $(CFLAGS) $< > $@.$$$$; \
        sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $@.$$$$ > $@; \
        rm -f $@.$$$$

ifneq ($(MAKECMDGOALS), clean)
-include $(DEPEND)
endif

CLN_GALILEO := opt/cln/galileo

install: $(GALILEO_TGT_LOADER) $(GALILEO_TGT_RESET_HANDLER) install-scripts
	install -d $(DESTDIR)/${CLN_GALILEO}
	install -m 0755 $(GALILEO_TGT_LOADER) $(DESTDIR)/${CLN_GALILEO}
	install -m 0755 $(GALILEO_TGT_RESET_HANDLER) $(DESTDIR)/${CLN_GALILEO}

DESTDIR ?= build

install-scripts:
	install -d $(DESTDIR)/$(CLN_GALILEO)
	install -m 0755 scripts/${CLN_GALILEO}/* $(DESTDIR)/$(CLN_GALILEO)
