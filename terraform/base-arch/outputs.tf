data "aws_caller_identity" "current" {
  # no arguments
}

output "aws_account_id" {
  value = "${data.aws_caller_identity.current.account_id}"
}

output "vpc_id" {
    value = "${aws_vpc.main.id}"
}
output "subnet_pub" {
    value = "${aws_subnet.pub.id}"
}
output "subnet_priv" {
    value = "${aws_subnet.priv.id}"
}
output "subnet_pub_natgw" {
    value = "${aws_subnet.pub_natgw.id}"
}
output "subnet_priv_etcd" {
    value = "${aws_subnet.priv_etcd.id}"
}

