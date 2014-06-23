# coding: utf-8
__author__ = 'chengc017'
from apscheduler.scheduler import Scheduler
from time import sleep
sched = Scheduler()
sched.start()
def test():
    print 'test'
sched.add_interval_job(test,seconds=1)




sleep(3000)