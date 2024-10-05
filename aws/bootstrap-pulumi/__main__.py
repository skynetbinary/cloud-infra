import pulumi
import pulumi_aws as aws


project = pulumi.get_project()
stack = pulumi.get_stack()

stack_name = f"{project}-{stack}"


# This S3 bucket will hold the pulumi configuration.
bucket = aws.s3.Bucket(
    f"{project}-bucket",
    bucket="bootstrap-pulumi-abcdef",
    acl="private",
    force_destroy=False,
    server_side_encryption_configuration=aws.s3.BucketServerSideEncryptionConfigurationArgs(
        rule=aws.s3.BucketServerSideEncryptionConfigurationRuleArgs(
            apply_server_side_encryption_by_default=aws.s3.BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs(
                sse_algorithm="AES256",
            ),
        ),
    ),
    versioning=aws.s3.BucketVersioningArgs(
        enabled=True,
    ),
    opts=pulumi.ResourceOptions(protect=True),
)


# Exports.
pulumi.export("bucket-arn", bucket.arn)
