"""
This script is used to create in one step all of the training tags for Customvision.ai
as well as to upload the downloaded images, train the system to recognize this images,
and test the trained model.
When it finished, it will print the porcentage of confidance it has in the test
identification.
"""

import os
import time
import sys
from azure.cognitiveservices.vision.customvision.training import (
    CustomVisionTrainingClient,
)
from azure.cognitiveservices.vision.customvision.prediction import (
    CustomVisionPredictionClient,
)
from azure.cognitiveservices.vision.customvision.training.models import (
    ImageFileCreateEntry,
)
from azure.cognitiveservices.vision.customvision.training.models import (
    ImageFileCreateBatch,
)
from msrest.authentication import ApiKeyCredentials
import conf

credentials = ApiKeyCredentials(in_headers={"Training-key": conf.TRAINING_KEY})
trainer = CustomVisionTrainingClient(conf.TRAINING_ENDPOINT, credentials)
prediction_credentials = ApiKeyCredentials(
    in_headers={"Prediction-key": conf.PREDICTION_KEY}
)
predictor = CustomVisionPredictionClient(
    conf.PREDICTION_ENDPOINT, prediction_credentials
)

PUBLISH_ITERATION_NAME = "classifyModel"

print("Creating project...")
PROJECT_NAME = "Moneras"
project = trainer.create_project(PROJECT_NAME)


def tag_species(species):
    """
    Defines a CustomVision.ai tag with an inat species, tags the images
    and uploads the current tagged images
    """
    tag = trainer.create_tag(project.id, species)

    base_image_location = os.path.join(os.path.dirname(__file__), conf.DIR_PATH)

    print("Adding images...")
    image_list = []

    file_list = next(os.walk(base_image_location + species), (None, None, []))[2]

    for file_name in file_list:
        with open(
            os.path.join(base_image_location, species, file_name), "rb"
        ) as tag_image_contents:
            image_list.append(
                ImageFileCreateEntry(
                    name=file_name, contents=tag_image_contents.read(), tag_ids=[tag.id]
                )
            )

    upload_result = trainer.create_images_from_files(
        project.id, ImageFileCreateBatch(images=image_list)
    )
    if not upload_result.is_batch_successful:
        print("Image batch upload failed.")
        for image in upload_result.images:
            print("Image status: ", image.status)
        sys.exit(-1)


for inat_species in conf.SPECIES:
    print(f"Tagging species: {inat_species}")
    tag_species(inat_species)

print("Training...")
iteration = trainer.train_project(project.id)
while iteration.status != "Completed":
    iteration = trainer.get_iteration(project.id, iteration.id)
    print("Training status: " + iteration.status)
    print("Waiting 10 seconds...")
    time.sleep(10)

trainer.publish_iteration(
    project.id, iteration.id, PUBLISH_ITERATION_NAME, conf.PREDICTION_RESOURCE_ID
)
print("Done!")

prediction_credentials = ApiKeyCredentials(
    in_headers={"Prediction-key": conf.PREDICTION_KEY}
)
predictor = CustomVisionPredictionClient(
    conf.PREDICTION_ENDPOINT, prediction_credentials
)

with open(
    os.path.join(conf.DIR_PATH, "Test/test_image.jpeg"), "rb"
) as test_image_contents:
    results = predictor.classify_image(
        project.id, PUBLISH_ITERATION_NAME, test_image_contents.read()
    )

    for prediction in results.predictions:
        print(f"\t{prediction.tag_name}: {prediction.probability * 100:0.2f}%")
