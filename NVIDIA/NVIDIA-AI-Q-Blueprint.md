Kubernetes (Helm)
Deploy the AI-Q blueprint to a Kubernetes cluster using the Helm charts included in the repository.

Prerequisites
Kubernetes cluster (EKS, GKE, AKS, or a local cluster such as Kind or Minikube).

kubectl configured with cluster access.

[helm v3.x installed](https://docs.nvidia.com/aiq-blueprint/2.2.0-rc1/deployment/kubernetes.html)

API keys for the models and tools you plan to use (refer to Installation – API Key Setup).

```
kubectl create namespace ns-aiq --dry-run=client -o yaml | kubectl apply -f -

```

```
kubectl create secret generic aiq-credentials -n ns-aiq \
  --from-literal=NVIDIA_API_KEY="$NGC_API_KEY" \
  --from-literal=TAVILY_API_KEY="$TAVILY_API_KEY" \
  --from-literal=DB_USER_NAME="aiq" \
  --from-literal=DB_USER_PASSWORD="aiq_dev"
```

