variable "AWS_REGION" {
  default = "ap-southeast-1"
}

variable "environment" {
    default = "qa"
}

locals {
  tags = {
      Environment = var.environment
      Email = "phampham01228@gmail.com"
  }
}
