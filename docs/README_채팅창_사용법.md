# 로컬 Ollama 채팅창 UI 사용법

터미널 대신 **브라우저에서 채팅창처럼** 쓰는 방법입니다.

---

## 1. 준비 (한 번만)

### 1) Ollama 서버 켜기

터미널에서 **먼저** 실행하고 그대로 두세요.

```bash
ollama serve
```

### 2) 채팅 UI용 패키지 설치 (한 번만)

**새 터미널 탭**을 열고:

```bash
cd /home/Local_Chatbot_Ollama
pip install -r requirements_chat_ui.txt
```

---

## 2. 채팅창 실행

같은 폴더에서:

```bash
python chat_ui.py
```

- 터미널에 `Running on local URL: http://127.0.0.1:7860` 이 나오면 성공입니다.
- **브라우저**에서 http://127.0.0.1:7860 로 접속하세요.

### GPU 서버에 SSH로 접속해서 쓰는 경우

채팅창은 서버의 7860 포트에서 떠 있습니다. **본인 PC**에서 브라우저로 보려면 **SSH 터널**이 필요합니다.

**본인 PC** 터미널에서:

```bash
ssh -L 7860:127.0.0.1:7860 사용자명@서버주소
```

서버에 접속된 상태에서, **본인 PC 브라우저**에 http://127.0.0.1:7860 입력하면 채팅창이 열립니다.

---

## 3. 사용 방법

- 채팅창에 메시지 입력 후 Enter (또는 전송 버튼).
- 로컬 Ollama가 답변을 생성해 같은 창에 표시됩니다.
- 모델을 바꾸려면 `chat_ui.py` 안의 `MODEL = "llama3.2:3b"` 를 원하는 모델명(예: `llama3.1:8b`)으로 수정한 뒤 다시 실행하면 됩니다.

---

## 4. 한국어가 깨지거나 영어가 섞일 때

**원인**: 사용 중인 모델(예: llama3.2:3b)이 한국어에 약해 한글이 깨지거나 영어·기호가 섞여 나올 수 있습니다.

**해결 방법** (둘 중 하나 또는 둘 다):

### 4-1. 시스템 프롬프트 사용 (이미 적용됨)

`chat_ui.py` 에 **한국어만 쓰라**는 시스템 지시가 들어 있습니다.  
그대로 실행해 보시고, 여전히 깨지면 아래 4-2처럼 **한국어 특화 모델**로 바꿔 보세요.

### 4-2. 한국어에 강한 모델로 변경

Ollama에서 한국어를 더 잘 하는 모델을 받아서 `chat_ui.py` 의 `MODEL` 만 바꾸면 됩니다.

**방법 A — Ollama에서 바로 받기 (간단)**

터미널에서 아래 중 하나 실행해서 모델을 받은 뒤, `chat_ui.py` 안에서 `MODEL = "..."` 만 해당 이름으로 수정하세요.

```bash
# Qwen 2.5 (한국어 지원 좋음, 3B는 가벼움)
ollama pull qwen2.5:3b
```

`chat_ui.py` 에서: `MODEL = "qwen2.5:3b"`

```bash
# Gemma2 (한국어 괜찮음)
ollama pull gemma2:2b
```

`chat_ui.py` 에서: `MODEL = "gemma2:2b"`

**방법 B — EEVE-Korean (한국어 전용, 설정 조금 더 필요)**

야놀자에서 만든 **EEVE-Korean** 은 한국어 전용 모델입니다.  
Hugging Face에서 GGUF 파일을 받아 Modelfile 로 Ollama에 등록해야 합니다.

- 검색어: **Ollama EEVE-Korean** 또는 **EEVE-Korean GGUF Hugging Face**
- 설치 후 `chat_ui.py` 에서 `MODEL = "EEVE-Korean-10.8B"` 처럼 등록한 이름으로 설정하면 됩니다.

---

## 5. 다른 선택지: Open WebUI

더 많은 기능(대화 저장, 여러 모델 선택 등)이 필요하면 **Open WebUI**를 쓰는 방법도 있습니다.  
Ollama와 연결되는 웹 UI라서, ChatGPT처럼 쓰기 편합니다.

- 검색어: **Open WebUI Ollama**
- 설치 방법은 공식 문서(Docker 또는 pip)를 따라 하시면 됩니다.

현재 만든 `chat_ui.py`는 **설치가 가볍고, 프로그램 키면 채팅창 하나만 나오는** 버전입니다.
