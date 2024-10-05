import pulumi
import pulumi_aws as aws


project = pulumi.get_project()
stack = pulumi.get_stack()

stack_name = f"{project}-{stack}"

config = pulumi.Config()

aws_account_id = config.require("aws-account-id")
instance_arn = config.require("instance-arn")
identity_store_id = config.require("identitystore-id")
admin_users: list[dict] = config.require_object("admin-users")


permission_set_admin = aws.ssoadmin.PermissionSet(
    f"{project}-permission-set-admin",
    name="admin",
    description="Provides administrator access to the AWS account.",
    instance_arn=instance_arn,
    relay_state="https://us-west-2.console.aws.amazon.com/",
    # The session duration is set to expire in an hour.
    session_duration="PT1H",
)

permission_set_policy_admin = aws.ssoadmin.ManagedPolicyAttachment(
    f"{project}-permission-set-policy-admin",
    instance_arn=instance_arn,
    managed_policy_arn="arn:aws:iam::aws:policy/AdministratorAccess",
    permission_set_arn=permission_set_admin.arn,
)

group_admin = aws.identitystore.Group(
    f"{project}-group-admin",
    display_name="group-admin",
    description="Provides administrator access to the AWS account.",
    identity_store_id=identity_store_id,
)

account_assignment_group_admin = aws.ssoadmin.AccountAssignment(
    f"{project}-account-assignment-group-admin",
    instance_arn=instance_arn,
    permission_set_arn=permission_set_admin.arn,
    principal_id=group_admin.group_id,
    principal_type="GROUP",
    target_id=aws_account_id,
    target_type="AWS_ACCOUNT",
)


for uid, user in enumerate(admin_users, 1):
    member = aws.identitystore.User(
        f"{project}-admin-user-{uid}",
        identity_store_id=identity_store_id,
        display_name=f"{user['first_name']} {user['last_name']}",
        user_name=user["first_name"].lower(),
        name={
            "given_name": user["first_name"],
            "family_name": user["last_name"],
        },
        emails={
            "value": user["email"],
        },
    )

    aws.identitystore.GroupMembership(
        f"{project}-admin-user-membership-{uid}",
        identity_store_id=identity_store_id,
        group_id=group_admin.group_id,
        member_id=member.user_id,
    )


# Exports.
pulumi.export("instance-arn", instance_arn)
pulumi.export("identity-center-store-id", identity_store_id)
