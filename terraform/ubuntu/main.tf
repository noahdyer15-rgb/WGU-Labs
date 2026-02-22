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
  key_name   = "d417-ubuntu-key"
  public_key = file("/home/student/.ssh/d417key.pub")
}

resource "aws_security_group" "ssh_allow" {
  name        = "d417-ubuntu-ssh"
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

resource "aws_instance" "ubuntu_server" {
  ami                         = "ami-0786adace1541ca80"
  instance_type               = "t2.micro"
  key_name                    = aws_key_pair.d417_key.key_name
  vpc_security_group_ids      = [aws_security_group.ssh_allow.id]
  associate_public_ip_address = true

  tags = {
    Name = "D417-Ubuntu-24"
  }
}