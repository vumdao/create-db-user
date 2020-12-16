#!/usr/bin/env python3

from aws_cdk import core

from sqs_stack.sqs_stack_stack import SqsStackStack


app = core.App()
core_env = core.Environment(region='ap-northeast-1')
SqsStackStack(app, "sqs-stack", env=core_env)

app.synth()
