# ModmeClone

## TODO - Required

1. [ ] permissions
   - ceo - all permissions
   - administrator - (crud) student, (crud) course, (crud) teacher, (crud) room, (crud) lead, (crud) holiday, (crud) archive, branch itself
   - branch director - (crud) student, (crud) course, (crud) teacher, (crud) room, (crud) lead, (crud) holiday, (crud) archive, branch itself
   - teacher - class days, self-groups
   - limited administrator - (crud) teacher, (crud) course, (crud) group, branch itself
   - marketer - (crud) leads
   - cashier - (crud) students, reports
2. [x] custom admin
3. [x] sentry
4. [x] github
5. [ ] test (pytest coverage 80% ^)
6. [ ] docker/docker compose
7. [ ] elasticsearch
8. [ ] security
9. [ ] github actions
10. [ ] server

## Don't Required

1. [ ] cache
2. [ ] celery
3. [ ] redis
4. [ ] rabbitmq
5. [ ] cron

## Makefile

- ```make mig``` make migrations and migrate
- ```make unmig``` delete migrations files
- ```make remig``` delete migrations files and make migrations and migrate
- ```make admin``` create admin superuser
- ```make load``` collect all datas
- ```make local``` i18n compile messages
- ```make poetry``` install poetry
