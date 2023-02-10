from celery import shared_task


@shared_task
def task_send_email_dishes_modified_yesterday() -> bool:
    """
    The function manages the elements that are to be passed as a task to be called
    """
    from dishes.email_service.send_email_service import send_email_dishes_modified_yesterday
    send_email_dishes_modified_yesterday()
    return True
