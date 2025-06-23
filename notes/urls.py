from django.urls import path
from .views import (
    NoteListCreateAPIView, NoteDetailAPIView, # REST API 視圖
    home_view, register_view, login_view, logout_view,
    note_list_view, note_create_view, note_update_view, note_delete_view
)

urlpatterns = [
    # --- 前端頁面 URL ---
    path('', home_view, name='home'), # 首頁
    path('register/', register_view, name='register'), # 註冊頁面
    path('login/', login_view, name='login'), # 登入頁面
    path('logout/', logout_view, name='logout'), # 登出動作

    path('notes_web/', note_list_view, name='note_list'), # 筆記列表 (Web 版)
    path('notes_web/create/', note_create_view, name='note_create'), # 創建筆記 (Web 版)
    path('notes_web/<int:pk>/edit/', note_update_view, name='note_update'), # 編輯筆記 (Web 版)
    path('notes_web/<int:pk>/delete/', note_delete_view, name='note_delete'), # 刪除筆記 (Web 版)


    # --- REST API URL  ---
    path('api/notes/', NoteListCreateAPIView.as_view(), name='note-list-create-api'),
    path('api/notes/<int:pk>/', NoteDetailAPIView.as_view(), name='note-detail-api'),
]