# nitric-python-provider-starter

# Getting Starter

## Prerequisites
 - Docker/Podman
 - Make
 - Python
 - uv

## Building the container

The provider container can be built using:

```bash
make build
```

## Running the container

To use this provider with nitric once it's built you can using the following in your nitric stack file:

```yaml
# The nitric provider to use
provider: docker://nitric-python-starter

# An example property that can be passed to the provider
region: test
```