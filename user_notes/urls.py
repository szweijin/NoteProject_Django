# user_notes/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # 包含 djoser 提供的認證相關 URL
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # 包含 notes 應用程式的 REST API URL
    path('api/', include('notes.urls')), # 這裡已經有了，負責 /api/notes/

    # 包含 notes 應用程式的前端 URL 到專案根路徑
    path('', include('notes.urls')),
]