from django.db.models import Func

class MonthName(Func):
    function = 'TO_CHAR'
    template = "%(function)s(%(expressions)s, 'Month')"