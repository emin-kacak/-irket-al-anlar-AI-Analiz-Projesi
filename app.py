from flask import Flask, request, render_template, jsonify
from llama_model import generate_response
from embedding import search_documents, create_collection
from data_loader import load_documents
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
db = SQLAlchemy(app)
class Session(db.Model):
    id = db.Column(db.String, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String, db.ForeignKey('session.id'))
    sender = db.Column(db.String)
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Başlangıçta veriyi yükle ve Qdrant'a ekle
documents = load_documents("01-07-2025.xlsx")
create_collection(documents)
print("Toplam veri:", len(documents))
results = search_documents("giriş yapan personel")
print("Arama sonucu:", results)

# HTML tabanlı chat arayüzü
@app.route("/", methods=["GET", "POST"])
def chat_page():
    response = ""
    
    if request.method == "POST":
        user_input = request.form["message"]
        relevant_info = search_documents(user_input)
        prompt = f"Kullanıcı: {user_input}\nİlgili Bilgiler: {relevant_info}\nYanıt:"
        response = generate_response(prompt)
    return render_template("chat.html", response=response)

def requires_full_context(user_input):
    keywords = ["kim", "daha erken", "en geç", "karşılaştır", "hepsi"]
    return any(k in user_input.lower() for k in keywords)
@app.route("/new_session", methods=["GET"])
def new_session():
    session_id = str(uuid.uuid4())
    new_session = Session(id=session_id)
    db.session.add(new_session)
    db.session.commit()
    return jsonify({"session_id": session_id})

@app.route("/history/<session_id>", methods=["GET"])
def get_history(session_id):
    messages = Message.query.filter_by(session_id=session_id).order_by(Message.timestamp).all()
    history = [{"sender": m.sender, "message": m.message} for m in messages]
    return jsonify(history)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    session_id = data.get("session_id")
    user_input = data.get("message")

    # Excel'den gelen tüm veriyi gönder
    relevant_info = "\n".join(documents)

    # LLM için sistem prompt
    system_prompt = """
    Sen bir Türkçe konuşan yapay zeka asistansın. Görevin, haftalık çalışma verilerini analiz etmek ve kullanıcının sorularını anlamlı şekilde yanıtlamaktır.

Aşağıda personel verileri verilmiştir.  
Kullanıcının sorusuna göre saatleri karşılaştır, isimleri ayıkla ve mantıklı cevap ver.

Uydurma bilgi verme, ama mantıklı tahminlerde bulunabilirsin.  
Yanıtların Türkçe, açık ve anlaşılır olsun.
"""

    # LLM prompt oluştur
    prompt = f"{system_prompt}\n\nPersonel Verileri:\n{relevant_info}\n\nSoru:\n{user_input}\n\nYanıt:"

    # Yanıt üret
    response = generate_response(prompt)

    # Veritabanına kaydet
    db.session.add(Message(session_id=session_id, sender="user", message=user_input))
    db.session.add(Message(session_id=session_id, sender="bot", message=response))
    db.session.commit()

    return jsonify({"response": response})

    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
