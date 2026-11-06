# 폰지키미 (SeniorGuard)

**팀명:** 안심하조  
**프로젝트명:** 폰지키미  
**서비스명:** SeniorGuard

> 시니어 사용자의 스마트폰 앱 사용 환경을 모니터링하고, 앱 위험도 분석과 보호자 알림을 지원하는 안드로이드 모바일 보안 서비스

## 팀원 소개

| 역할 | 팀원 |
| --- | --- |
| 기획 | 최영빈 |
| 프론트엔드 | 박주현, 조세빈 |
| 백엔드 | 김유나, 박정현 |

## 1. 프로젝트 소개

**폰지키미(SeniorGuard)**는 모바일 보안에 익숙하지 않은 시니어 사용자를 위한 스마트폰 보안 서비스입니다. 안드로이드 기기에서 앱 사용 이벤트를 감지하고, 해당 앱의 권한과 기기 상태를 수집한 뒤 백엔드 분석 서버에 전달합니다. 분석 서버는 앱의 위험 점수와 위험 등급을 산출하며, 위험 상황이 발견되면 연결된 보호자에게 알림을 보내도록 설계되어 있습니다.

## 2. 개발 배경

스마트폰 보급과 함께 악성 앱, 개인정보 유출, 과도한 앱 권한 요청 등 모바일 보안 위협이 지속적으로 발생하고 있습니다. 특히 디지털 기기에 익숙하지 않은 시니어 사용자는 앱의 위험성을 직접 판단하거나 대응하기 어려울 수 있습니다.

이에 스마트폰 사용 상황을 자동으로 모니터링하고, 위험도를 분석해 사용자와 보호자의 대응을 돕는 서비스를 기획했습니다.

## 3. 주요 기능

### 3.1 앱 사용 모니터링

- Android `UsageStatsManager`를 이용한 앱 실행 이벤트(`ACTIVITY_RESUMED`) 감지
- Foreground Service 기반 백그라운드 모니터링
- 약 5초 간격으로 새로운 앱 사용 이벤트 확인
- 이벤트 발생 시 앱 정보 스냅샷 수집 및 분석 요청

### 3.2 앱 및 기기 상태 정보 수집

- 실행된 앱의 패키지명
- 앱이 요청한 권한과 권한 허용 여부
- 네트워크 연결 상태 및 화면 활성화 여부
- 앱 실행 이벤트 발생 시각과 정보 수집 시각
- 가능한 경우 APK SHA-256 해시 계산 및 전송

### 3.3 위험도 자동 분석

- 안드로이드 앱에서 **BE1 분석 API로 스냅샷 자동 전송**
- BE1이 BE2 보안 분석 서버에 요청을 전달하고 분석 결과 반환
- 위험 점수(`risk_score`), 위험 등급(`risk_level`), 요약(`summary`) 등 응답 처리
- 권한·실행 환경 및 VirusTotal 관련 분석 결과 활용
- 동일 앱의 반복 분석 요청을 줄이기 위한 전송 간격 제한

### 3.4 보호자 푸시 알림

- Firebase Cloud Messaging(FCM)을 이용한 기기 토큰 발급 및 BE1 등록
- 안드로이드에서 FCM 메시지 수신 및 알림 표시
- BE1에 `danger` 등급 진단 발생 시 연결된 보호자에게 FCM을 발송하는 코드 구현
- **수동 테스트 알림의 실제 수신 확인 완료**

> **검증 범위:** 앱 사용 감지 → 정보 수집 → BE1 → BE2 분석 결과 반환은 실제 테스트에 성공했습니다. 보호자 FCM은 수동 발송·수신 테스트를 완료했으며, **`danger` 자동 판정부터 보호자 푸시 수신까지의 전체 시나리오는 아직 별도 검증이 필요합니다.**

## 4. 기술 스택

| 구분 | 기술 | 용도 |
| --- | --- | --- |
| 모바일 | Kotlin, Android SDK | 안드로이드 앱 구현 |
| UI | Jetpack Compose | 앱 화면 구성 |
| 앱 모니터링 | `UsageStatsManager`, Foreground Service | 앱 실행 이벤트 수집 |
| 서버 | Python, Django, Django REST Framework | BE1·BE2 API 및 서버 구현 |
| 인증 | DRF Token Authentication | 로그인 및 인증된 API 요청 |
| 데이터베이스 | SQLite(로컬 기본값), `DATABASE_URL` 설정 시 외부 DB(BE1) | 사용자·진단 정보 저장 |
| 푸시 알림 | Firebase Cloud Messaging, Firebase Admin SDK | 보호자 알림 발송 및 수신 |
| 외부 분석 | VirusTotal API | APK 해시 기반 검사 결과 활용 |
| 배포 | Render | 백엔드 서버 호스팅 |
| 개발 협업 | Android Studio, Git, GitHub | 개발 및 버전 관리 |

## 5. 시스템 구조

