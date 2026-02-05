.POSIX:

all: run move_results


check:
	echo "Checking for required programs..."
	command -v python3 >/dev/null 2>&1 || { echo "Error: python3 not found."; exit 1; }
	command -v hw-probe >/dev/null 2>&1 || { echo "Error: hw-probe not found."; exit 1; }
	echo "All required programs are available."

probe:
	mkdir -p /tmp
	TMPDIR=$$(mktemp -d /tmp/hwprobe.XXXXXX)
	trap 'rm -rf "$$TMPDIR"' EXIT INT TERM
	echo "Temporary directory created."

	echo "Running probe, please supply your root password."
	su -m root -c "hw-probe -all -save $$TMPDIR"

	# Save the tmpdir path for later targets
	echo $$TMPDIR > .tmpdir

extract: probe
	TMPDIR=$$(cat .tmpdir)
	echo "Extracting hardware dump..."
	tar -xf $$TMPDIR/*.tgz -C $$TMPDIR
	echo "Extraction finished."

run: extract
	REPO_DIR=$$(pwd)
	TMPDIR=$$(cat .tmpdir)

	echo "Running script..."
	python main.py "$$TMPDIR"

#create new target to move
move_results:
	REPO_DIR=$$(pwd)
	TMPDIR=$$(cat .tmpdir)

	mkdir -p "$$REPO_DIR/test_results"
	if compgen -G "$$TMPDIR/*.txt" > /dev/null; then
		mv "$$TMPDIR"/*.txt "$$REPO_DIR/test_results/"
	else
		echo "Warning: No .txt files found to move."
	fi
	echo "Results moved to test_results"

clean:
	rm -f .tmpdir

.PHONY: all probe extract run move_results clean

