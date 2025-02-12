CREWAI_ROOT = $(shell pwd)/crewai_ai_content_aws

run_flow:
	@bash -c 'cd $(CREWAI_ROOT) && ./.venv/bin/creawai flow kickoff'
