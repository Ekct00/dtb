#!/bin/bash
cd /root/dtb
. venv/bin/activate
export PYTHONIOENCODING=utf8
python3 daily_lhb_report.py
. deactivate