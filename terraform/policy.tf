resource "aws_iam_policy" "base_instance_policy" {
    name = "base_instance_policy"
    description = "update dns, set tags, pull from ecr"
    policy = "${file("policies/base-instance-policy.json")}"
}
