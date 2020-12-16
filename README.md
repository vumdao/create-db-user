Use slackbot to send SQS message which trigger lambda function for executing SQL command on database

![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/58gluaj6ycqa9b5riuid.png)

This post focuses on creating SQS queue and lambda function (not how to create a slackbot)

###**1. Create SQS queue using CDK (Cloud Development Toolkit)**
####Source: https://github.com/vumdao/create-db-user/tree/master/sqs_stack
####Notes:
- SQS name: create-db-account
- SQS Default visibility timeout must be equal or higher than the timeout of the lambda function which is subscribed to
- Deploy SQS
```
cdk deploy
```
![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/l8gf78jfpxq36cqd7u2n.png)

###**2. Create Lambda function which is triggered by the SQS queue using AWS Chalice**
####Source: https://github.com/vumdao/create-db-user/tree/master/lambda

####The lambda function receive SQS message to execute SQL of creating new user on RDS
```
chalice new-project create-db-user
```

####Set VPC for Lambda Function same with RDS, AWS Chalice bases on current region and the subnet ID to detect VPC, security is a must for using subnet-ID 
```
      "subnet_ids": [
         "subnet-0f6ea4292ab9a63db",
         "subnet-00d29b42b2e17b5b5"
      ],
      "security_group_ids": ["sg-00668399e4bdd462e"]
```
####Disable mange IAM role from AWS Chalice to control the policy of the role
```
      "manage_iam_role": false,
      "iam_role_arn": "arn:aws:iam::111111111111:role/create-db-user-dev",
```

####Policy
```
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:*:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "sqs:ReceiveMessage",
                "sqs:DeleteMessage",
                "sqs:GetQueueAttributes"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeNetworkInterfaces",
                "ec2:CreateNetworkInterface",
                "ec2:DeleteNetworkInterface",
                "ec2:DescribeInstances",
                "ec2:AttachNetworkInterface"
            ],
            "Resource": "*"
        }
    ]
}           
```

####Lambda does not resolve hostname directly so RDS hostname is resolved by using socket function
```
host=socket.gethostbyname(DB_HOST)
```

####Deploy the lambda
```
chalice deploy
```
![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/frkdv23mrbk4yo9u9f2q.png)

![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/4ujta923rvpuzpuvx1mi.png)

![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/0s9wc1i76gm0eo9zglln.png)

###Test
![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/1zj36ynfjncnjybnccp4.png)

Ref: https://dev.to/vumdao/connect-postgres-database-using-lambda-function-1mca
