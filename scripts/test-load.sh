#!/bin/bash

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <BASE_URL>"
    exit 1
fi

BASE_URL=$1

echo "Starting load test on $BASE_URL"
echo "Monitoring HPA..."

# Start monitoring HPA in background
kubectl get hpa web-app-hpa -w &
HPA_PID=$!

# Run load test
python3 ./app/stress-test.py $BASE_URL 120

# Stop monitoring
kill $HPA_PID

echo "Load test completed. Check HPA status with: kubectl get hpa"