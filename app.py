from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Session-Speicherung für Nutzer (optional für Erweiterungen)
user_sessions = {}

# Mehrsprachige FAQs
faqs = {
    'de': {
        "1": "Unsere Lieferzeit beträgt 2–4 Werktage.",
        "2": "Du kannst Produkte innerhalb von 14 Tagen zurückgeben.",
        "3": "Unsere Öffnungszeiten sind Mo–Fr 09–17 Uhr."
    },
    'en': {
        "1": "Our delivery time is 2–4 business days.",
        "2": "You can return products within 14 days.",
        "3": "Our opening hours are Mon–Fri 9am–5pm."
    },
    'tr': {
        "1": "Teslimat süresi 2–4 iş günüdür.",
        "2": "Ürünleri 14 gün içinde iade edebilirsiniz.",
        "3": "Çalışma saatlerimiz Pazartesi–Cuma 09:00–17:00 arasıdır."
    }
}

# Menü je Sprache
def get_menu(lang):
    return {
        "de": "Wie kann ich dir helfen?\n1️⃣ Lieferung\n2️⃣ Rückgabe\n3️⃣ Öffnungszeiten",
        "en": "How can I help you?\n1️⃣ Delivery\n2️⃣ Return\n3️⃣ Opening hours",
        "tr": "Size nasıl yardımcı olabilirim?\n1️⃣ Teslimat\n2️⃣ İade\n3️⃣ Çalışma saatleri"
    }.get(lang, "")

# Fallback-Text je Sprache
def get_fallback(lang):
    return {
        "de": "Ich leite deine Nachricht an unser Support-Team weiter.",
        "en": "Forwarding your message to our support team.",
        "tr": "Mesajınız destek ekibine iletiliyor."
    }.get(lang, "")

# Haupt-Logik des Chatbots
def get_bot_response(message, sender_id="web_user"):
    session = user_sessions.get(sender_id, {})
    lang = session.get("lang")

    if not lang:
        if message == "1":
            lang = "de"
        elif message == "2":
            lang = "en"
        elif message == "3":
            lang = "tr"
        else:
            return "Bitte wähle eine Sprache:\n1️⃣ Deutsch\n2️⃣ English\n3️⃣ Türkçe"
        user_sessions[sender_id] = {"lang": lang}
        return get_menu(lang)

    if message in ["1", "2", "3"]:
        return faqs[lang].get(message, get_fallback(lang))

    return get_fallback(lang)

# Flask-Endpunkt
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    response = get_bot_response(message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
