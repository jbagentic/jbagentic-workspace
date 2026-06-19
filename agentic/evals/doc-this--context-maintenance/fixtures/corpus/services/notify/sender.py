# Notification sender. One function per delivery channel.


def send_email(user, message):
    """Send an email notification."""
    raise NotImplementedError


def send_sms(user, message):
    """Send an SMS notification."""
    raise NotImplementedError
