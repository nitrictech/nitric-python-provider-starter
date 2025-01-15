.PHONY: build
build:
	@docker build -t nitric-python-starter .
	@echo Docker container nitric-python-starter built

# Only necessary if you are planning on using the nitric SDKs for automatic resource discovery
# This is where we build an abstract runtime that will interact with the Nitric SDKs at runtime
# .PHONY: runtime
# runtime:
# 	@cd runtime && go build -o runtime ./cmd/main.go

.PHONY: install
install:
	@uv sync --dev

# Only necessary if you are using CDKTF to generate language bindings for HCL modules
# .PHONY: generate
# generate: install clean
# 	@npx -y cdktf-cli@0.20.8 get
# 	@touch imports/__init__.py

clean:
	@rm -rf imports

run:
	@docker run -it --rm -v $(PWD)/cdktf:/cdktf mapfre