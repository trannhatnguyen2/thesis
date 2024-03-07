variable "project_id" {
  description = "The project ID to host the cluster in"
  default     = "mlops-416203"
}

variable "region" {
  description = "The region the cluster in"
  default     = "us-central1-f"
}

variable "k8s" {
  description = "GKE for thesis_sentiment"
  default     = "thesis-sentiment"
}