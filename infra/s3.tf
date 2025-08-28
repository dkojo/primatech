resource "aws_s3_bucket" "avatars" {
  bucket        = var.bucket_name
  force_destroy = true
}

resource "aws_s3_bucket_policy" "avatars_policy" {
  bucket = aws_s3_bucket.avatars.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid    = "AllowAppRoleAccess",
        Effect = "Allow",
        Principal = {
          AWS = aws_iam_role.app_role.arn
        },
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:PutObjectAcl"
        ],
        Resource = "${aws_s3_bucket.avatars.arn}/*"
      }
    ]
  })
}

