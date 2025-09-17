import os
from dotenv import load_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

def main():
    load_dotenv()
    endpoint = os.getenv("FORM_ENDPOINT")
    key = os.getenv("FORM_KEY")

    # Tạo client
    client = DocumentAnalysisClient(endpoint, AzureKeyCredential(key))

    # Test với file ảnh test1.jpg
    with open("test1.jpg", "rb") as f:
        poller = client.begin_analyze_document("prebuilt-invoice", f)
        result = poller.result()

    # In kết quả
    for doc in result.documents:
        print("Detected fields:")
        for name, field in doc.fields.items():
            print(f"{name}: {field.value} (confidence={field.confidence})")

if __name__ == "__main__":
    main()