output "cluster_endpoint" {
  description = "Endpoint for EKS cluster"
  value       = aws_eks_cluster.forum_cluster.endpoint
}

output "cluster_name" {
  description = "Name of the EKS cluster"
  value       = aws_eks_cluster.forum_cluster.name
}

output "db_endpoint" {
  description = "Endpoint for RDS instance"
  value       = aws_db_instance.forum_db.endpoint
}

output "kubeconfig_command" {
  description = "Command to update kubeconfig to connect to cluster"
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${aws_eks_cluster.forum_cluster.name}"
}