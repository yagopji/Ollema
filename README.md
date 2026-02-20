# 🤖 Ollama 로컬 챗봇 UI

로컬 Ollama 모델을 브라우저에서 채팅창처럼 사용할 수 있는 웹 인터페이스입니다.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/gradio-4.0+-green.svg)](https://gradio.app/)

---

## ✨ 주요 기능

- 💬 **브라우저 기반 채팅 UI**: 터미널 대신 웹에서 대화
- 🌐 **한국어 지원**: 한국어 특화 모델 및 시스템 프롬프트
- 🎨 **다크 테마**: 눈에 편안한 어두운 인터페이스
- ⚡ **빠른 응답**: 로컬 모델로 지연 없는 대화
- 🔧 **모델 선택**: 다양한 Ollama 모델 지원

---

## 🚀 빠른 시작

### 1. 필수 요구사항

- Python 3.8 이상
- Ollama 설치됨 ([설치 가이드](scripts/ollama_install.sh))

### 2. 설치 및 실행

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. Ollama 서버 실행 (별도 터미널)
ollama serve

# 3. 채팅 UI 실행
python chat_ui.py
```

### 3. 브라우저 접속

```
http://127.0.0.1:7860
```

---

## 📁 프로젝트 구조

```
Ollema/
├── README.md                          # 이 파일
├── requirements.txt                   # Python 패키지 의존성
├── chat_ui.py                        # 메인 채팅 UI 프로그램
├── .gitignore                        # Git 제외 파일
│
├── docs/                             # 📚 문서
│   ├── README_채팅창_사용법.md       # 상세 사용 가이드
│   └── 모델_성능_업그레이드_가이드.md # 모델 선택 가이드
│
└── scripts/                          # 🔧 스크립트
    └── ollama_install.sh             # Ollama 설치 스크립트
```

---

## 📦 설치 방법

### 방법 1: 자동 설치

```bash
# Ollama 설치
bash scripts/ollama_install.sh

# Python 패키지 설치
pip install -r requirements.txt
```

### 방법 2: 수동 설치

**Ollama 설치**:
- Linux/Mac: `bash scripts/ollama_install.sh`
- 또는 공식 사이트: https://ollama.ai

**Python 패키지**:
```bash
pip install gradio>=4.0.0 requests>=2.28.0
```

---

## 💡 사용 방법

### 기본 사용

1. **Ollama 서버 실행** (별도 터미널):
   ```bash
   ollama serve
   ```

2. **채팅 UI 실행**:
   ```bash
   python chat_ui.py
   ```

3. **브라우저에서 접속**: http://127.0.0.1:7860

4. **메시지 입력 후 Enter**: 답변 후 자동으로 입력창에 포커스 유지

### 모델 변경

`chat_ui.py` 파일에서 `MODEL` 변수를 수정:

```python
MODEL = "qwen2.5:7b"  # 원하는 모델로 변경
```

**추천 모델**:
- **속도 우선**: `qwen2.5:7b`, `llama3.1:8b`
- **성능 우선**: `deepseek-r1:32b`, `qwen2.5:32b`

자세한 모델 정보는 [모델 가이드](docs/모델_성능_업그레이드_가이드.md)를 참고하세요.

---

## 🌐 원격 서버 사용 (SSH)

GPU 서버에 SSH로 접속해서 사용하는 경우:

```bash
# 본인 PC에서 SSH 터널 생성
ssh -L 7860:127.0.0.1:7860 사용자명@서버주소

# 서버에서 chat_ui.py 실행 후
# 본인 PC 브라우저에서 http://127.0.0.1:7860 접속
```

---

## 📚 문서

- **[사용 가이드](docs/README_채팅창_사용법.md)**: 상세한 사용 방법 및 문제 해결
- **[모델 가이드](docs/모델_성능_업그레이드_가이드.md)**: 모델 선택 및 성능 비교

---

## ⚙️ 설정

### 시스템 프롬프트 변경

`chat_ui.py`에서 `SYSTEM_PROMPT` 변수 수정:

```python
SYSTEM_PROMPT = "당신은 친절한 AI 어시스턴트입니다..."
```

### 포트 변경

```python
demo.launch(server_name="127.0.0.1", server_port=7860)  # 포트 번호 변경
```

### 테마 변경

`chat_ui.py`의 `DARK_CSS` 변수에서 색상 수정 가능

---

## 🔧 문제 해결

### "연결 실패" 오류

**원인**: Ollama 서버가 실행되지 않음

**해결**:
```bash
# 별도 터미널에서 실행
ollama serve
```

### 한국어가 깨짐

**원인**: 모델이 한국어에 약함

**해결**:
1. 한국어 특화 모델 사용:
   ```bash
   ollama pull qwen2.5:7b
   ```
2. `chat_ui.py`에서 모델 변경:
   ```python
   MODEL = "qwen2.5:7b"
   ```

### 모델을 찾을 수 없음

**해결**: 먼저 모델을 다운로드:
```bash
ollama pull 모델명
```

---

## 🎯 추천 모델

| 용도 | 모델 | 명령어 |
|------|------|--------|
| **속도 우선** | Qwen 2.5 7B | `ollama pull qwen2.5:7b` |
| **성능 우선** | DeepSeek-R1 32B | `ollama pull deepseek-r1:32b` |
| **균형** | Qwen 2.5 32B | `ollama pull qwen2.5:32b` |

자세한 비교는 [모델 가이드](docs/모델_성능_업그레이드_가이드.md) 참고

---

## 🔗 참고 링크

- **Ollama 공식**: https://ollama.ai
- **Gradio 문서**: https://gradio.app
- **모델 라이브러리**: https://ollama.ai/library

---

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---

## 🤝 기여

버그 리포트, 기능 제안, Pull Request를 환영합니다!

---

**시작하기**: `ollama serve` → `python chat_ui.py` → 브라우저 접속 🚀
