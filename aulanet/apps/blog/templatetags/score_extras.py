from django import template

register = template.Library()

@register.filter
def score_values(user_queryset):
    """Devuelve una lista de puntuaciones de usuarios que no sean None"""
    return [u.score for u in user_queryset if u.score is not None]

@register.filter
def average_score(values):
    """Calcula promedio de una lista de números"""
    if not values:
        return None
    return round(sum(values)/len(values), 1)
