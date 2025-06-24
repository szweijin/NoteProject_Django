from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note                                                # 指定這個序列化器對應的 Django 模型是 Note
        # fields = '__all__'                                        # 包含模型中所有的欄位
        fields = ['id', 'title', 'content', 'created_at', 'user']   # 明確列出要包含的欄位
        read_only_fields = ['user', 'created_at']                   # 將 user 和 created_at 設定為唯讀
