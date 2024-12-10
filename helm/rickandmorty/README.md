## Helm Chart Structure
```
helm/
  rickandmorty/
    Chart.yaml
    values.yaml
    templates/
      _helpers.tpl
      deployment.yaml
      service.yaml
      ingress.yaml
```

## How to Run
1. **Ensure you have Helm installed** and a Kubernetes cluster context configured (e.g., `kubectl get nodes` works).

2. **Navigate to the chart directory**:
   ```bash
   cd helm/rickandmorty
   ```

3. **Install the chart**:
   ```bash
   helm install rickandmorty .
   ```
   This command installs the chart with the release name `rickandmorty`. It will:
   - Create a Deployment with 2 replicas.
   - Create a LoadBalancer Service.
   - Create an Ingress resource if ingress is enabled.

<img width="1385" alt="image" src="https://github.com/user-attachments/assets/e31ee056-db2c-4583-902f-ebb4a10323f1">


4. **Check the resources**:
   ```bash
   kubectl get deployments
   kubectl get svc
   kubectl get ingress
   ```

5. **Access the Application**:
   - If you have a LoadBalancer and it provides an external IP, run:
     ```bash
     kubectl get svc
     ```
     Suppose it shows an external IP for `rickandmorty-rickandmorty`. Curl the `/healthcheck`:
     ```bash
     curl http://<EXTERNAL_IP>/healthcheck
     ```

   - For the Ingress, ensure `rickandmorty.local` resolves to the ingress controller’s IP. For example, add an entry to `/etc/hosts`:
     ```bash
     echo "<INGRESS_IP> rickandmorty.local" | sudo tee -a /etc/hosts
     ```
     Then:
     ```bash
     curl http://rickandmorty.local/healthcheck
     curl http://rickandmorty.local/characters
     ```
   
   You should see the JSON responses from the application.
<img width="1397" alt="image" src="https://github.com/user-attachments/assets/564607cf-1bd5-4fe1-b0c3-e0ac43a56a32">


**Note:**  
- If you don’t have a LoadBalancer (e.g., running in a local environment without MetalLB or cloud LB), you might want to set `service.type` to `NodePort` and access via the node’s IP and nodePort.
- Make sure `ingress.className` matches the installed Ingress Controller. For NGINX ingress, `nginx` is correct. If you’re using another controller, adjust accordingly.
