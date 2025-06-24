from rest_framework import generics                   
from rest_framework.permissions import IsAuthenticated 
from .models import Note                               
from .serializers import NoteSerializer        

from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm 
from django.contrib.auth import login, logout 
from django.contrib.auth.decorators import login_required 
from django.contrib import messages 

# --- 前端頁面相關視圖 ---

def home_view(request):
    """
    處理首頁請求，渲染首頁模板。
    """
    return render(request, 'home.html')

def register_view(request):
    """
    處理使用者註冊頁面
    如果收到 POST 請求，則嘗試創建使用者；否則顯示註冊表單
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 註冊成功後自動登入
            messages.success(request, '註冊成功！')
            return redirect('note_list') # 註冊並登入後導向筆記列表
        else:
            messages.error(request, '註冊失敗，請檢查輸入。')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    """
    處理使用者登入頁面。
    如果收到 POST 請求，則嘗試登入；否則顯示登入表單。
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'歡迎回來，{user.username}！')
            return redirect('note_list') # 登入成功後導向筆記列表
        else:
            messages.error(request, '登入失敗，請檢查使用者名稱和密碼。')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required # 只有登入的使用者才能訪問此視圖
def logout_view(request):
    """
    處理使用者登出。
    """
    logout(request)
    messages.info(request, '您已成功登出。')
    return redirect('home')

@login_required
def note_list_view(request):
    """
    顯示當前使用者所有筆記的列表。
    """
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'note_list.html', {'notes': notes})

@login_required
def note_create_view(request):
    """
    處理創建新筆記的頁面。
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Note.objects.create(user=request.user, title=title, content=content)
            messages.success(request, '筆記創建成功！')
            return redirect('note_list')
        else:
            messages.error(request, '標題和內容都不能為空。')
    return render(request, 'note_form.html', {'form_type': 'create'})

@login_required
def note_update_view(request, pk):
    """
    處理更新筆記的頁面。
    """
    note = get_object_or_404(Note, pk=pk, user=request.user) # 確保筆記屬於當前使用者
    if request.method == 'POST':
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        note.save()
        messages.success(request, '筆記更新成功！')
        return redirect('note_list')
    return render(request, 'note_form.html', {'note': note, 'form_type': 'update'})

@login_required
def note_delete_view(request, pk):
    """
    處理刪除筆記的邏輯。
    """
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST': # 使用 POST 請求來執行刪除，避免意外點擊
        note.delete()
        messages.success(request, '筆記刪除成功！')
        return redirect('note_list')
    return render(request, 'note_confirm_delete.html', {'note': note})

# --- REST Framework 相關視圖 ---
class NoteListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer # 指定使用的序列化器
    permission_classes = [IsAuthenticated] # 只有登入的使用者才能訪問

    def get_queryset(self):
        # 覆寫 get_queryset 方法，確保使用者只能看到自己的筆記
        return Note.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # 創建筆記時，自動將當前登入的使用者設定為筆記的擁有者
        serializer.save(user=self.request.user)

class NoteDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer # 指定使用的序列化器
    permission_classes = [IsAuthenticated] # 只有登入的使用者才能訪問

    def get_queryset(self):
        # 確保使用者只能操作自己的特定筆記
        return Note.objects.filter(user=self.request.user)