```text
[시니어 Android 앱]
    │ 앱 실행 이벤트 감지 (UsageStatsManager)
    ▼
[MonitoringService + SnapshotCollector]
    │ 패키지명 / 권한 / 기기 상태 / APK SHA-256 등
    ▼
[DiagnosisSender]
    │ POST /api/diagnoses/analyze/ (인증 토큰)
    ▼
[BE1: Django REST API]
    │ 분석 요청 전달
    ▼
[BE2: 보안 분석 서버 + VirusTotal]
    │ 위험 등급 / 점수 / 분석 근거 반환
    ▼
[BE1: 진단 결과 저장 및 응답]
    │
    ├──► [시니어 앱: 분석 결과 수신 및 Logcat 확인]
    │
    └──► [danger 판정 시: 연결된 보호자 FCM 발송 로직]
                    ▼
           [보호자 Android 기기]
```

**실제 통합 테스트:** Chrome 실행 감지 후 `safe` 등급과 점수 10, VirusTotal 상태 `completed`인 분석 응답을 확인했습니다.

## 6. 빠른 시작

### 6.1 사전 요구사항

- Android Studio 및 Android SDK
- Android Emulator 또는 안드로이드 기기
- Python 및 가상환경 도구(백엔드를 로컬 실행하는 경우)
- FCM 설정을 위한 Firebase 프로젝트
- 실제 서버 연동 테스트를 위한 테스트 계정

### 6.2 프로젝트 가져오기

```bash
git clone https://github.com/2kim2/2026_hackathon.git
cd 2026_hackathon
```

### 6.3 프론트엔드 실행

1. Android Studio에서 `frontend/` 폴더를 엽니다.
2. Gradle 동기화를 완료합니다.
3. Firebase 설정 파일 `frontend/app/google-services.json`이 프로젝트 환경에 맞게 구성되어 있는지 확인합니다.
4. 에뮬레이터 또는 실제 기기를 선택하고 **Run**을 누릅니다.
5. 앱 사용 기록 접근 권한과 알림 권한을 허용합니다.
6. BE1 서버 주소와 테스트 계정으로 로그인한 뒤 모니터링을 시작합니다.

**BE1 배포 서버 주소:** `https://senior-guard-backend.onrender.com`

> 로그인 정보와 FCM 토큰 원문은 README·시연 영상에 공개하지 않습니다. 분석 요청은 로그인으로 발급된 인증 토큰을 사용하므로 **로그인 후 모니터링**해야 합니다.

### 6.4 백엔드 로컬 실행 (개발용)

BE1과 BE2는 각각 별도 Django 프로젝트입니다. 아래 명령은 프로젝트 내 `manage.py`와 `requirements.txt`를 기준으로 한 로컬 실행 예시이며, 환경 변수를 먼저 설정해야 합니다.

**BE1**

```bash
cd backend
python -m venv .venv
# 가상환경 활성화 후
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

주요 환경 변수: `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `BE2_ANALYSIS_URL`, `FIREBASE_CREDENTIALS_PATH`. 필요 시 `DATABASE_URL`, `DJANGO_DEBUG` 등을 지정합니다.

**BE2**

```bash
cd backend-security
python -m venv .venv
# 가상환경 활성화 후
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8001
```

주요 환경 변수: `DJANGO_SECRET_KEY`, `VIRUSTOTAL_API_KEY`(VirusTotal 사용 시).

> 로컬 개발 환경에서는 BE1의 `BE2_ANALYSIS_URL`을 BE2 실행 주소에 맞게 설정해야 합니다. Firebase Admin 서비스 계정 비공개 키, Django 비밀키, VirusTotal API 키는 GitHub에 업로드하지 않습니다.

## 7. 폴더 구조

```text
2026_hackathon/
├── frontend/                  # Android/Kotlin 앱
│   └── app/src/main/
│       └── java/com/example/seniorguard/
│           ├── MainActivity.kt
│           ├── MonitoringService.kt
│           ├── UsageEventMonitor.kt
│           ├── SnapshotCollector.kt
│           ├── DiagnosisSender.kt
│           ├── AuthManager.kt
│           ├── FCMTokenManager.kt
│           ├── FCMTokenSender.kt
│           └── SeniorGuardMessagingService.kt
├── backend/                   # BE1: 계정, 가족 연결, 진단, 알림 API
│   ├── accounts/
│   ├── applications/
│   ├── diagnoses/
│   ├── families/
│   ├── notifications/
│   └── config/
├── backend-security/          # BE2: 위험도 분석
│   ├── analyzer/
│   └── config/
└── README.md
```

## 8. 주요 구성 요소 및 API

### 8.1 Frontend

