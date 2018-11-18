build:
	docker build -t dep .
run:
	pipenv run python3 main.py
rund:
	docker run --env-file .env -it dep

shell:
	docker run -it --env-file .env dep bash

deploy:
	aws ecr get-login --no-include-email --profile dep --region us-east-1 | sh
	docker tag dep 397678393215.dkr.ecr.us-east-1.amazonaws.com/dep
	docker push 397678393215.dkr.ecr.us-east-1.amazonaws.com/dep
