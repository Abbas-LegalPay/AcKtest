from django.db import models
from AccuknoxApp.models.accuknox_user_model import AccuKnoxUser


class FriendRequest(models.Model):
    from_user = models.ForeignKey(AccuKnoxUser, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(AccuKnoxUser, related_name='received_requests', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "accuknox_friends_details"
        verbose_name = "AccuKnox Friends Detail"
        verbose_name_plural = "AccuKnox Friends Details"
