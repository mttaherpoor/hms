from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class EmailService:

    @staticmethod
    def send_booking_emails(billing):

        context = {
            "billing": billing
        }

        # doctor
        EmailService._send(
            subject="New Appointment",
            template_prefix="email/new_appointment",
            to=[billing.appointment.doctor.user.email],
            context=context,
        )

        # patient
        EmailService._send(
            subject="Appointment Booked Successfully",
            template_prefix="email/appointment_booked",
            to=[billing.appointment.patient.email],
            context=context,
        )

    @staticmethod
    def _send(subject, template_prefix, to, context):

        text_body = render_to_string(
            f"{template_prefix}.txt",
            context
        )

        html_body = render_to_string(
            f"{template_prefix}.html",
            context
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.FROM_EMAIL,
            to=to,
        )

        msg.attach_alternative(html_body, "text/html")
        msg.send()
