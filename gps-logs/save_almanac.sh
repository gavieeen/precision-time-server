#!/bin/bash
timestamp=$(date +%Y%m%d%H%M%S)
gpspipe -w -n 20 > ~/almanac_$timestamp.json
