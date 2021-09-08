from smtplib import SMTPException

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinLengthValidator
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

from cms.models.pluginmodel import CMSPlugin

from common.models import ActivableModel, TimestampedModel


class ContactFormPluginModel(CMSPlugin):
    name_fname = models.CharField(
        _('name of the name field'), max_length=100,
        default=_('Your name')
    )
    name_placeholder = models.CharField(
        _('placeholder of the name field'), max_length=100,
        default=_('Type your name')
    )
    email_fname = models.CharField(
        _('name of the e-mail field'), max_length=100,
        default=_('Your e-mail')
    )
    email_placeholder = models.CharField(
        _('placeholder of the e-mail field'), max_length=100,
        default=_('Type your e-mail')
    )
    message_fname = models.CharField(
        _('name of the message field'), max_length=100,
        default=_('Your message')
    )
    message_placeholder = models.CharField(
        _('placeholder of the message field'), max_length=100,
        default=_('Type your message here')
    )
    button_text = models.CharField(
        _('submit button text'), max_length=100,
        default=_('SEND MESSAGE')
    )

    def __str__(self):
        return '(Contact Form)'


class Recipient(ActivableModel, TimestampedModel):
    TO, CC, BCC = ('TO', 'CC', 'BCC')
    R_TYPE_CHOICES = (
        (TO, TO),
        (CC, CC),
        (BCC, BCC)
    )
    plugin = models.ForeignKey(
        verbose_name=_('Contact Form Plugin'),
        to=ContactFormPluginModel, null=True, on_delete=models.SET_NULL,
        related_name='recipients'
    )
    name = models.CharField(_('name'), max_length=100)
    email = models.EmailField(_('e-mail'))
    recipient_type = models.CharField(
        _('recipient type'), max_length=3, choices=R_TYPE_CHOICES, default=TO,
        help_text=_(
            'Type of the recipient: TO - normal, CC - copy, BCC - hidden copy.'
        )
    )

    def __str__(self):
        return (
            f'{self.get_recipient_type_display()}: '
            f'{self.name} <{self.email}>'
        )


class ContactMessage(TimestampedModel):
    STATUS_PENDING, STATUS_SUCCESS, STATUS_ERROR = range(1, 4)
    STATUS_CHOICES = (
        (STATUS_PENDING, _('pending')),
        (STATUS_SUCCESS, _('sent')),
        (STATUS_ERROR, _('error'))
    )

    sender_name = models.CharField(
        _('sender name'), max_length=100,
        null=False, blank=False
    )
    sender_email = models.EmailField(
        _('sender e-mail'),
        null=False, blank=False
    )
    message = models.TextField(
        _('message'), null=False, blank=False,
        validators=[MinLengthValidator(20)],
    )
    status = models.SmallIntegerField(
        _('status'), choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    status_msg = models.TextField(
        _('Status message')
    )
    recipients = models.ManyToManyField(
        to=Recipient, verbose_name=_('recipients'),
        blank=False
    )

    class Meta:
        verbose_name = _('Contact Message')
        verbose_name_plural = _('Contact Messages')

    def __str__(self):
        return _('{status} message from {email}').format(
            status=self.get_status_display(),
            email=self.sender_email
        )

    def send(self, do_save=True):
        recipients = self.recipients.all()
        to = [r.email for r in recipients if r.recipient_type == Recipient.TO]
        bcc = [r.email for r in recipients if r.recipient_type == Recipient.BCC]
        cc = [r.email for r in recipients if r.recipient_type == Recipient.CC]
        
        msg_body = render_to_string(
            'contact/email/contact_message.txt',
            {
                'project_title': settings.PROJECT_TITLE,
                'instance': self
            }
        )
        mail = EmailMultiAlternatives(
            subject=settings.CONTACT_MSG_SUBJECT.format(
                PROJECT_TITLE=settings.PROJECT_TITLE
            ),
            body=msg_body,
            to=to, bcc=bcc, cc=cc,
            reply_to=[self.sender_email]
        )
        try:
            mail.send()
        except SMTPException as e:
            self.status = self.STATUS_ERROR
            self.status_msg = _('Sending failed:\n{}').format(e)
            if do_save:
                self.save()
            return False
        else:
            self.status = self.STATUS_SUCCESS
            self.status_msg = _('Successfully sent.')
            if do_save:
                self.save()
            return True
