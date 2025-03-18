#!/bin/bash
cd /root/dtb
source venv/bin/activate
python daily_lhb_report.py
python plot_and_send.py
deactivate