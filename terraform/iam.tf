resource "aws_iam_instance_profile" "base_instance_role" {
  name  = "base_instance_role"
  roles = ["${aws_iam_role.base_role.name}"]
}

resource "aws_iam_role" "base_role" {
  name               = "base_instance_role"
  assume_role_policy = "${file("policies/role.json")}"
}

resource "aws_iam_policy" "base_policy" {
  name        = "base_instance_policy"
  description = "view/edit tags, pull from ecr, update dns"
  policy      = "${file("policies/base-instance-policy.json")}"
}

resource "aws_iam_role_policy_attachment" "base-attach" {
  role       = "${aws_iam_role.base_role.name}"
  policy_arn = "${aws_iam_policy.base_policy.arn}"
}
