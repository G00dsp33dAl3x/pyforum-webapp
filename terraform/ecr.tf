# ecr.tf
resource "aws_ecr_repository" "forum_app" {
  name                 = "${var.project_name}"
  image_tag_mutability = "MUTABLE"
  force_delete         = false  # Set to true if you want to delete the repository even if it contains images

  image_scanning_configuration {
    scan_on_push = true  # Automatically scan Docker images for vulnerabilities
  }

  encryption_configuration {
    encryption_type = "AES256"  # Default encryption using AWS managed keys
  }

  tags = {
    Name        = "${var.project_name}-ecr"
    Environment = "production"
  }
}

resource "aws_ecr_lifecycle_policy" "forum_app_policy" {
  repository = aws_ecr_repository.forum_app.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "Keep only the last 10 images",
        selection = {
          tagStatus     = "any",
          countType     = "imageCountMoreThan",
          countNumber   = 10
        },
        action = {
          type = "expire"
        }
      }
    ]
  })
}

# IAM policy to allow EKS nodes to pull images from ECR
resource "aws_iam_policy" "ecr_access_policy" {
  name        = "${var.project_name}-ecr-access-policy"
  description = "Policy to allow pulling images from ECR"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetAuthorizationToken"
        ],
        Resource = "*"
      }
    ]
  })
}

# Attach the ECR access policy to the EKS node role
resource "aws_iam_role_policy_attachment" "ecr_access_attachment" {
  policy_arn = aws_iam_policy.ecr_access_policy.arn
  role       = aws_iam_role.eks_node_role.name
}

# Output the ECR repository URL
output "ecr_repository_url" {
  description = "URL of the ECR repository"
  value       = aws_ecr_repository.forum_app.repository_url
}

# Add the following commands to the outputs.tf for easier Docker image pushing
output "ecr_login_command" {
  description = "Command to authenticate Docker to the ECR repository"
  value       = "aws ecr get-login-password --region ${var.aws_region} | docker login --username AWS --password-stdin ${aws_ecr_repository.forum_app.repository_url}"
}

output "docker_build_command" {
  description = "Command to build the Docker image"
  value       = "docker build -t ${aws_ecr_repository.forum_app.repository_url}:latest ."
}

output "docker_push_command" {
  description = "Command to push the Docker image to ECR"
  value       = "docker push ${aws_ecr_repository.forum_app.repository_url}:latest"
}