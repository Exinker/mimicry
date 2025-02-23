MIGRATION = head


run:
	@echo "\033[1;32m\tRun server:\033[0m"
	uv run uvicorn main:app --reload

alembic-create:
	@echo "\033[1;32m\tCreate migration:\033[0m"
	uv run alembic revision --autogenerate -m "$(MESSAGE)"

alembic-upgrade:
	@echo "\033[1;32m\tUpgrade migration:\033[0m"
	uv run alembic upgrade "$(MIGRATION)"
