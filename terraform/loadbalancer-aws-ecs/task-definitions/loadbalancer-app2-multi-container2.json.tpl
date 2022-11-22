[
    {
    "name": "cat-loadbalancer",
    "image": "mkorangestripe/loadbalancer:2.0.0",
    "command": ["gunicorn -b 0.0.0.0:80 load_balancer:app"],
    "entryPoint": ["sh", "-c"],
    "essential": true,
    "portMappings": [
      {
        "containerPort": 80,
        "hostPort": 80
      }
    ],
    "memory": 256,
    "links": [
        "cheetah"
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "${AWS_CLOUDWATCH_LOG_GROUP}",
        "awslogs-region": "${AWS_REGION}",
        "awslogs-stream-prefix": "ecs"
      }
    }
  },
  {
    "name": "cheetah",
    "hostname": "cheetah",
    "image": "nginxdemos/hello:0.2",
    "essential": true,
    "memory": 256,
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "${AWS_CLOUDWATCH_LOG_GROUP}",
        "awslogs-region": "${AWS_REGION}",
        "awslogs-stream-prefix": "ecs"
      }
    }
  }
]