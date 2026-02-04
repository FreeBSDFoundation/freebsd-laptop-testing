.POSIX:

PYTHON    = python3
SCRIPT    = main.py
DUMP_FILE = hw-.info.tgz
HWPROBE   = hw-probe
USER_ID   = $$(id -u -n)
GROUP_ID  = $$(id -g -n)

all: run

check:
	@echo "Checking system for required applications"
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo "Error: $(PYTHON) not found."; exit 1; }
	@command -v $(HWPROBE) >/dev/null 2>&1 || { echo "Error: $(HWPROBE) is not installed."; exit 1;}
	@echo "$(PYTHON) and $(HWPROBE) are available."

probe:
	@echo "Running probe for $(USER_ID)..."
	@echo "============="
	t=$$(mktemp -d); \
	su -m root -c "hw-probe -all -save $$t"; \
	cp -R $$t/*.tgz ./; \

	@echo "============="


run: extract
	@echo "Running $(SCRIPT)..."
	$(PYTHON) $(SCRIPT)

extract: probe
	@echo "Extracting hardware dump..."
	tar -xf *.tgz
	@echo "Finished. Thank you for your contribution!"
	rm -rf $$t
.PHONY: all probe extract run


