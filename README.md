# Şirket Çalışanları AI Analiz Projesi 🤖📊

Bu proje, şirket çalışanlarının haftalık giriş-çıkış saatlerini analiz eden ve doğal dilde soruları yanıtlayan bir yapay zeka destekli sohbet sistemidir.  
Kullanıcılar, web arayüzü üzerinden çalışanlara dair sorular sorabilir; sistem ise Excel tabanlı verileri inceleyerek anlamlı ve insani yanıtlar üretir.

## 🎯 Amaç

- Şirket personelinin işe giriş ve çıkış saatlerini analiz etmek  
- Kullanıcının doğal dilde sorduğu soruları anlamak  
- LLM (Large Language Model) ile mantıklı, bağlamsal ve insani cevaplar üretmek  
- Veritabanı üzerinden oturum yönetimi ve geçmiş sohbetleri saklamak  
- Qdrant ile embedding tabanlı veri arama desteği sağlamak

---

## 🧠 Sistem Özeti

- **Backend:** Flask tabanlı Python uygulaması  
- **LLM Entegrasyonu:** Local LLM (örneğin LlamaCpp) ile prompt tabanlı yanıt üretimi  
- **Veri Kaynağı:** Excel dosyası üzerinden personel verisi  
- **Veritabanı:** SQLite + SQLAlchemy ile oturum ve mesaj yönetimi  
- **Frontend:** HTML + CSS ile sade ve insansı chat arayüzü  
- **Embedding & Arama:** Qdrant ile semantik veri eşleştirme


