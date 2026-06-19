"""Notification dispatch for the notify service."""


def send_email(user, template, payload):
    _dispatch("email", user, template, payload)
    emit("notify.email.sent", user)


def send_sms(user, template, payload):
    _dispatch("sms", user, template, payload)
    emit("notify.sms.sent", user)


def _dispatch(channel, user, template, payload):  # placeholder
    ...


def emit(event_name, payload):  # placeholder
    ...
