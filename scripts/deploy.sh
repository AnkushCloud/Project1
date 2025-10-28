#!/bin/bash

set -e

echo "Starting deployment..."

# Build and push Docker image
echo "Building Docker image..."
docker build -t your-docker-repo/web-app:1.0 ./app
docker push your-docker-repo/web-app:1.0

# Initialize and apply Terraform
echo "Applying Terraform configuration..."
cd terraform
terraform init
terraform apply -auto-approve

# Get the external IP
EXTERNAL_IP=$(kubectl get service web-app-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo "Deployment completed!"
echo "Application is available at: http://$EXTERNAL_IP"
echo "To test autoscaling, run: ./scripts/test-load.sh http://$EXTERNAL_IP"