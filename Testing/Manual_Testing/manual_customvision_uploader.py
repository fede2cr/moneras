# <snippet_imports>
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid
# </snippet_imports>

'''
Prerequisites:

1. Install the Custom Vision SDK. Run:
pip install --upgrade azure-cognitiveservices-vision-customvision

2. Create an "Images" folder in your working directory.

3. Download the images used by this sample from:
https://github.com/Azure-Samples/cognitive-services-sample-data-files/tree/master/CustomVision/ImageClassification/Images

This sample looks for images in the following paths:
<your working directory>/Images/Hemlock
<your working directory>/Images/Japanese_Cherry
<your working directory>/Images/Test
'''

# <snippet_creds>
# Replace with valid values
TRAINING_ENDPOINT = "https://moneras.cognitiveservices.azure.com/"
training_key = "00d29e5b45e4491c84f2b59a852b7be6"
PREDICTION_ENDPOINT = "https://moneras-prediction.cognitiveservices.azure.com/"
prediction_key = "a3c8a41e1744430986bee59c0fbde509"
prediction_resource_id = "/subscriptions/c46c12a8-1626-4a23-9c25-c67d583be012/resourceGroups/Monero/providers/Microsoft.CognitiveServices/accounts/Moneras-Prediction"
# </snippet_creds>

# <snippet_auth>
credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(TRAINING_ENDPOINT, credentials)
#trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
#predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)
predictor = CustomVisionPredictionClient(PREDICTION_ENDPOINT, prediction_credentials)

# </snippet_auth>

# <snippet_create>
publish_iteration_name = "classifyModel"

credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(TRAINING_ENDPOINT, credentials)

# Create a new project
print ("Creating project...")
project_name = "Moneras"
project = trainer.create_project(project_name)
# </snippet_create>

# <snippet_tags>
# Make two tags in the new project
capuchin_tag = trainer.create_tag(project.id, "Cebus imitator")
howler_tag = trainer.create_tag(project.id, "Alouatta palliata")
# </snippet_tags>

# <snippet_upload>
base_image_location = os.path.join (os.path.dirname(__file__), "Images")

print("Adding images...")

image_dirs = []
image_list = []
#image_list = [item for item in os.listdir(base_image_location) if os.path.isfile(os.path.join(base_image_location, item))]

file_list = next(os.walk(base_image_location + "/Cebus imitator"), (None, None, []))[2]  # [] if no file
print(file_list)

for file_name in file_list:
    with open(os.path.join (base_image_location, "Cebus imitator", file_name), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[capuchin_tag.id]))

file_list = next(os.walk(base_image_location + "/Alouatta palliata"), (None, None, []))[2]  # [] if no file
print(file_list)

for file_name in file_list:
    with open(os.path.join (base_image_location, "Alouatta palliata", file_name), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[howler_tag.id]))

#for image_num in range(1, 11):
#    file_name = "japanese_cherry_{}.jpg".format(image_num)
#    with open(os.path.join (base_image_location, "Alouatta palliata", file_name), "rb") as image_contents:
#        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[howler_tag.id]))


upload_result = trainer.create_images_from_files(project.id, ImageFileCreateBatch(images=image_list))
if not upload_result.is_batch_successful:
    print("Image batch upload failed.")
    for image in upload_result.images:
        #print("Image status: ", image.status)
        print("Image status: ", image)
    exit(-1)
# </snippet_upload>

# <snippet_train>
print ("Training...")
iteration = trainer.train_project(project.id)
while (iteration.status != "Completed"):
    iteration = trainer.get_iteration(project.id, iteration.id)
    print ("Training status: " + iteration.status)
    print ("Waiting 10 seconds...")
    time.sleep(10)
# </snippet_train>

# <snippet_publish>
# The iteration is now trained. Publish it to the project endpoint
trainer.publish_iteration(project.id, iteration.id, publish_iteration_name, prediction_resource_id)
print ("Done!")
# </snippet_publish>

# <snippet_test>
# Now there is a trained endpoint that can be used to make a prediction
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(PREDICTION_ENDPOINT, prediction_credentials)

with open(os.path.join (base_image_location, "Test/test_image.jpeg"), "rb") as image_contents:
    results = predictor.classify_image(
        project.id, publish_iteration_name, image_contents.read())

    # Display the results.
    for prediction in results.predictions:
        print("\t" + prediction.tag_name +
              ": {0:.2f}%".format(prediction.probability * 100))
# </snippet_test>

# <snippet_delete>
# You cannot delete a project with published iterations, so you must first unpublish them.
#print ("Unpublishing project...")
#trainer.unpublish_iteration(project.id, iteration.id)

#print ("Deleting project...")
#trainer.delete_project (project.id)
# </snippet_delete>
