data "aws_ami" "ubuntu20" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "bts" {
  ami             = data.aws_ami.ubuntu20.id
  instance_type   = "t2.micro"
  key_name        = "${var.ami_key_pair_name}"
  security_groups = ["${aws_security_group.allow-ssh.id}"]
  associate_public_ip_address = true
  tags = {
    Name = "demo"
  }

  subnet_id = "${aws_subnet.demo-subnet.id}"
}
