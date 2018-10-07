variable "region" {}
variable "subnet" {}
variable "key_id" {}
variable "access_key" {}
variable "logging_drivers" {}
variable "user" {}
variable "pwd" {}
variable "security_group" {}

provider "aws" {
  region = "${var.region}"
  profile = "iam-admin"
}

variable "ecs-cluster-name" {
  default = "dep-tf"
}

variable "app-container" {
  default = "dep:latest"
}

resource "aws_ecs_cluster" "main" {
  name = "dep-tf"
}

resource "aws_ecs_task_definition" "main_task" {
  family = "dep-tf"
  network_mode = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu = "256"
  memory = "512"
  task_role_arn = "arn:aws:iam::397678393215:role/ecsTaskExecutionRole"
  execution_role_arn = "arn:aws:iam::397678393215:role/ecsTaskExecutionRole"
  container_definitions = <<DEFINITION
[
  {
    "image": "dep:latest",
    "name": "dep",
    "networkMode": "awsvpc",
    "environment": [
      {"name": "user", "value": "${var.user}"},
      {"name": "pwd", "value": "${var.pwd}"},
      {"name": "AWS_ACCESS_KEY_ID", "value": "${var.key_id}"},
      {"name": "AWS_SECRET_ACCESS_KEY", "value": "${var.access_key}"},
      {"name": "AWS_DEFAULT_REGION", "value": "${var.region}"},
      {"name": "ECS_AVAILABLE_LOGGING_DRIVERS", "value": "[\"json-file\", \"awslogs\"]"}
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/dep-task-tf-definition",
        "awslogs-region": "${var.region}",
        "awslogs-stream-prefix": "ecs"
      }
    }
  }
]
DEFINITION
}


// ,
//    "logConfiguration": [
//      {"name": "awslogs-group", "value": "/ecs/dep-task-tf-definition"},
//      {"name": "awslogs-region", "value": "${var.region}"},
//      {"name": "awslogs-stream-prefix", "value": "ecs"}
//    ]

resource "aws_cloudwatch_event_rule" "dep-daily-tf" {
  name                = "DepDailyTF"
  description         = "run task nightly"
  schedule_expression = "cron(0 22 * * ? *)"
}

resource "aws_cloudwatch_event_target" "ecs_scheduled_task" {
  target_id = "run-dep-daily-tf"
  arn       = "${aws_ecs_cluster.main.arn}"
  rule      = "${aws_cloudwatch_event_rule.dep-daily-tf.name}"
  role_arn  = "arn:aws:iam::397678393215:role/ecsTaskExecutionRole"

  ecs_target = {
    task_count = 1
    launch_type = "FARGATE"
    task_definition_arn = "${aws_ecs_task_definition.main_task.arn}"
    network_configuration = {
      subnets = ["subnet-7db77421"]
      security_groups = ["sg-0e80c346"]
      assign_public_ip = "true"
    }
  }
}
