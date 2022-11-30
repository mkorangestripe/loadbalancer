provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "loadbalancer-app2" {
  cidr_block = var.vpc_cidr_block
  enable_dns_support = true
  enable_dns_hostnames = true

    tags = {
    Name = "ECS loadbalancer-app2 - VPC"
  }
}

resource "aws_subnet" "loadbalancer-app2" {
  vpc_id     = aws_vpc.loadbalancer-app2.id
  cidr_block = "10.0.0.0/24"
  availability_zone = var.aws_availability_zone
    tags = {
    Name = "ECS loadbalancer-app2 - Public Subnet"
  }
}

resource "aws_route_table" "loadbalancer-app2" {
  vpc_id = aws_vpc.loadbalancer-app2.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.loadbalancer-app2.id
  }
    tags = {
    Name = "ECS loadbalancer-app2 - RouteTable"
  }
}

resource "aws_route_table_association" "loadbalancer-app2" {
  subnet_id = aws_subnet.loadbalancer-app2.id
  route_table_id = aws_route_table.loadbalancer-app2.id
}

resource "aws_internet_gateway" "loadbalancer-app2" {
  vpc_id = aws_vpc.loadbalancer-app2.id

    tags = {
      Name = "ECS loadbalancer-app2 - InternetGateway"
    }
  }

resource "aws_ecs_cluster" "loadbalancer-app2" {
  name = "loadbalancer-app2"
}

resource "aws_ecs_task_definition" "loadbalancer-app2" {
  family                   = "loadbalancer-app2" # unique name for the task definition
  container_definitions    = data.template_file.task_definition_template.rendered
  requires_compatibilities = ["FARGATE"] # Stating that we are using ECS Fargate
  network_mode             = "awsvpc"    # Using awsvpc as our network mode as this is required for Fargate
  memory                   = 512         # Specifying the memory our container requires
  cpu                      = 256         # Specifying the CPU our container requires
  execution_role_arn       = aws_iam_role.ecsTaskExecutionRole2.arn
}

resource "aws_cloudwatch_log_group" "loadbalancer-app2" {
  name = var.aws_cloudwatch_log_group
}

resource "aws_iam_role" "ecsTaskExecutionRole2" {
  name               = "ecsTaskExecutionRole2"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
  role       = aws_iam_role.ecsTaskExecutionRole2.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_security_group" "loadbalancer-app2-security-group" {
  name       = "ECS loadbalancer-app2 - ECS SecurityGroup"
  vpc_id     = aws_vpc.loadbalancer-app2.id
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port    = 443
    to_port      = 443
    protocol     = "tcp"
    cidr_blocks  = ["0.0.0.0/0"]
}

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ecs_service" "loadbalancer-app2" {
  name            = "loadbalancer-app2"                              # service name
  cluster         = aws_ecs_cluster.loadbalancer-app2.id             # referencing the created cluster
  task_definition = aws_ecs_task_definition.loadbalancer-app2.arn    # referencing the task the service will start
  launch_type     = "FARGATE"
  desired_count   = 1 # the number of containers to deploy

  network_configuration {
    subnets          = [aws_subnet.loadbalancer-app2.id]
    assign_public_ip = true # Providing our containers with public IPs
    security_groups  = [aws_security_group.loadbalancer-app2-security-group.id] # Setting the security group
  }
}
