#!/bin/bash
cd /home/cfarancho/DepartureTimeSensor || exit
git fetch origin main
if ! git diff --quiet origin/main; then
    echo "New changes detected, pulling..."
    git pull origin main
    cd /home/cfarancho/DepartureTimeSensor
    launcher.sh
else
    echo "no changes found."
finish