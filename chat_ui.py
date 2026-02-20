# -*- coding: utf-8 -*-
"""
로컬 Ollama 채팅 UI
실행 후 브라우저에서 채팅창처럼 사용할 수 있습니다.
사용 전에 터미널에서 'ollama serve' 를 먼저 실행해 두세요.
한국어가 깨지면: MODEL 을 한국어 특화 모델로 바꾸거나, 아래 SYSTEM_PROMPT 가 적용된 상태로 사용하세요.
"""

import requests
import gradio as gr

# 사용할 모델: 속도·품질 균형 (빠른 답변 + 괜찮은 성능)
# 처음 한 번만 터미널에서: ollama pull qwen2.5:7b
MODEL = "qwen2.5:7b"
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"

# 잼민이 이름 + 한국어만 사용 (중국어 금지)
SYSTEM_PROMPT = (
    "당신의 이름은 잼민이입니다. 누가 이름을 물어보면 반드시 '저는 잼민이예요'라고 소개하세요. "
    "당신은 친절한 한국어 AI 어시스턴트입니다. "
    "모든 답변을 반드시 한국어(한글)로만 작성하세요. 중국어(中文)는 절대 사용하지 마세요. 영어나 다른 언어도 섞지 말고, 오직 한글만 사용하세요."
)


def chat(message, history):
    """사용자 메시지를 Ollama에 보내고 답변을 받아 반환합니다."""
    if not message or not message.strip():
        return ""
    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message.strip()},
        ]
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": messages,
                "stream": False,
            },
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()
        reply = data.get("message", {}).get("content", "답변을 받지 못했습니다.")
        # 혹시 인코딩 문제가 있으면 UTF-8 로 보장
        if isinstance(reply, bytes):
            reply = reply.decode("utf-8", errors="replace")
        return reply
    except requests.exceptions.ConnectionError:
        return "연결 실패: Ollama 서버가 떠 있는지 확인하세요. 터미널에서 'ollama serve' 를 실행한 뒤 다시 시도하세요."
    except Exception as e:
        return f"오류 발생: {str(e)}"


# 다크 테마: 하얀 영역 제거, 채팅창 전체 어둡게, 글자 잘 보이게
DARK_CSS = """
/* 전체 바탕 */
.gradio-container, body { background: #161618 !important; min-height: 100vh !important; }
/* 메인 카드 + 그 안 모든 영역 어둡게 (하얀 부분 제거) */
.contain, .main, [class*="container"],
.contain *, .main *, .gradio-container .contain,
[class*="block"], [class*="panel"], section {
    background: #252529 !important;
    background-color: #252529 !important;
}
/* 채팅 메시지 표시 영역 (하얀 배경 나오는 부분 강제 제거) */
[class*="chatbot"], [class*="chatbot"] > div, [class*="chatbot"] div,
[class*="chat"], [class*="message"], .wrap, [class*="wrap"],
[class*="scroll"], .scroll-hide, [class*="scroll-hide"],
[class*="svelte"] {
    background: #252529 !important;
    background-color: #252529 !important;
    color: #e4e4e7 !important;
}
/* 메인 컨테이너 테두리만 유지 */
.contain, .main { border-radius: 12px !important; border: 1px solid #2d2d32 !important; }
/* 사용자/봇 말풍선 */
[class*="message"].user, [class*="user"] { background: #2a2a2e !important; color: #e4e4e7 !important; }
[class*="message"].assistant, [class*="assistant"] { background: #252529 !important; color: #e4e4e7 !important; }
/* 대화 글자 - 잘 보이게 */
.message, .user, .assistant, [class*="message"] *, [class*="chatbot"] *,
.markdown, .prose, .prose p, .prose li, [class*="markdown"] { color: #e4e4e7 !important; }
.markdown a, .prose a { color: #a5b4fc !important; }
h1, h2, label, .caption { color: #a1a1aa !important; }
/* 입력창 */
input, textarea, [class*="input"] { 
    background: #252529 !important; color: #e4e4e7 !important; 
    border: 1px solid #3f3f46 !important; border-radius: 8px !important;
}
input::placeholder, textarea::placeholder { color: #71717a !important; }
button { background: #3f3f46 !important; color: #e4e4e7 !important; border-radius: 8px !important; }
button:hover { background: #52525b !important; }
"""


# 답변 후에도 입력창 포커스 유지 (Enter 치면 계속 여기 커서 유지)
FOCUS_INPUT_JS = """
<div style="display:none;">
<script>
(function() {
  var lastUpdate = Date.now();
  function focusInput() {
    var root = document.querySelector('.gradio-container') || document.body;
    var ta = root.querySelector('textarea');
    if (!ta) ta = root.querySelector('input[type="text"]');
    if (ta && ta.offsetParent) { ta.focus(); return true; }
    return false;
  }
  function scheduleFocus() {
    lastUpdate = Date.now();
    [200, 500, 900, 1400, 2000, 2800, 3600].forEach(function(ms) {
      setTimeout(focusInput, ms);
    });
  }
  var container = document.querySelector('.gradio-container') || document.body;
  var observer = new MutationObserver(function() { scheduleFocus(); });
  observer.observe(container, { childList: true, subtree: true });
  setInterval(function() {
    if (Date.now() - lastUpdate < 8000) {
      var ta = container.querySelector('textarea') || container.querySelector('input[type="text"]');
      if (ta && document.activeElement !== ta) focusInput();
    }
  }, 600);
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') scheduleFocus();
  });
  scheduleFocus();
})();
</script>
</div>
"""

# Gradio: 잼민이 챗봇 + 어두운 테마 + 입력창 자동 포커스
with gr.Blocks(css=DARK_CSS, title="잼민이") as demo:
    gr.HTML(FOCUS_INPUT_JS)
    gr.ChatInterface(
        fn=chat,
        title="잼민이",
        description="메시지 입력 후 Enter. 답변 후 자동으로 입력창에 커서가 있으니 그대로 다음 말 입력하면 됩니다. (사용 전 터미널에서 ollama serve 실행)",
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
