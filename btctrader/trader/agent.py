from celery import Celery

celery = Celery('agent', broker='django://')

@celery.task
def blah():
    pass