#!/bin/bash
cd /root/dtb
source venv/bin/activate
python daily_lhb_report.py
deactivate