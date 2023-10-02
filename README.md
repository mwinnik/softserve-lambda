Lambda trigger

![image](https://github.com/mwinnik/softserve-lambda/assets/86104714/ef9d94ae-f52f-4942-956d-c685d94f8bea)

![image](https://github.com/mwinnik/softserve-lambda/assets/86104714/c186750c-a18b-45d7-b5a9-8b4e70c9d340)


Environment variables

![image](https://github.com/mwinnik/softserve-lambda/assets/86104714/d0899613-81e1-4d2a-9615-2d0709984033)

Lambda policy

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeVolumes",
                "ec2:DescribeSnapshots"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::softserve-chat-gpt-mw/*"
            ]
        }
    ]
}
```

Bucket policy 

```
{
    "Version": "2012-10-17",
    "Id": "PolicyForLambdaAndRole",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::11111111111:role/aws_lambda_ebs_verifier"
            },
            "Action": "s3:PutObject",
            "Resource": [
                "arn:aws:s3:::softserve-chat-gpt-mw/*",
                "arn:aws:s3:::softserve-chat-gpt-mw"
            ]
        },
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::11111111111:role/AWS-aws102464-Admin"
            },
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::softserve-chat-gpt-mw/*",
                "arn:aws:s3:::softserve-chat-gpt-mw"
            ]
        }
    ]
}
```
Bucket lifecycle policy

![image](https://github.com/mwinnik/softserve-lambda/assets/86104714/c190e90b-aa14-4100-9e8b-cbac317176f2)

Buket encryption with SSE-S3

![image](https://github.com/mwinnik/softserve-lambda/assets/86104714/4e59e2bd-9878-42ba-ab61-9afbb762dc41)

