module "public_subnet" {
  source = "github.com/terraform-community-modules/tf_aws_public_subnet"

  name   = "public-nat"
  cidrs  = [""]
  azs    = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
  vpc_id = "vpc-12345678"
  igw_id = "igw-12345678"

  tags {
      "Terraform" = "true"
      "Environment" = "${var.environment}"
  }
}
module "vpc" {
  source = "github.com/terraform-community-modules/tf_aws_vpc"

  name = "${var.environment}"

  cidr = "${lookup(var.cidr, var.environment)}"
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = "true"

  azs = ["${lookup(var.aws_az, var.az)}"]

  tags {
    "Terraform" = "true"
    "Environment" = "${var.environment}"
  }
}
