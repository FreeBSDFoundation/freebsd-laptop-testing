.POSIX:

all: run

run:
	@set -e; \
	\
	repodir=`pwd`; \
	echo "Repository directory: $$repodir"; \
	\
	echo "Checking for required applications..."; \
	command -v python >/dev/null 2>&1 || { echo "Error: python not found."; exit 1; }; \
	command -v hw-probe >/dev/null 2>&1 || { echo "Error: hw-probe not found."; exit 1; }; \
	echo "python and hw-probe are available."; \
	\
	tmpdir=`mktemp -d /tmp/hwprobe.XXXXXX` || exit 1; \
	trap 'rm -rf "$$tmpdir"' EXIT INT TERM; \
	echo "Created temp dir: $$tmpdir"; \
	\
	echo "Running probe. Please enter your root password."; \
	echo "============="; \
	su -m root -c "hw-probe -all -save $$tmpdir"; \
	echo "============="; \
	\
	echo "Extracting file"; \
	cd "$$tmpdir"; \
	tar -xf *.tgz; \
	\
	echo "Running script"; \
	python "$$repodir/main.py" "$$tmpdir"; \
	\
	echo "Creating test_results subdirectory"; \
	maker=`kenv | grep '^smbios.system.maker=' | cut -d'=' -f2 | tr -d '"' | tr '[:upper:]' '[:lower:]'`; \
	if [ -z "$$maker" ]; then \
		echo "Error: Could not determine system maker."; \
		exit 1; \
	fi; \
	target_dir="$$repodir/test_results/$$maker"; \
	mkdir -p "$$target_dir"; \
	echo "Moving generated file into $$target_dir"; \
	set -- "$$tmpdir"/*.txt; \
	if [ -e "$$1" ]; then \
		mv "$$@" "$$target_dir/"; \
	else \
		echo "Error: No .txt file generated."; \
		exit 1; \
	fi; \
	\
	echo "Finished. Thank you for your contribution!"
