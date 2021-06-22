from django.conf import settings


def global_variables(request):
    return {
        "PROJECT_TITLE": settings.PROJECT_TITLE,
    }
