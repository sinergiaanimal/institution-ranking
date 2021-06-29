from django.db import models


class ActivableModelQuerySet(models.QuerySet):

    def active(self):
        return self.filter(is_active=True)
