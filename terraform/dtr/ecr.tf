resource "aws_ecr_repository" "toolbox" {
    name = "toolbox"
}

resource "aws_ecr_repository" "bootstrap" {
    name = "bootstrap"
}

