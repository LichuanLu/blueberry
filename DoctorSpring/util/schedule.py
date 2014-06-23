# coding: utf-8
__author__ = 'chengc017'
from apscheduler.scheduler import Scheduler
from time import sleep
from oss_util import copyObjects
sched = Scheduler()
sched.start()

sched.add_interval_job(copyObjects,seconds=1)

while(True):
    sleep(3000)