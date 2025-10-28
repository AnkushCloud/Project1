

Components Interaction:
1. Terraform provisions GKE cluster and infrastructure
2. Docker image is built and pushed to Container Registry
3. Helm deploys application with HPA configuration
4. LoadBalancer Service exposes application externally
5. HPA monitors CPU and scales pods between 1-3 based on 50% threshold
6. Load testing generates traffic to trigger autoscaling