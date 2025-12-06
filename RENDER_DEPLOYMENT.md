# Render 배포 가이드

이 문서는 TextAI 프로젝트를 Render에 배포하는 방법을 설명합니다.

## 📋 사전 준비사항

1. **Render 계정 생성**
   - [Render.com](https://render.com)에 가입
   - GitHub 계정과 연동 (권장)

2. **필요한 환경 변수 준비**
   - `OPENAI_API_KEY`: OpenAI API 키
   - `SUPABASE_URL`: Supabase 프로젝트 URL
   - `SUPABASE_SERVICE_ROLE_KEY`: Supabase Service Role Key
   - `REACT_APP_SUPABASE_URL`: Supabase 프로젝트 URL (Frontend용)
   - `REACT_APP_SUPABASE_ANON_KEY`: Supabase Anon Key (Frontend용)

## 🚀 배포 단계

### 방법 1: render.yaml 사용 (권장)

1. **GitHub에 프로젝트 푸시**
   ```bash
   git add .
   git commit -m "Render 배포 설정 추가"
   git push origin main
   ```

2. **Render 대시보드에서 Blueprint 배포**
   - Render 대시보드 접속
   - "New +" 버튼 클릭
   - "Blueprint" 선택
   - GitHub 저장소 연결
   - `render.yaml` 파일이 자동으로 감지됨
   - "Apply" 클릭

3. **환경 변수 설정**
   - Backend 서비스에서 다음 환경 변수 설정:
     - `OPENAI_API_KEY`
     - `SUPABASE_URL`
     - `SUPABASE_SERVICE_ROLE_KEY`
   - Frontend 서비스에서 다음 환경 변수 설정:
     - `REACT_APP_SUPABASE_URL`
     - `REACT_APP_SUPABASE_ANON_KEY`
     - `REACT_APP_API_URL` = Backend 서비스의 전체 URL (예: `https://textai-backend.onrender.com`)

### 방법 2: 수동 배포

#### Backend 배포

1. **새 Web Service 생성**
   - Render 대시보드에서 "New +" → "Web Service" 선택
   - GitHub 저장소 연결

2. **설정 입력**
   - **Name**: `textai-backend`
   - **Environment**: `Python 3`
   - **Region**: `Singapore` (또는 원하는 지역)
   - **Branch**: `main` (또는 기본 브랜치)
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

3. **환경 변수 추가**
   - `PYTHON_VERSION` = `3.12.0`
   - `OPENAI_API_KEY` = (실제 API 키)
   - `SUPABASE_URL` = (실제 Supabase URL)
   - `SUPABASE_SERVICE_ROLE_KEY` = (실제 Service Role Key)
   - `RENDER` = `true`

4. **배포 시작**
   - "Create Web Service" 클릭

#### Frontend 배포

1. **새 Web Service 생성**
   - Render 대시보드에서 "New +" → "Web Service" 선택
   - 같은 GitHub 저장소 선택

2. **설정 입력**
   - **Name**: `textai-frontend`
   - **Environment**: `Node`
   - **Region**: `Singapore` (Backend와 동일한 지역 권장)
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npx serve -s build -l $PORT`

3. **환경 변수 추가**
   - `NODE_VERSION` = `18.18.0`
   - `REACT_APP_API_URL` = Backend 서비스의 URL (예: `https://textai-backend.onrender.com`)
   - `REACT_APP_SUPABASE_URL` = (실제 Supabase URL)
   - `REACT_APP_SUPABASE_ANON_KEY` = (실제 Anon Key)

4. **배포 시작**
   - "Create Web Service" 클릭

## ⚙️ 환경 변수 설정 상세

### Backend 환경 변수

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `OPENAI_API_KEY` | OpenAI API 키 | `sk-...` |
| `SUPABASE_URL` | Supabase 프로젝트 URL | `https://xxx.supabase.co` |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase Service Role Key | `eyJ...` |
| `RENDER` | Render 환경임을 나타내는 플래그 | `true` |

### Frontend 환경 변수

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `REACT_APP_API_URL` | Backend API URL | `https://textai-backend.onrender.com` |
| `REACT_APP_SUPABASE_URL` | Supabase 프로젝트 URL | `https://xxx.supabase.co` |
| `REACT_APP_SUPABASE_ANON_KEY` | Supabase Anon Key | `eyJ...` |

## 🔍 배포 확인

1. **Backend 확인**
   - Backend 서비스 URL로 접속 (예: `https://textai-backend.onrender.com`)
   - `/stream` 엔드포인트에 POST 요청 테스트

2. **Frontend 확인**
   - Frontend 서비스 URL로 접속 (예: `https://textai-frontend.onrender.com`)
   - 브라우저 콘솔에서 API 연결 상태 확인

## 🐛 문제 해결

### Backend 배포 실패

1. **의존성 설치 실패**
   - `requirements.txt`에 모든 패키지가 포함되어 있는지 확인
   - Python 버전이 `3.12.0`인지 확인

2. **포트 바인딩 오류**
   - `$PORT` 환경 변수를 사용하는지 확인
   - `0.0.0.0`으로 바인딩하는지 확인

3. **타임아웃 오류**
   - Gunicorn 타임아웃을 120초로 설정했는지 확인
   - AI API 호출 시간이 길 경우 타임아웃 증가 고려

### Frontend 배포 실패

1. **빌드 실패**
   - `package.json`의 모든 의존성이 올바른지 확인
   - Node 버전이 `18.18.0`인지 확인

2. **API 연결 실패**
   - `REACT_APP_API_URL`이 올바르게 설정되었는지 확인
   - Backend 서비스가 실행 중인지 확인
   - CORS 설정이 올바른지 확인

### CORS 오류

- Backend의 `app.py`에서 CORS가 `"*"`로 설정되어 있는지 확인
- Frontend URL이 Backend의 허용된 origin에 포함되어 있는지 확인

## 📝 참고사항

1. **무료 플랜 제한사항**
   - Render 무료 플랜은 15분간 비활성화 시 서비스가 슬립 모드로 전환됨
   - 첫 요청 시 깨어나는 데 시간이 걸릴 수 있음
   - 시연 전에 서비스를 깨워두는 것을 권장

2. **환경 변수 보안**
   - 민감한 정보는 환경 변수로만 관리
   - `.env` 파일을 Git에 커밋하지 않음

3. **성능 최적화**
   - 필요시 Gunicorn 워커 수 조정
   - 타임아웃 설정 조정

## 🎯 시연용 팁

1. **사전 준비**
   - 배포 후 서비스가 완전히 시작될 때까지 대기 (약 5-10분)
   - 각 서비스에 한 번씩 요청을 보내 슬립 모드 해제

2. **백업 계획**
   - 로컬 환경도 준비해두기
   - 네트워크 문제 시 대비

3. **모니터링**
   - Render 대시보드에서 로그 확인
   - 에러 발생 시 빠르게 대응

## 📞 지원

문제가 발생하면 Render 로그를 확인하거나 GitHub Issues에 문의하세요.

