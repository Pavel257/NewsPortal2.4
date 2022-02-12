from django.apps import AppConfig


class AppointmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointments'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import appointments.signals







        # from .tasks import send_mails
        # from .scheduler import appointment_scheduler
        # print('started')
        #
        # appointment_scheduler.add_job(
        #     id='mail send',
        #     func=send_mails,
        #     trigger='interval',
        #     seconds=10,
        # )
        # appointment_scheduler.start()