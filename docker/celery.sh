#!/bin/bash

if [[ ${1} == 'celery' ]]; then
  celery -A tasks.celery_tasks:celery worker --loglevel=INFO --pool=solo
elif [[ ${1} == 'flower' ]]; then
  celery -A tasks.celery_tasks:celery flower