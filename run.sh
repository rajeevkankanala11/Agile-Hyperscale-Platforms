#!/usr/bin/env bash
# Reproduce all synthesised tables and Figure 4 from published inputs.
set -e
cd "$(dirname "$0")/src"
python3 compute_metrics.py
python3 make_tables.py
python3 make_figure4.py
echo "Done. See ../outputs/"
