provider "aws" {
    region = "${var.aws_region}"
}
variable "environment" {
    default = "dev"
}
variable "aws_region" {
    default = "us-east-1"
}
variable "az" {
    default = "a"
}
variable "aws_az" {
    type = "map"
    default {
        a = "us-east-1a"
        b = "us-east-1b"
    }
}
variable "cidr" {
    type = "map"
    default {
        dev = "10.0.0.0/16"
        prod = "10.1.0.0/16"
    }
}
variable "ami" {
    type = "map"
    default {
        us-east-1 = "ami-3b7f9e2d"
        us-east-2 = "ami-e66d4883"
    }
}
