# 📚 **EduFlow 프로젝트**

EduFlow는 Django 프레임워크와 Django REST Framework(DRF)를 기반으로 한 **온라인 교육 플랫폼**입니다. 이 프로젝트는 강좌, 레슨, 과제 및 제출물 관리 기능을 제공합니다. 강사, 관리자 및 학생 간의 효율적인 학습 환경을 제공합니다.

---

## 🚀 **프로젝트 기능**

### 🎓 **강좌 관리 (Courses)**

-   강좌 생성, 수정, 삭제
-   강좌 공개(Publish) 기능
-   학생 수강 등록 기능

### 📖 **레슨 관리 (Lessons)**

-   강좌별 레슨 생성 및 조회
-   레슨 업데이트 및 삭제

### 🏃 **과제 관리 (Assignments)**

-   강좌별 과제 생성 및 조회
-   제출물 관리 및 제출 기능

### 👤 **사용자 관리 (Users)**

-   사용자 등록 및 인증 (JWT 기반)
-   사용자 프로필 조회 및 수정
-   비밀번호 변경 및 계정 삭제

---

## 🛠 **기술 스택**

-   **Backend**: Django, Django REST Framework
-   **Database**: MySQL
-   **Authentication**: JWT (JSON Web Tokens)
-   **Dependencies**: Pillow, MySQLclient

---

## ⚙️ **프로젝트 설치 및 실행 방법**

### ✅ **1. 프로젝트 클론**

```bash
git clone https://github.com/yourusername/eduflow.git
cd eduflow
```

### 📦 **2. 가상환경 생성 및 활성화**

```bash
# 가상환경 생성
python -m venv venv

# Windows
venv\\Scripts\\activate

# macOS/Linux
source venv/bin/activate
```

### 🔧 **3. 필수 패키지 설치**

```bash
pip install -r requirements.txt
```

### 🏗 **4. 데이터베이스 설정 (MySQL)**

`settings.py`의 데이터베이스 설정을 자신의 환경에 맞게 변경합니다:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eduflow_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 🔄 **5. 마이그레이션 적용**

```bash
python manage.py makemigrations
python manage.py migrate
```

### 🚀 **6. 서버 실행**

```bash
python manage.py runserver
```

접속 URL: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔑 **API 엔드포인트 요약**

### 👤 **Users API**

| 엔드포인트                       | 메서드 | 설명               |
| -------------------------------- | ------ | ------------------ |
| `/api/v1/users/register/`        | POST   | 사용자 등록        |
| `/api/v1/users/login/`           | POST   | 사용자 로그인      |
| `/api/v1/users/profile/`         | GET    | 사용자 프로필 조회 |
| `/api/v1/users/change-password/` | POST   | 비밀번호 변경      |
| `/api/v1/users/delete/`          | DELETE | 사용자 계정 삭제   |

### 🎓 **Courses API**

| 엔드포인트                      | 메서드 | 설명           |
| ------------------------------- | ------ | -------------- |
| `/api/v1/courses/`              | GET    | 모든 강좌 조회 |
| `/api/v1/courses/`              | POST   | 강좌 생성      |
| `/api/v1/courses/{id}/`         | GET    | 특정 강좌 조회 |
| `/api/v1/courses/{id}/publish/` | POST   | 강좌 공개      |
| `/api/v1/courses/{id}/enroll/`  | POST   | 강좌 수강 등록 |

### 📖 **Lessons API**

| 엔드포인트                                         | 메서드 | 설명                  |
| -------------------------------------------------- | ------ | --------------------- |
| `/api/v1/courses/{course_id}/lessons/`             | GET    | 강좌별 레슨 목록 조회 |
| `/api/v1/courses/{course_id}/lessons/`             | POST   | 강좌별 레슨 생성      |
| `/api/v1/courses/{course_id}/lessons/{lesson_id}/` | GET    | 특정 레슨 상세 조회   |

### 🏃 **Assignments & Submissions API**

| 엔드포인트                                                             | 메서드 | 설명           |
| ---------------------------------------------------------------------- | ------ | -------------- |
| `/api/v1/courses/{course_id}/assignments/`                             | GET    | 과제 목록 조회 |
| `/api/v1/courses/{course_id}/assignments/`                             | POST   | 과제 생성      |
| `/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions/` | POST   | 과제 제출      |

---

## 🧪 **테스트 실행**

```bash
python manage.py test
```

---

## 💡 **기타 정보**

-   Django Admin: `/admin/`
-   JWT 인증 사용 (`Authorization: Bearer <token>` 헤더 필요)
-   파일 업로드 경로: `/media/`
-   MySQL 사용 시 `slug` 필드의 `max_length`는 255 이하로 설정

---

## ✨ **기여 방법**

1. Fork 저장소
2. 새로운 브랜치 생성: `git checkout -b feature/내기능`
3. 변경 사항 커밋: `git commit -m 'Add 내 기능'`
4. 브랜치 푸시: `git push origin feature/내기능`
5. Pull Request 생성

---
