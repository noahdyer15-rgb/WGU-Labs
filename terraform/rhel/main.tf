terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}

resource "aws_key_pair" "d417_key" {
  key_name   = "d417-rhel-key"
  public_key = file("/home/student/.ssh/d417key.pub")
}

resource "aws_security_group" "ssh_allow" {
  name        = "d417-rhel-ssh"
  description = "Allow SSH access"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "rhel_server" {
  ami                         = "ami-026fc9b0dc11499dc"
  instance_type               = "t2.micro"
  key_name                    = aws_key_pair.d417_key.key_name
  vpc_security_group_ids      = [aws_security_group.ssh_allow.id]
  associate_public_ip_address = true

  tags = {
    Name = "D417-RHEL-10"
  }
}