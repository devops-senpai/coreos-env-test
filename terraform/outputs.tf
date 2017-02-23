data "aws_caller_identity" "current" {
  # no arguments
}

output "aws_account_id" {
  value = "${data.aws_caller_identity.current.account_id}"
}

output "vpc_id" {
    value = "${aws_vpc.main.id}"
}
