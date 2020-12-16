from aws_cdk import (
    core,
    aws_sqs as sqs
)


class SqsStackStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, env, **kwargs) -> None:
        super().__init__(scope, construct_id, env=env, **kwargs)

        core_tag = core.Tags.of(self)
        create_db_sqs = sqs.Queue(scope=self, id='CreateDBUserSQS', queue_name='create-db-account',
                                  visibility_timeout=core.Duration.seconds(60))
        core_tag.add(
            key='cfn.aws-sqs.stack',
            value='create-db-user-sqs'
        )
