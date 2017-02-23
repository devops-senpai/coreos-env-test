resource "aws_subnet" "pub" {
  vpc_id     = "${aws_vpc.main.id}"
  cidr_block = "10.0.0.0/24"

  tags {
    Name = "Public Subnet"
  }
}

resource "aws_subnet" "priv" {
  vpc_id     = "${aws_vpc.main.id}"
  cidr_block = "10.0.1.0/24"

  tags {
    Name = "Private Subnet"
  }
}

resource "aws_subnet" "pub_natgw" {
  vpc_id     = "${aws_vpc.main.id}"
  cidr_block = "10.0.255.240/28"

  tags {
    Name = "Nat GW Subnet"
  }
}

resource "aws_subnet" "priv_etcd" {
  vpc_id     = "${aws_vpc.main.id}"
  cidr_block = "10.0.255.224/28"

  tags {
    Name = "Private ETCD Subnet"
  }
}
