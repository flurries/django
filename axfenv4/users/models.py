from django.db import models

# Create your models here.


class UserModel(models.Model):
    username = models.CharField(max_length=32, unique=True)  # 名称
    password = models.CharField(max_length=256)  # 密码
    email = models.CharField(max_length=64, unique=True)  # 邮箱
    # False 代表女
    sex = models.BooleanField(default=False)  # 性别
    icon = models.ImageField(upload_to='icons')  # 头像
    is_delete = models.BooleanField(default=False)  # 是否删除

    class Meta:
        db_table = 'axf_users'
