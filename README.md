# 📚 **EduFlow 프로젝트**

EduFlow는 Django 프레임워크와 Django REST Framework(DRF)를 기반으로 한 **온라인 교육 플랫폼**입니다. 강좌, 레슨, 과제 및 제출물 관리 기능과 함께 **ELK 스택**을 통한 실시간 로그 모니터링 기능을 제공합니다.

---

## 🚀 **프로젝트 주요 기능**

### 🎓 **강좌 관리 (Courses)**

-   강좌 생성, 수정, 삭제
-   강좌 공개(Publish) 기능
-   학생 수강 등록 기능

### 📖 **레슨 관리 (Lessons)**

-   강좌별 레슨 생성 및 조회
-   레슨 업데이트 및 삭제

### 🏃 **과제 및 제출물 관리 (Assignments & Submissions)**

-   강좌별 과제 생성, 조회 및 제출
-   제출물 관리 기능

### 👤 **사용자 관리 (Users)**

-   사용자 등록 및 인증 (JWT 기반)
-   사용자 프로필 조회 및 수정
-   비밀번호 변경 및 계정 삭제

### 📊 **ELK 스택을 통한 로그 분석**

-   **Elasticsearch**: 실시간 데이터 검색 및 분석
-   **Logstash**: 데이터 수집 및 Elasticsearch로 전달
-   **Kibana**: 시각화 대시보드를 통한 로그 모니터링

---

## 🛠 **기술 스택**

-   **Backend**: Django, Django REST Framework
-   **Database**: MySQL
-   **Authentication**: JWT (JSON Web Tokens)
-   **Logging & Monitoring**: ELK Stack (Elasticsearch, Logstash, Kibana)
-   **Dependencies**: Pillow, MySQLclient, python-logstash

---

## ⚙️ **프로젝트 설치 및 실행 방법**

### ✅ **1. 프로젝트 클론**

```bash
git clone https://github.com/yourusername/eduflow.git
cd eduflow
```

### 📦 **2. 가상환경 생성 및 활성화**

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
```

### 🔧 **3. 필수 패키지 설치**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 🏗 **4. 데이터베이스 설정 (MySQL)**

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

## 📊 **ELK 스택 설정 및 실행**

### 🐳 **1. Docker 및 Docker Compose 설치**

```bash
# Ubuntu
sudo apt update && sudo apt install -y docker.io docker-compose

# macOS (Homebrew 사용)
brew install --cask docker
```

### 🛠 **2. ELK 스택 Docker Compose 설정 (`docker-compose.yml`)**

```yaml
version: "3.7"
services:
    elasticsearch:
        image: docker.elastic.co/elasticsearch/elasticsearch:8.12.0
        container_name: elasticsearch
        environment:
            - discovery.type=single-node
            - xpack.security.enabled=false
        ports:
            - "9200:9200"

    logstash:
        image: docker.elastic.co/logstash/logstash:8.12.0
        container_name: logstash
        ports:
            - "5044:5044"
        volumes:
            - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf

    kibana:
        image: docker.elastic.co/kibana/kibana:8.12.0
        container_name: kibana
        environment:
            ELASTICSEARCH_HOSTS: http://elasticsearch:9200
        ports:
            - "5601:5601"
        depends_on:
            - elasticsearch
```

### ⚡ **3. ELK 스택 실행**

```bash
docker-compose up -d
```

### 📝 **4. Logstash 설정 (`logstash.conf`)**

```plaintext
input {
  tcp {
    port => 5044
    codec => json
  }
}

output {
  elasticsearch {
    hosts => ["http://elasticsearch:9200"]
    index => "eduflow-logs-%{+YYYY.MM.dd}"
  }
  stdout { codec => rubydebug }
}
```

### 🌐 **5. Kibana 접속 확인**

웹 브라우저에서 다음 URL에 접속:

```
http://localhost:5601
```

✅ **Kibana 접속 문제 해결**:

-   `docker ps -a`로 컨테이너 상태 확인
-   포트 점유 여부 확인: `lsof -i :5601`
-   Kibana 로그 확인: `docker logs kibana`
-   Elasticsearch 연결 여부 확인: `curl localhost:9200`

---

### 💡 **6. Django에서 Logstash 연동 설정**

```python
import logging
from logstash import TCPLogstashHandler

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'logstash': {
            'level': 'INFO',
            'class': 'logstash.TCPLogstashHandler',
            'host': 'localhost',
            'port': 5044,
            'version': 1,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['logstash'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

---

## 🎨 Docker 실행 후 Redis 사용 방법

```bash
docker exec -i -t eduflow-redis-a redis-cli
```

## 📄 **에러 코드 및 응답 형식**

| HTTP 상태 코드   | 설명                  | 응답 예시                                |
| ---------------- | --------------------- | ---------------------------------------- |
| 200 OK           | 요청 성공             | `{ "status": "success" }`                |
| 201 Created      | 리소스 생성 성공      | `{ "status": "created" }`                |
| 400 Bad Request  | 잘못된 요청           | `{ "error": "Invalid input" }`           |
| 401 Unauthorized | 인증 실패             | `{ "error": "Authentication required" }` |
| 403 Forbidden    | 권한 부족             | `{ "error": "Permission denied" }`       |
| 404 Not Found    | 리소스를 찾을 수 없음 | `{ "error": "Not found" }`               |

---

## ✨ **기여 방법**

1. Fork 저장소
2. 새로운 브랜치 생성: `git checkout -b feature/elk-integration`
3. 변경 사항 커밋: `git commit -m 'Add ELK stack integration'`
4. 브랜치 푸시: `git push origin feature/elk-integration`
5. Pull Request 생성
