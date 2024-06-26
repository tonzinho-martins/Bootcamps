run:
	@uvicorn workout_api.main:app --reload

create-migrations:
	@alembic revision --autogenerate 

run-migrations:
	@alembic upgrade head
