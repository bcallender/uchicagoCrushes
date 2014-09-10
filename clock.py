from apscheduler.schedulers.blocking import BlockingScheduler
import logging 
import update_db


sched = BlockingScheduler()
logging.basicConfig()

@sched.scheduled_job('interval', minutes=1)
def update_post_data():
	update_db.update_data()

sched.start()
