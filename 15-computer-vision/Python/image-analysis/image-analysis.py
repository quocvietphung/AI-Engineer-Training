from dotenv import load_dotenv
import os, sys
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image
import matplotlib.pyplot as plt

def main():
    try:
        # Load config
        load_dotenv()
        cog_endpoint = os.getenv("COG_SERVICE_ENDPOINT")
        cog_key = os.getenv("COG_SERVICE_KEY")

        image_file = "images/street.jpg"
        if len(sys.argv) > 1:
            image_file = sys.argv[1]

        # Authenticate client
        global cv_client
        cv_client = ComputerVisionClient(cog_endpoint, CognitiveServicesCredentials(cog_key))

        # Analyze image
        AnalyzeImage(image_file)

        # Generate thumbnail
        GetThumbnail(image_file)

    except Exception as ex:
        print("Error:", ex)


def AnalyzeImage(image_file):
    print("Analyzing:", image_file)

    with open(image_file, "rb") as img_stream:
        features = ["description", "tags", "objects"]
        analysis = cv_client.analyze_image_in_stream(img_stream, visual_features=features)

    # Print description
    if analysis.description and analysis.description.captions:
        print("\nDescription:", analysis.description.captions[0].text)

    # Print tags
    print("\nTags:", [tag.name for tag in analysis.tags])

    # Print detected objects
    print("\nObjects:")
    for obj in analysis.objects:
        print(f" - {obj.object_property} at "
              f"({obj.rectangle.x},{obj.rectangle.y},"
              f"{obj.rectangle.w},{obj.rectangle.h})")


def GetThumbnail(image_file):
    print("Generating thumbnail...")

    with open(image_file, "rb") as img_stream:
        thumb = cv_client.generate_thumbnail_in_stream(
            100, 100, img_stream, smart_cropping=True
        )

    # Save thumbnail
    with open("thumbnail.jpg", "wb") as f:
        for chunk in thumb:
            f.write(chunk)

    print("Thumbnail saved as thumbnail.jpg")


if __name__ == "__main__":
    main()