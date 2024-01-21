from aws_cdk import (
    Duration,
    Stack,
    CfnOutput,
    aws_lambda as lambda_,
    # aws_sqs as sqs,
)
from constructs import Construct


class DockerLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        dockerFunc = lambda_.DockerImageFunction(
            self, "docker_lambda",
            code=lambda_.DockerImageCode.from_image_asset("./image"),
            memory_size=1024,
            timeout=Duration.seconds(10),
            architecture=lambda_.Architecture.ARM_64,
        )

        functionUrl = dockerFunc.add_function_url(
            auth_type=lambda_.FunctionUrlAuthType.AWS_IAM,
            cors=lambda_.FunctionUrlCorsOptions(
                allowed_methods=[lambda_.HttpMethod.ALL],
                allowed_headers=['*'],
                allowed_origins=['*'],
            )
        )

        CfnOutput(self, "FunctionUrlOutput", value=functionUrl.url)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "DockerLambdaQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
