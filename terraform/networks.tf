resource "aws_vpc" "demo-env" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "demo-env"
  }
}