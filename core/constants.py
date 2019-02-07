from django.utils.translation import gettext_lazy as _


class STATUS:
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"

    choices = (
        (ACTIVE, _('Active')),
        (DELETED, _('Deleted')),
    )
