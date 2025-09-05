import pandas as pd

def load_documents(excel_path):
    df = pd.read_excel(excel_path)
    documents = []

    for _, row in df.iterrows():
        text = f"{row['Personel Adı']} adlı personel {row['Giriş Tarihi']} tarihinde {row['Giriş Saati']} giriş yapıp {row['Çıkış Saati']} çıkış yapmıştır."
        documents.append(text)

    return documents
