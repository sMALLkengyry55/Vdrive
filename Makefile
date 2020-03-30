# general
MANAGE=./manage.py
COVERAGE=coverage
COVER=apps
UTIL_TEST=./manage.py test --settings=settings.unittest

DOCKER_COMPOSE=docker-compose
DOCKER_DEV_CONFIG=docker-dev.yml
DOCKER_TEST_CONFIG=docker-test.yml


test:
	$(COVERAGE) erase; \
	$(COVERAGE) run --source $(COVER) $(UTIL_TEST); \
	$(COVERAGE) report

run_tests:
	$(DOCKER_COMPOSE) -f $(DOCKER_DEV_CONFIG) run web bash -c "pip install -r requirements_dev.txt; $(UTIL_TEST)"

docker_dev:
	$(DOCKER_COMPOSE) -f $(DOCKER_DEV_CONFIG) up

docker_dev_status:
	$(DOCKER_COMPOSE) -f $(DOCKER_DEV_STATUS) ps

docker_dev_rebuild:
	$(DOCKER_COMPOSE) -f $(DOCKER_DEV_CONFIG) up --build

docker_dev_with_recreating_db:
	echo RECREATE_DB=1 > docker_env.env; \
	$(DOCKER_COMPOSE) -f $(DOCKER_DEV_CONFIG) up --build; \
	> docker_env.env

docker_test:
	$(DOCKER_COMPOSE) -f $(DOCKER_TEST_CONFIG) up --build -d

docker_test_stop:
	$(DOCKER_COMPOSE) -f $(DOCKER_TEST_CONFIG) stop
