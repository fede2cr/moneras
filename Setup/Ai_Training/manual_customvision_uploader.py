'''
This code uses
'''
import os
import time
import secrets
import sys
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch
#, Region
from msrest.authentication import ApiKeyCredentials

credentials = ApiKeyCredentials(in_headers={"Training-key": secrets.TRAINING_KEY})
trainer = CustomVisionTrainingClient(secrets.TRAINING_ENDPOINT, credentials)
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": secrets.PREDICTION_KEY})
predictor = CustomVisionPredictionClient(secrets.PREDICTION_ENDPOINT, prediction_credentials)

PUBLISH_ITERATION_NAME = "classifyModel"

print ("Creating project...")
PROJECT_NAME = "Moneras"
project = trainer.create_project(PROJECT_NAME)

capuchin_tag = trainer.create_tag(project.id, "Cebus imitator")
howler_tag = trainer.create_tag(project_id=project.id, name="Alouatta palliata")

base_image_location = os.path.join (os.path.dirname(__file__), "Images")

print("Adding images...")
image_list = []

file_list = next(os.walk(base_image_location + "/Cebus imitator"), (None, None, []))[2]

for file_name in file_list:
    with open(os.path.join (base_image_location, "Cebus imitator",
        file_name), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name,
            contents=image_contents.read(), tag_ids=[capuchin_tag.id]))

file_list = next(os.walk(base_image_location + "/Alouatta palliata"), (None, None, []))[2]

for file_name in file_list:
    with open(os.path.join (base_image_location, "Alouatta palliata",
        file_name), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name,
            contents=image_contents.read(), tag_ids=[howler_tag.id]))

upload_result = trainer.create_images_from_files(project.id,
    ImageFileCreateBatch(images=image_list))
if not upload_result.is_batch_successful:
    print("Image batch upload failed.")
    for image in upload_result.images:
        print("Image status: ", image.status)
    sys.exit(-1)

print ("Training...")
iteration = trainer.train_project(project.id)
while iteration.status != "Completed":
    iteration = trainer.get_iteration(project.id, iteration.id)
    print ("Training status: " + iteration.status)
    print ("Waiting 10 seconds...")
    time.sleep(10)

trainer.publish_iteration(project.id, iteration.id,
    PUBLISH_ITERATION_NAME, secrets.PREDICTION_RESOURCE_ID)
print ("Done!")

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": secrets.PREDICTION_KEY})
predictor = CustomVisionPredictionClient(secrets.PREDICTION_ENDPOINT, prediction_credentials)

with open(os.path.join (base_image_location, "Test/test_image.jpeg"), "rb") as image_contents:
    results = predictor.classify_image(
        project.id, PUBLISH_ITERATION_NAME, image_contents.read())

    for prediction in results.predictions:
        print(f"\t{prediction.tag_name}: {prediction.probability * 100:0.2f}%")
