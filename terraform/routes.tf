resource "aws_internet_gateway" "gw" {
    vpc_id = "${aws_vpc.main.id}"

    tags {
        Name = "public_igw"
    }
}
resource "aws_network_interface" "natgw" {
    subnet_id = "${aws_subnet.pub_natgw.id}"
}
resource "aws_eip" "natgw" {
  vpc      = true
}
resource "aws_nat_gateway" "gw" {
    allocation_id = "${aws_eip.natgw.id}"
    subnet_id = "${aws_subnet.pub_natgw.id}"
    depends_on = ["aws_eip.natgw", "aws_internet_gateway.gw"]
}
resource "aws_route_table" "pub" {
    vpc_id = "${aws_vpc.main.id}"
    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = "${aws_internet_gateway.gw.id}"
    }
    tags {
        Name = "public"
    }
}
resource "aws_route" "igw" {
    route_table_id = "${aws_route_table.pub.id}"
    destination_cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.gw.id}"
}
resource "aws_route_table_association" "pub" {
    subnet_id = "${aws_subnet.pub.id}"
    route_table_id = "${aws_route_table.pub.id}"
}
resource "aws_route_table_association" "pub_natgw" {
    subnet_id = "${aws_subnet.pub_natgw.id}"
    route_table_id = "${aws_route_table.pub.id}"
}


resource "aws_route_table" "priv" {
    vpc_id = "${aws_vpc.main.id}"
    route {
        cidr_block = "0.0.0.0/0"
        nat_gateway_id = "${aws_nat_gateway.gw.id}"
    }
    tags {
        Name = "main_private"
    }
}
#resource "aws_route" "nat" {
#    route_table_id = "${aws_route_table.priv.id}"
#    destination_cidr_block = "0.0.0.0/0"
#    nat_gateway_id  = "${aws_nat_gateway.gw.id}"
#}
resource "aws_route_table_association" "priv" {
    subnet_id = "${aws_subnet.priv.id}"
    route_table_id = "${aws_route_table.priv.id}"
}
resource "aws_route_table_association" "priv_etcd" {
    subnet_id = "${aws_subnet.priv_etcd.id}"
    route_table_id = "${aws_route_table.priv.id}"
}
resource "aws_main_route_table_association" "main" {
    vpc_id = "${aws_vpc.main.id}"
    route_table_id = "${aws_route_table.priv.id}"
}
