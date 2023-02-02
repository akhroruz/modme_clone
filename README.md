# ModmeClone

## TODO - Required

1. permissions
   - administrator - (crud) student, (crud) course, (crud) teacher, (crud) room
   - 



1. [x] custom admin
2. [x] sentry
3. [x] github
4. [ ] test (pytest coverage 80% ^)
5. [ ] docker/docker compose
6. [ ] elasticsearch
7. [ ] security
8. [ ] github actions
9. [ ] server

## Don't Required

1. [ ] cache
2. [ ] celery
3. [ ] redis
4. [ ] rabbitmq
5. [ ] cron

## Makefile

- ```make mig``` makemigrations & migrate
- ```make unmig``` delete migrations files
- ```make admin``` create admin superuser
- ```make load``` collect all datas
- ```make local``` i18n compile messages
