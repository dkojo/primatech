data "aws_eks_cluster" "eks" {
  name = var.eks_cluster_name
}

data "aws_eks_cluster_auth" "eks" {
  name = var.eks_cluster_name
}

data "aws_iam_openid_connect_provider" "oidc" {
  arn = var.eks_oidc_provider_arn
}

resource "aws_iam_role" "app_role" {
  name = "prima-tech-challenge-cluster-app-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Federated = data.aws_iam_openid_connect_provider.oidc.arn
        },
        Action = "sts:AssumeRoleWithWebIdentity",
        Condition = {
          StringEquals = {
            "${replace(data.aws_iam_openid_connect_provider.oidc.url, "https://", "")}:sub" = "system:serviceaccount:default:app-sa"
          }
        }
      }
    ]
  })
}

resource "aws_iam_policy" "app_policy" {
  name = "eks-app-policy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid    = "S3FullAccessToAvatarBucket",
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:PutObjectAcl",
          "s3:DeleteObject",
          "s3:ListBucket"
        ],
        Resource = [
          aws_s3_bucket.avatars.arn,
          "${aws_s3_bucket.avatars.arn}/*"
        ]
      },
      {
        Sid    = "DynamoDBFullAccessToUsersTable",
        Effect = "Allow",
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Scan",
          "dynamodb:Query",
          "dynamodb:DescribeTable"
        ],
        Resource = aws_dynamodb_table.users.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_app_policy" {
  role       = aws_iam_role.app_role.name
  policy_arn = aws_iam_policy.app_policy.arn
}

resource "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}

# IAM Role for GitHub Actions
resource "aws_iam_role" "github_actions_role" {
  name = "github-actions-prima-api-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Federated = aws_iam_openid_connect_provider.github.arn
        },
        Action = "sts:AssumeRoleWithWebIdentity",
        Condition = {
          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:robertyawmegbenu/prima-tech-challenge:*"
          }
        }
      }
    ]
  })
}

resource "aws_iam_policy" "github_actions_policy" {
  name = "github-actions-prima-api-policy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      # Allow Terraform to manage infra
      {
        Sid: "TerraformManagement",
        Effect: "Allow",
        Action: [
          "s3:*",
          "dynamodb:*",
          "iam:*",
          "ecr:*",
          "eks:*",
          "cloudwatch:*",
          "logs:*"
        ],
        Resource: "*"
      },
      {
        Sid: "ECRAuth",
        Effect: "Allow",
        Action: [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:CompleteLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:InitiateLayerUpload",
          "ecr:PutImage",
          "ecr:BatchGetImage"
        ],
        Resource: "*"
      },
      {
        Sid: "EKSAccess",
        Effect: "Allow",
        Action: [
          "eks:DescribeCluster",
          "eks:ListClusters"
        ],
        Resource: "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_github_actions_policy" {
  role       = aws_iam_role.github_actions_role.name
  policy_arn = aws_iam_policy.github_actions_policy.arn
}

