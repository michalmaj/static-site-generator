# #!/usr/bin/env bash
# set -euo pipefail

# python3 src/main.py
# cd public && python3 -m http.server 8888


#!/usr/bin/env bash
set -euo pipefail

# Lokalnie: domyślny basepath "/", build do docs/
python3 src/main.py
echo "[serve] http://localhost:8888"
cd docs && python3 -m http.server 8888