from django import template


register = template.Library()


@register.filter
def score_percentage(value, max_score):
    """
    Returns value of a given score as a percentage of max_score.
    """
    if not (value and max_score):
        return 0
    return round((value * 100) / max_score)
