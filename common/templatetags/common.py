from django import template


register = template.Library()


@register.filter
def get_value(obj, key, default=None):
    """
    Returns dictionary item value by name for dictionary objects or property value by name for other types.
    Also list of lists obj is supported.
    :param obj: dict or object
    :param key: dict item or property name
    :param default: default value
    :return:
    """
    if isinstance(obj, dict):
        return obj.get(key, default)

    elif hasattr(obj, '__iter__'):
        for item in obj:
            if hasattr(obj, '__iter__') and len(item) > 1 and item[0] == key:
                return item[1]
        return default

    else:
        return getattr(obj, key, default)
