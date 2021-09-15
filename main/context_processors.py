from django.conf import settings


def global_variables(request):
    return {
        "PROJECT_TITLE": settings.PROJECT_TITLE,
        "INSTITUTION_NAME": settings.INSTITUTION_NAME,
        "GA_MEASUREMENT_ID": getattr(settings, "GA_MEASUREMENT_ID", None)
    }
