from django.contrib.auth import get_user_model


class BaseCalculation:

    user_model = get_user_model() 
    
    def __init__(self, user_id, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user_id = user_id
        self.user = self.user_model.objects.get(id=user_id)