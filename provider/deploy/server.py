from typing import AsyncIterator
import os
from nitric.utils import dict_from_struct
from nitric.proto.deployments.v1 import (
    DeploymentBase,
    DeploymentUpRequest,
    DeploymentUpEvent,
    DeploymentDownRequest,
    DeploymentDownEvent,
)
from cdktf import App
from .stack import DynamicTerraformStack

# Because this will be executed as a nitric docker provider
# We use this environment variable to find the bound working directory to write out results
workspace = os.getenv("WORKSPACE", "/workspace")

class DeploymentService(DeploymentBase):
    """Deployment Service implementation"""

    async def up(
        self, deployment_up_request: DeploymentUpRequest
    ) -> AsyncIterator[DeploymentUpEvent]:
        # Start the tf cdk deployment
        # The end result will be the synthesis of a terraform application
        # This will be a json output, but HCL output is also possible if required
        yield DeploymentUpEvent(message="Starting CDKTF Stack Synthesis...")

        attributes = dict_from_struct(deployment_up_request.attributes)

        enable_hcl = attributes.get("hcl", False)
        out_dir = f"{workspace}/cdktf.out"

        app = App(
            hcl_output=enable_hcl,
            # This line is only necessary if you are using relative modules
            # context={"cdktfRelativeModules": ["./modules"]},
            outdir=out_dir,
        )
        project_name = attributes["project"]
        stack_name = attributes["stack"]
        full_stack_name = f"{project_name}-{stack_name}"

        
        DynamicTerraformStack(app, full_stack_name, deployment_up_request)
        yield DeploymentUpEvent(message=f"Synthesizing stack: {full_stack_name}")
        app.synth()
        yield DeploymentUpEvent(message=f"Results written to: {out_dir}")

        # This is only necessary if the container is running as root
        # With rootless docker or podman then a chown will not be necessary
        os.chmod(f"{out_dir}/stacks/{full_stack_name}", 0o777)

        yield DeploymentUpEvent(message="Done")

    async def down(
        self, deployment_down_request: DeploymentDownRequest
    ) -> AsyncIterator[DeploymentDownEvent]:
        # This is technically a no-op unless we want to interactively being tearing down the
        # stack based on the current tfstate
        # This can be done by simply spawning the terraform CLI against the current terraform project
        yield DeploymentDownEvent(
            message="this provider does not support down operations.\nUse `terraform destroy` on the generated output."
        )
