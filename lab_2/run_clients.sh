#!/bin/bash
echo "Running Client A..."
python client_a.py
sleep 1  # Wait for 1 second between executions
echo "Running Client B..."
python client_b.py
