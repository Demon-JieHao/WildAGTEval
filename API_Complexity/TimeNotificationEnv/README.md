# Time Notification Environment (TimeNotificationEnv)

TimeNotificationEnv는 시간 기반 알림, 리마인더 및 알람을 관리하기 위한 환경을 제공합니다. 이 환경은 다른 환경들(SmartHomeEnv, MediaControlEnv 등)과 통합되어 종합적인 알림 시스템을 구현합니다.

## 주요 기능

- **알람 관리**: 특정 시간과 요일에 반복되는 알람 설정
- **리마인더 관리**: 특정 날짜와 시간에 알림을 제공하는 일회성 리마인더
- **알림 관리**: 다양한 환경에서 발생하는 알림 메시지 수집 및 표시
- **사용자 환경 설정**: 방해 금지 모드, 알림음 등의 사용자별 알림 설정

## 도구 목록

TimeNotificationEnv는 다음과 같은 도구를 제공합니다:

### 알람 관리
- `create_alarm`: 새로운 알람 생성
- `get_alarms`: 사용자의 알람 목록 조회
- `delete_alarm`: 알람 삭제 또는 비활성화

### 리마인더 관리
- `create_reminder`: 새로운 리마인더 생성
- `get_reminders`: 사용자의 리마인더 목록 조회

### 알림 관리
- `create_notification`: 새로운 알림 생성
- `get_notifications`: 사용자의 알림 목록 조회
- `set_notification_preferences`: 알림 설정 변경

## 사용 예제

### 알람 생성
```python
# 평일 오전 7시 알람 생성
result = invoke_tool("create_alarm", 
                    title="아침 기상", 
                    time="07:00:00", 
                    days=["monday", "tuesday", "wednesday", "thursday", "friday"],
                    sound="cheerful")

# 특정 장치에서 울리는 알람 생성
result = invoke_tool("create_alarm",
                    title="아침 운동",
                    time="06:00:00",
                    days=["monday", "wednesday", "friday"],
                    device_endpoint="12")  # Smart Phone 장치
```

### 리마인더 생성
```python
# 30분 전에 알림을 주는 리마인더 생성
result = invoke_tool("create_reminder",
                    title="의사 예약",
                    date="2025-06-20",
                    time="14:00:00",
                    description="연간 건강 검진",
                    notify_before_minutes=30)

# 하루 전에 알림을 주는 리마인더 생성
result = invoke_tool("create_reminder",
                    title="프로젝트 마감일",
                    date="2025-07-01",
                    time="17:00:00",
                    notify_before_minutes=1440)  # 24시간(1일) 전
```

### 알람 및 리마인더 조회
```python
# 모든 활성 알람 조회
result = invoke_tool("get_alarms", active_only=True)

# 특정 기간의 리마인더 조회
result = invoke_tool("get_reminders",
                    status="pending",
                    date_from="2025-06-01",
                    date_to="2025-06-30")
```

### 알림 관리
```python
# 알림 생성
result = invoke_tool("create_notification",
                    title="새 기기 등록됨",
                    message="새로운 스마트 스피커가 네트워크에 등록되었습니다.",
                    priority="normal")

# 최근 알림 조회
result = invoke_tool("get_notifications",
                    limit=10,
                    include_read=False)

# 방해 금지 모드 설정
result = invoke_tool("set_notification_preferences",
                    do_not_disturb=True,
                    notification_sounds=False)
```

## 다른 환경과의 통합

TimeNotificationEnv는 다음과 같이 다른 환경들과 통합됩니다:

- **SmartHomeEnv**: 알람 시 조명 켜기, 커튼 열기 등의 동작 연동
- **MediaControlEnv**: 알람 시 특정 음악이나 소리 재생
- **CommunicationController**: 알림을 메시지로 전달
- **InformationControlEnv**: 날씨 정보를 포함한 아침 알람 등 정보와 알림 연계
- **CulinaryControlEnv**: 요리 타이머나 식사 시간 알림

## 데이터 모델

TimeNotificationEnv는 다음과 같은 주요 데이터 구조를 사용합니다:

- `alarms.json`: 사용자별 알람 정보 저장
- `reminders.json`: 사용자별 리마인더 정보 저장
- `notifications.json`: 시스템 및 애플리케이션 알림 내역 저장
