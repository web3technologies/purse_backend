from django.db.models import Func, F


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(CAST(%(expressions)s AS numeric), %(extra)s)'

    def __init__(self, expression, decimal_places=2, **extra):
        super().__init__(expression, **extra)
        self.extra['extra'] = decimal_places
        
