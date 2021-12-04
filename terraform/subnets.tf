resource "aws_subnet" "demo-subnet" {
  cidr_block = "${cidrsubnet(aws_vpc.demo-env.cidr_block, 3, 1)}"
  vpc_id = "${aws_vpc.demo-env.id}"
  availability_zone = "us-east-2a"
}

resource "aws_route_table" "route-table-demo-env" {
    vpc_id = "${aws_vpc.demo-env.id}"
    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = "${aws_internet_gateway.demo-gw.id}"
    }
    tags = {
        Name = "route-table-demo-env"
    }
}
resource "aws_route_table_association" "subnet-association" {
  subnet_id      = "${aws_subnet.demo-subnet.id}"
  route_table_id = "${aws_route_table.route-table-demo-env.id}"
}
