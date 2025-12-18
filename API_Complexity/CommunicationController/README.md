# Communication Controller

Communication Controller는 사용자의 연락처, 통화 및 메시지 기능을 관리하는 환경입니다. 이 컨트롤러는 다른 환경들(SmartHomeEnv, MediaControlEnv 등)과 통합되어 통신 기능을 제공합니다.

## 주요 기능

### 1. 연락처 관리
- 이름, 전화번호 또는 이메일로 연락처 검색 (`find_contact`)

### 2. 통화 기능
- 연락처나 전화번호로 통화 시작 (`make_call`)
- 현재 진행 중인 통화 종료 (`end_call`)
- 통화 기록 조회 (`get_call_history`)

### 3. 메시지 기능
- 연락처에 텍스트 메시지 전송 (`send_message`)
- 특정 연락처와의 메시지 기록 조회 (`get_messages`)

### 4. 장치 관리
- 통화 기능을 지원하는 장치 검색 (`find_call_device`)

## API 사용 예시

### 연락처 검색
```python
# 이름으로 검색
result = invoke_tool("find_contact", query="Alice", search_type="name")

# 전화번호로 검색
result = invoke_tool("find_contact", query="555", search_type="phone")

# 이메일로 검색
result = invoke_tool("find_contact", query="@example.com", search_type="email")
```

### 통화 관리
```python
# 통화 시작
result = invoke_tool("make_call", contact_id="contact1", device_endpoint="4", call_type="audio")

# 통화 종료
result = invoke_tool("end_call")

# 통화 기록 조회
result = invoke_tool("get_call_history", limit=5)
```

### 메시지 관리
```python
# 메시지 보내기
result = invoke_tool("send_message", contact_id="contact1", content="안녕하세요!")

# 특정 연락처와의 메시지 기록 조회
result = invoke_tool("get_messages", contact_id="contact1", limit=10)

# 모든 연락처의 메시지 기록 조회
result = invoke_tool("get_messages", limit=20)
```

### 장치 검색
```python
# 모든 통화 가능 장치 찾기
result = invoke_tool("find_call_device")

# 특정 이름으로 장치 찾기
result = invoke_tool("find_call_device", device_name="Smart Phone")

# 특정 엔드포인트로 장치 찾기
result = invoke_tool("find_call_device", endpoint="12")
```

## 데이터 구조

CommunicationController는 다음과 같은 데이터 구조를 사용합니다:

1. **연락처 (contacts)**
   - 사용자별 연락처 정보 (이름, 전화번호, 이메일 등)

2. **통화 기록 (call_history)**
   - 발신/수신 통화 기록 (시간, 지속시간, 상태 등)

3. **메시지 기록 (message_history)**
   - 발신/수신 메시지 기록 (내용, 시간, 읽음 상태 등)

## 보안 및 개인정보

- 모든 통신 기능은 사용자별로 분리되어 있어, 다른 사용자의 데이터에 접근할 수 없습니다.
- 사용자는 자신의 연락처, 통화 기록, 메시지만 볼 수 있습니다.
