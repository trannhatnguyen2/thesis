gcloud container clusters get-credentials thesis-sentiment-gke --zone us-central1-f --project mlops-416203
cd helm_charts/nginx_ingress/
kubectl create ns nginx-ingress
kubens nginx-ingress
helm upgrade --install nginx-ingress-controller .
cd ..
cd app/
kubectl create ns model-serving
kubens model-serving
helm upgrade --install app .
kubectl get ing