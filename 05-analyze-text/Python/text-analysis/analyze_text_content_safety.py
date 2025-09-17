from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv

# Load env
load_dotenv()
endpoint = os.getenv("COG_SERVICE_ENDPOINT")
key = os.getenv("COG_SERVICE_KEY")

client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

# Nội dung test
text = "This is a fucking test message."

# Gọi API phân tích
request = AnalyzeTextOptions(
    text=text,
    categories=[TextCategory.HATE, TextCategory.SELF_HARM, TextCategory.SEXUAL, TextCategory.VIOLENCE]
)

response = client.analyze_text(request)

print("🔎 Input:", text)
for result in response.categories_analysis:
    print(f"Category: {result.category}, Severity: {result.severity}")