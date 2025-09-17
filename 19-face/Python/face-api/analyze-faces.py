from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

# Import namespaces
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials


def main():
    global cv_client

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')

        # Authenticate Computer Vision client
        credentials = CognitiveServicesCredentials(cog_key)
        cv_client = ComputerVisionClient(cog_endpoint, credentials)

        # Detect faces
        image_file = os.path.join('images', 'people.jpg')
        DetectFaces(image_file)

    except Exception as ex:
        print(ex)


def DetectFaces(image_file):
    print('Detecting faces in', image_file)

    # Specify features to be retrieved
    features = [VisualFeatureTypes.faces]

    # Get faces
    with open(image_file, mode="rb") as image_data:
        analysis = cv_client.analyze_image_in_stream(image_data, features)

        if analysis.faces:
            print(len(analysis.faces), "faces detected.")

            # Prepare image for drawing
            fig = plt.figure(figsize=(8, 6))
            plt.axis("off")
            image = Image.open(image_file)
            draw = ImageDraw.Draw(image)
            color = "lightgreen"

            # Draw bounding box for each face
            for face in analysis.faces:
                r = face.face_rectangle
                bounding_box = ((r.left, r.top), (r.left + r.width, r.top + r.height))
                draw.rectangle(bounding_box, outline=color, width=5)

            # Save annotated image
            plt.imshow(image)
            outputfile = "detected_faces.jpg"
            fig.savefig(outputfile)
            print("\nResults saved in", outputfile)
        else:
            print("No faces detected.")


if __name__ == "__main__":
    main()