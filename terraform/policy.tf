resource "aws_iam_policy" "base_instance_policy" {
    name = "base_instance_policy"
    description = "My test policy"
    policy = ${file("policies/base-instance-policy.json")}
}
