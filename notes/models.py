# notes/models.py
from django.db import models
from django.contrib.auth.models import User # 導入 Django 內建的 User 模型

class Note(models.Model):
    # 使用 ForeignKey 關聯到 Django 內建的 User 模型
    # 當使用者被刪除時，其所有筆記也會被刪除 (models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100) # 筆記標題，最大長度 100 字元
    content = models.TextField() # 筆記內容，不限制長度
    created_at = models.DateTimeField(auto_now_add=True) # 筆記建立時間，會自動設定為建立時的時間

    def __str__(self):
        # 定義當物件被轉換為字串時的顯示方式，方便在 Django Admin 中查看
        return f"{self.title} by {self.user.username}"