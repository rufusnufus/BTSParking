
resource "aws_internet_gateway" "demo-gw" {
  vpc_id = "${aws_vpc.demo-env.id}"
    tags = {
        Name = "demo-gw"
    }
}