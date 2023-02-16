# Modme Clone API

## TODO - Required

1. [x] custom admin
2. [x] sentry
3. [x] github
4. [ ] permissions
    - ceo - all permissions
    - administrator - (crud) student, (crud) course, (crud) teacher, (crud) room, (crud) lead, (crud) holiday, (crud) archive, branch itself
    - branch director - (crud) student, (crud) course, (crud) teacher, (crud) room, (crud) lead, (crud) holiday, (crud) archive, branch itself
    - teacher - class days, self-groups
    - limited administrator - (crud) teacher, (crud) course, (crud) group, branch itself
    - marketer - (crud) leads
    - cashier - (crud) students, reports
5. [ ] test (pytest coverage 80% ^)
6. [ ] docker/docker compose
7. [x] elasticsearch
8. [ ] security
9. [x] GitHub actions
10. [ ] server

## Don't Require

1. [ ] cache
2. [ ] celery
3. [ ] redis
4. [ ] rabbitmq
5. [ ] cron
6. [x] flake8

## Makefile

- ```make mig``` make migrations and migrate
- ```make unmig``` delete migrations files
- ```make remig``` all in one
- ```make admin``` create admin superuser
- ```make load``` collect all datas
- ```make faker``` create random fake datas in database
- ```make search_index``` to create and populate the Elasticsearch index and mapping
- ```make ram``` remove all tables from the database
