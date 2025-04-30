#!/bin/bash
echo "=== chronyc tracking ==="
chronyc tracking
echo
echo "=== chronyc sourcestats ==="
chronyc sourcestats
echo
echo "=== ptp4l status ==="
pgrep ptp4l && echo "ptp4l running" || echo "ptp4l not running"
