


─────────────────────────────────────────────────────────────
│                                                             │
│  ┌─────────────────┐    ┌─────────────────────────────────┐ │
│  │   Terraform     │    │        GKE Cluster              │ │
│  │                 │    │                                 │ │
│  │  - main.tf      │────│  ┌─────────────────────────────┐│ │
│  │  - variables.tf │    │  │     Kubernetes Namespace    ││ │
│  │  - outputs.tf   │    │  │                             ││ │
│  └─────────────────┘    │  │  ┌─────────────────────┐    ││ │
│                         │  │  │   Deployment        │    ││ │
│  ┌─────────────────┐    │  │  │                     │    ││ │
│  │   Container     │    │  │  │  ┌───────────────┐  │    ││ │
│  │   Registry      │    │  │  │  │     Pod       │  │    ││ │
│  │                 │    │  │  │  │               │  │    ││ │
│  │  - web-app:1.0  │◄───┼──┼──┼──│  - Flask App  │  │    ││ │
│  └─────────────────┘    │  │  │  │  - Gunicorn   │  │    ││ │
│                         │  │  │  └───────────────┘  │    ││ │
│                         │  │  │                     │    ││ │
│                         │  │  │  ┌───────────────┐  │    ││ │
│                         │  │  │  │     Pod       │  │    ││ │
│                         │  │  │  │               │  │    ││ │
│                         │  │  │  │  - Flask App  │  │    ││ │
│                         │  │  │  │  - Gunicorn   │  │    ││ │
│                         │  │  │  └───────────────┘  │    ││ │
│                         │  │  └─────────────────────┘    ││ │
│                         │  │                             ││ │
│                         │  │  ┌─────────────────────┐    ││ │
│                         │  │  │   HPA Controller    │    ││ │
│                         │  │  │                     │    ││ │
│                         │  │  │ - Min Pods: 1       │    ││ │
│                         │  │  │ - Max Pods: 3       │    ││ │
│                         │  │  │ - CPU Target: 50%   │    ││ │
│                         │  │  └─────────────────────┘    ││ │
│                         │  │                             ││ │
│                         │  │  ┌─────────────────────┐    ││ │
│                         │  │  │   LoadBalancer      │    ││ │
│                         │  │  │      Service        │    ││ │
│                         │  │  │                     │    ││ │
│  External Traffic ──────┼──┼──│  - External IP      │    ││ │
│                         │  │  └─────────────────────┘    ││ │
│                         │  └─────────────────────────────┘│ │
│                         └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

Components Interaction:
1. Terraform provisions GKE cluster and infrastructure
2. Docker image is built and pushed to Container Registry
3. Helm deploys application with HPA configuration
4. LoadBalancer Service exposes application externally
5. HPA monitors CPU and scales pods between 1-3 based on 50% threshold
6. Load testing generates traffic to trigger autoscaling