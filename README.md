
# 筆記應用 (Django Notes App)

這是一個基於 Django 和 Django REST Framework 構建的簡單筆記應用程式。它提供使用者認證、個人筆記管理以及 RESTful API。

## 功能概覽

* **使用者認證**：安全的使用者註冊、登入、登出功能，由 Djoser 提供支援。
* **筆記管理**：針對登入使用者，提供個人筆記的增、刪、改、查 (CRUD) 功能。
* **RESTful API**：提供標準的 API 端點，可供其他前端應用程式或行動應用程式整合使用。
* **Django 模板前端**：包含基本的網頁介面，使用者可直接在瀏覽器中操作筆記。
* **響應式設計**：使用 Bootstrap 5，確保應用程式在不同設備上都能提供良好的使用者體驗。

## 如何在本地運行此專案

按照以下步驟在你的本地機器上啟動專案：

### 1. 克隆儲存庫

首先，將專案從 GitHub 克隆到你的本地電腦：

```bash
git clone [https://github.com/szweijin/NoteProject_Django.git](https://github.com/szweijin/NoteProject_Django.git)
cd NoteProject_Django
````

### 2\. 創建並激活虛擬環境

強烈建議使用 Python 虛擬環境來管理專案依賴，避免與系統或其它專案的套件衝突：

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS / Linux
# 或
# .venv\Scripts\activate   # Windows
```

### 3\. 安裝依賴

激活虛擬環境後，安裝 `requirements.txt` 中列出的所有依賴套件：

```bash
pip install -r requirements.txt
```

### 4\. 運行資料庫遷移

應用 Django 的資料庫遷移，創建必要的資料表：

```bash
python manage.py migrate
```


### 5\. 創建超級使用者 (管理員)

如果你需要訪問 Django 管理後台，請創建一個超級使用者：

```bash
python manage.py createsuperuser
```
會出現
```bash
使用者名稱: (自訂)
電子郵件: (可略)
Password: (輸入時不會出現字元，只要輸入完按 enter 即可)
Password (again): (同上)
Superuser created successfully.
```
按照提示輸入使用者名稱、電子郵件和密碼。

### 6\. 運行開發伺服器

啟動 Django 的開發伺服器：

```bash
python manage.py runserver
```

### 7\. 訪問應用程式

現在，你可以在瀏覽器中訪問以下網址來使用應用程式：

  * **前端介面**: `http://127.0.0.1:8000/`
  * **管理後台**: `http://127.0.0.1:8000/admin/`

-----

## 如何部署到 Render

這個專案已配置為可直接部署到 **Render** 平台。以下是簡要步驟：

### 1\. 在 GitHub 上擁有此專案

確保你已將此專案推送到你自己的 GitHub 儲存庫。本專案包含以下 Render 部署所需的檔案：

  * **`Procfile`**: 定義了 Web 服務的啟動命令。
  * **`requirements.txt`**: 列出了所有 Python 依賴，Render 會自動安裝。
  * **`user_notes/settings.py`**: 已調整為支援生產環境配置（例如 `DEBUG=False`, `ALLOWED_HOSTS`, `DATABASE_URL` 解析和靜態檔案服務）。

### 2\. 在 Render 上創建新的 Web 服務

1.  登入你的 **Render** 帳號 ([render.com](https://render.com/))。
2.  點擊儀表板上的 **`New`** -\> **`Web Service`**。
3.  連接你的 **GitHub 帳號**，並選擇此專案的儲存庫。
4.  在配置頁面，進行以下設定：
      * **Service Name**: 為你的服務命名 (例如 `my-django-notes-app`)。
      * **Root Directory**: 保持為空 (除非你的專案程式碼在儲存庫的子資料夾中)。
      * **Runtime**: 應該會自動偵測為 `Python 3`。
      * **Build Command**: `pip install -r requirements.txt`
      * **Start Command**: `gunicorn user_notes.wsgi:application` (請確認 `user_notes` 是你 Django 專案的實際資料夾名稱)
      * **Branch**: 選擇你打算部署的分支 (例如 `main` 或你用於部署配置的 `deploy-render` 分支)。
5.  **添加環境變數 (Environment Variables)**:
      * **`SECRET_KEY`**: 這是一個**必須**且**保密**的 Django 金鑰。請生成一個新的、長且隨機的字串作為其值。
      * **`DJANGO_DEBUG`**: 設定為 `False` (字串類型)。
      * Render 會自動為你的 PostgreSQL 資料庫提供一個 `DATABASE_URL` 環境變數，你無需手動配置。
6.  選擇適合你的實例類型 (例如 `Free` 免費層)。
7.  點擊 **`Create Web Service`**。

### 3\. 執行資料庫遷移和創建超級使用者 (在 Render 服務上)

部署成功後，你的資料庫表可能還未創建。你需要透過 Render 的 Shell 運行資料庫遷移：

1.  在 Render 儀表板中，點擊進入你的 Web 服務詳情頁面。
2.  在頂部導覽列找到 **`Shell`** 標籤並點擊。
3.  在打開的 Shell 介面中，輸入以下命令來運行資料庫遷移：
    ```bash
    python manage.py migrate
    ```
4.  如果你需要在生產環境中創建管理員帳號：
    ```bash
    python manage.py createsuperuser
    ```
    按照提示輸入詳細資訊。

現在，你的 Django 筆記應用程式應該已經部署完成，並可透過 Render 提供的 URL 進行訪問了！

-----