| 구성 요소 | 역할 |
| --- | --- |
| `MainActivity` 및 Compose 화면 | 권한 안내, 모니터링 시작·중지 등 사용자 흐름 |
| `UsageEventMonitor` | 사용 기록 접근 권한 확인 및 앱 실행 이벤트 조회 |
| `MonitoringService` | Foreground Service 기반 이벤트 감시·스냅샷 수집·분석 요청 연결 |
| `SnapshotCollector` | 패키지명·앱 권한·네트워크·화면 상태 수집 |
| `DiagnosisSender` | 인증 토큰으로 BE1 분석 API 호출, 응답 로그 기록, APK 해시 계산 |
| `AuthManager` | 로그인 및 서버 인증 정보 관리 |
| `FCMTokenManager` / `FCMTokenSender` | FCM 토큰 발급 및 서버 등록 |
| `SeniorGuardMessagingService` | 수신된 FCM 메시지 처리 및 안드로이드 알림 표시 |

### 8.2 Backend

- **BE1:** 계정 인증, 가족 연결, 앱·진단 데이터 관리, BE2 분석 요청 중계, 위험 진단 시 보호자 FCM 알림 발송 처리
- **BE2:** 앱 권한·실행 상태 분석, 위험 점수와 등급 산출, VirusTotal 조회 및 분석 결과 반환

### 8.3 주요 BE1 API

| 메서드 | 엔드포인트 | 기능 |
| --- | --- | --- |
| `POST` | `/api/accounts/login/` | 로그인 및 인증 토큰 발급 |
| `POST` | `/api/notifications/fcm-token/` | FCM 토큰 등록 |
| `POST` | `/api/diagnoses/analyze/` | 앱 사용 스냅샷 위험도 분석 요청 |
| `GET/POST` | `/api/diagnoses/` | 진단 결과 목록 조회·등록 |
| `POST` | `/api/families/codes/` | 가족 연결 코드 생성 |
| `POST` | `/api/families/requests/by-code/` | 연결 코드로 가족 연결 요청 |

> API에 따라 로그인 인증이 필요합니다. 분석 API는 `Authorization: Token <인증 토큰>` 헤더를 사용합니다.

## 9. 실행 및 테스트 결과

### 9.1 앱 모니터링

1. 앱을 실행하고 사용 기록 접근 권한을 허용합니다.
2. 로그인 후 모니터링을 시작합니다.
3. 홈 화면으로 이동해 Chrome 등 다른 앱을 실행합니다.
4. Android Studio Logcat에서 `SeniorGuardSnapshot`으로 필터링합니다.
5. 패키지명, 이벤트 발생 시각, 앱 권한 수, 네트워크·화면 상태가 기록되는지 확인합니다.

**결과:** 앱 실행 이벤트 감지 및 스냅샷 수집 정상 작동 확인.

### 9.2 위험도 분석 API 통합 테스트

1. BE1 서버에 로그인한 상태에서 모니터링을 시작합니다.
2. Chrome을 실행해 앱 사용 이벤트를 발생시킵니다.
3. Logcat에서 `SeniorGuardDiagnosis`로 필터링합니다.
4. 분석 성공 로그와 응답 필드를 확인합니다.

**실제 확인 로그 (2026-11-07)**

```text
분석 완료: 앱=com.android.chrome, 등급=safe, 점수=10,
요약=특별한 위험 징후가 발견되지 않았습니다., VirusTotal=completed
```

**결과:** **FE → BE1 → BE2 → FE** 분석 요청·응답 성공. 최초 요청에서 BE2 연결 문제로 HTTP 502가 발생했으나, 이후 요청에서 정상 분석 결과를 확인했습니다.

### 9.3 FCM 푸시 알림 테스트

1. 테스트 계정으로 로그인합니다.
2. 앱에서 FCM 토큰을 발급받고 BE1 서버에 등록합니다.
3. 백엔드에서 테스트 메시지를 수동 발송합니다.
4. 안드로이드 기기에서 알림 수신 여부를 확인합니다.

**결과:** FCM 토큰 발급, 서버 등록(HTTP 200 확인), 실제 푸시 알림 수신 성공.

### 9.4 통합 검증 현황

| 항목 | 상태 |
| --- | --- |
| 앱 사용 이벤트 감지 | ✅ 실제 테스트 성공 |
| 스냅샷 수집 | ✅ 실제 테스트 성공 |
| 로그인 및 FCM 토큰 등록 | ✅ 실제 테스트 성공 |
| FE → BE1 분석 API 호출 | ✅ 실제 테스트 성공 |
| BE1 → BE2 분석 결과 반환 | ✅ 실제 테스트 성공 |
| 위험 점수·등급·VirusTotal 결과 확인 | ✅ 실제 테스트 성공 |
| FCM 수동 테스트 메시지 수신 | ✅ 실제 테스트 성공 |
| `danger` 판정 후 연결된 보호자에게 자동 푸시 수신 | ⏳ 코드 구현, 전체 시나리오 실측 미완료 |

> 테스트 완료는 실제 확인한 범위만 의미합니다. `danger` 자동 알림은 백엔드 처리 코드가 있어도 보호자 기기까지 이어지는 종단 간 시나리오는 별도로 검증해야 합니다.

---

**GitHub Repository:** https://github.com/2kim2/2026_hackathon
