"""
Marathi Personal AI (मराठी एआय)
- General chatbot: ask anything, in Marathi / English / Hinglish
- Optional: knows your ~4600 schemes if you put them in schemes.csv
- Remembers chat between runs (chat_history.json)

Setup:
    pip install anthropic
    set ANTHROPIC_API_KEY=your_key      (Windows)
    export ANTHROPIC_API_KEY=your_key   (Mac/Linux)
    python marathi_ai.py
"""

import csv
import json
import os
import re
import sys
from pathlib import Path

import anthropic

MODEL = "claude-sonnet-5-5"
HISTORY_FILE = Path("chat_history.json")
SCHEMES_FILE = Path("schemes.csv")   # optional; any columns are fine
MAX_TURNS_KEPT = 20                  # last N messages sent to the AI
TOP_SCHEMES = 5

SYSTEM_PROMPT = """तू 'मराठी एआय' आहेस — वापरकर्त्याचा वैयक्तिक सहाय्यक.
- वापरकर्ता ज्या भाषेत लिहितो त्याच भाषेत उत्तर दे. डिफॉल्ट भाषा: सोपी, स्पष्ट मराठी.
- कोणताही विषय चालेल: अभ्यास, विज्ञान, कोडिंग, गप्पा, सल्ला, लेखन, इत्यादी.
- उत्तरे लहान आणि समजायला सोपी ठेव; गरज असेल तेव्हाच सविस्तर सांग.
- तुला माहीत नसेल तर तसे प्रामाणिकपणे सांग, अंदाजे माहिती खरी म्हणून सांगू नकोस.
- जर संदर्भात [योजना माहिती] दिली असेल आणि प्रश्न योजनांबद्दल असेल, तरच ती वापर.
  प्रश्न योजनांचा नसेल तर ती माहिती दुर्लक्षित करून सामान्यपणे उत्तर दे.
- योजनेचे नियम/तारखा बदलू शकतात, त्यामुळे अर्ज करण्यापूर्वी अधिकृत वेबसाइट तपासायला सांग.
"""

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY


# ---------- Schemes (optional) ----------
def tokenize(text: str):
    return set(re.findall(r"[\w\u0900-\u097F]+", text.lower()))


def load_schemes():
    if not SCHEMES_FILE.exists():
        return []
    rows = []
    with SCHEMES_FILE.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            text = " | ".join(f"{k}: {v}" for k, v in row.items() if v)
            rows.append((tokenize(text), text))
    print(f"✅ {len(rows)} योजना लोड झाल्या.")
    return rows


def find_schemes(schemes, question):
    q = tokenize(question)
    if not q or not schemes:
        return ""
    scored = []
    for tokens, text in schemes:
        score = len(q & tokens)
        if score >= 2:  # needs at least 2 matching words
            scored.append((score, text))
    scored.sort(key=lambda x: x[0], reverse=True)
    if not scored:
        return ""
    best = "\n".join(f"- {t[:700]}" for _, t in scored[:TOP_SCHEMES])
    return f"[योजना माहिती]\n{best}\n[/योजना माहिती]\n\n"


# ---------- History ----------
def load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return []


def save_history(history):
    HISTORY_FILE.write_text(
        json.dumps(history, ensure_ascii=False, indent=1), encoding="utf-8"
    )


def trimmed(history):
    msgs = history[-MAX_TURNS_KEPT:]
    while msgs and msgs[0]["role"] != "user":  # must start with user
        msgs = msgs[1:]
    return msgs


# ---------- Chat ----------
def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("❌ ANTHROPIC_API_KEY सेट करा (वरच्या सूचना पहा).")

    schemes = load_schemes()
    history = load_history()

    print("🙏 नमस्कार! मी तुमचा मराठी एआय आहे. काहीही विचारा.")
    print("   आदेश: /new = नवीन चॅट, /exit = बाहेर पडा\n")

    while True:
        try:
            user_text = input("तुम्ही: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nनमस्कार!")
            break

        if not user_text:
            continue
        if user_text == "/exit":
            print("नमस्कार! 🙏")
            break
        if user_text == "/new":
            history = []
            save_history(history)
            print("🆕 नवीन चॅट सुरू.\n")
            continue

        # Add scheme context only for this turn (not stored in history)
        context = find_schemes(schemes, user_text)
        history.append({"role": "user", "content": user_text})
        messages = trimmed(history)
        messages[-1] = {"role": "user", "content": context + user_text}

        print("एआय: ", end="", flush=True)
        reply = ""
        try:
            with client.messages.stream(
                model=MODEL,
                max_tokens=1500,
                system=SYSTEM_PROMPT,
                messages=messages,
            ) as stream:
                for chunk in stream.text_stream:
                    reply += chunk
                    print(chunk, end="", flush=True)
            print("\n")
        except anthropic.APIError as e:
            print(f"\n⚠️ त्रुटी: {e}\n")
            history.pop()
            continue

        history.append({"role": "assistant", "content": reply})
        save_history(history)


if __name__ == "__main__":
    main()
