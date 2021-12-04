locals {
    ports_in = [
        3000,
        8000,
        80,
        22
    ]
    ports_out = [
        0
    ]
}

resource "aws_security_group" "allow-ssh" {
    name = "allow-all-sg"
    vpc_id = "${aws_vpc.demo-env.id}"
    dynamic "ingress" {
        for_each = toset(local.ports_in)
        content {
            description = "HTTP from VPC"
            from_port   = ingress.value
            to_port     = ingress.value
            protocol    = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
        }
    }

    dynamic "egress" {
        for_each = toset(local.ports_out)
        content {
            from_port   = egress.value
            to_port     = egress.value
            protocol    = "-1"
            cidr_blocks = ["0.0.0.0/0"]
        }
    }
}
