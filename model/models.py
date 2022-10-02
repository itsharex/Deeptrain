from django.db import models

identitys = {
    0: "User",
    1: "VIP",  # Very Important Person
    2: "Admin",
    3: "ServerHost",
}

identity_choices = list(identitys.items())


class User(models.Model):
    id: models.AutoField
    username = models.CharField(max_length=12, default="")
    password = models.CharField(max_length=32, default="")  # password by md5(32x)
    register_time = models.DateTimeField(auto_now_add=True)

    objects: models.manager.Manager

    def __str__(self):
        return f"{self.username} ({self.id})"

    def __int__(self):
        return self.id


class Profile(models.Model):
    id: models.AutoField
    user_bind = models.OneToOneField("User", on_delete=models.CASCADE)  # django -> user_bind_id.
    detail = models.TextField(default="", max_length=200)
    identity = models.SmallIntegerField(choices=identity_choices)

    objects: models.manager.Manager

    def __str__(self):
        return f"Profile object ({self.id}, identity {self.__get_identity()}) with User {self.user_bind}"

    def __int__(self):
        return self.id

    def __get_identity(self):
        return identitys.get(self.identity)

    def get_data(self, default_detail="") -> ("detail", "identity"):
        return (self.detail or default_detail), self.__get_identity()

    def is_admin(self) -> bool:
        return self.identity >= 2
