import os
import redis
from django.core.mail import EmailMessage
from django.conf import settings
from celery import task
from celery.utils.log import get_task_logger
from ResultsPDF.api.v1.utils import json_to_pdf

logger = get_task_logger(__name__)


r = redis.Redis(host=os.getenv('REDIS_SERVER'), port=6379, db=2, charset="utf-8", decode_responses=True)


@task()
def send_links_pdf_email_task(user_id, user_email, task_queue_push_time):
    """
    sends an email with suggested_links attached in a pdf,
    if no new request with new data came in last 5 minutes from user
    """
    last_link_with_time = r.zrevrange(2, 0, 0, withscores=True)
    if not last_link_with_time or last_link_with_time[0][1] > task_queue_push_time:
        return None
    data = r.zrange(user_id, 0, -1)
    file_buffer = json_to_pdf(data)
    filename = 'suggested_links.pdf'
    email = EmailMessage('Further Suggested Reading Links!',
                         '''Please Find Attached the PDF document containing the suggested links for your further reading!
                         collected exclusively on the basis of your recent queries''',
                         settings.EMAIL_HOST_USER,
                         [user_email])
    email.attach(filename, file_buffer.read(), 'application/pdf')
    email.send()
    r.delete(user_id)
    logger.info("Sent suggested links pdf email")
    return None
