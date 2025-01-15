from cdktf import TerraformStack, TerraformVariable, TerraformHclModule, S3Backend
from constructs import Construct
from nitric.proto.deployments.v1 import (
    DeploymentUpRequest,
)
from nitric.utils import dict_from_struct
from cdktf_cdktf_provider_aws import provider as aws_provider


class DynamicTerraformStack(TerraformStack):
    """Terraform Dynamic Stack"""

    def __init__(self, scope: Construct, id: str, req: DeploymentUpRequest):
        super().__init__(scope, id)

        attributes = dict_from_struct(req.attributes)
        # retrieve region property with a default value (note this is purely as an example)
        region = attributes.get("region", "us-west-2")

        # This will read the attributes provided as part of the nitric stack file
        # attributes = dict_from_struct(deployment_up_request.attributes)

        # These are resources automatically discovered by the nitric CLI
        # It is only necessary to use these if you want to use the nitric SDKs in your applications
        # in order to automate infrastructure discovery
        # resources = req.spec.resources

        # Setup a backend
        # As an example this will setup an s3 backend, configuration can be read from the request and
        # more backend types supported from that configuration
        S3Backend(self, region="TODO", bucket="TODO", key="TODO", dynamodb_table="TODO")

        # Declare terraform variables for the stack if necessary
        # These can be read from the request and passed into the stack
        # example_variable = TerraformVariable(self, "example", type="string")

        # Configure on or more provider(s) as part of the root module
        provider = aws_provider.AwsProvider(self, "aws", region=region)

        # Create a new dynamic module
        # For more information on this see: https://developer.hashicorp.com/terraform/cdktf/concepts/modules
        # The below is provided an fill in example showing how a module can be referenced from a git repository
        # For a specific verson use may also use the ref parameter
        # See: https://developer.hashicorp.com/terraform/language/modules/sources#github
        module = TerraformHclModule(self, "example",
            source = "github.com/cloudposse/terraform-aws-s3-bucket",
            variables = {
                "TODO": "TODO"
            },
            providers = [provider]
        )

