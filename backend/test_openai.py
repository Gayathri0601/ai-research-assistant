from openai import OpenAI

# 👉 paste your SAME API key here
client = OpenAI(api_key="sk-PASTE-YOUR-KEY-HERE")

print("Testing Chat API...")

try:
    chat = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say hello"}]
    )
    print("✅ Chat API works")
except Exception as e:
    print("❌ Chat API failed:", e)


print("\nTesting Embeddings API...")

try:
    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input="hello"
    )
    print("✅ Embeddings API works")
except Exception as e:
    print("❌ Embeddings API failed:", e)