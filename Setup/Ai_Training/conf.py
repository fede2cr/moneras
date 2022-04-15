"""
Configuration file for the project. Add here the information for the species
that the cameras are going to focus on.
"""
SPECIES = ["Alouatta palliata", "Cebus imitator"]

# iNaturalist configuration
INAT_USER = "fede2cr"

"""
Grab this information from the Azure Portal. You should have two resources,
the trainig resource, and the prediction resource.
"""
TRAINING_ENDPOINT = "https://copy-paste-endpoint.cognitiveservices.azure.com/"
TRAINING_KEY = "copy-paste-key"
PREDICTION_ENDPOINT = (
    "https://copy-paste-prediction-endpoint.cognitiveservices.azure.com/"
)
PREDICTION_KEY = "copy-paste-prediction-key"
# Resource ID split into two lines
PREDICTION_RESOURCE_ID = (
    "/subscriptions/123-456-789/"
    + "resourceGroups/Monero/providers/Microsoft.CognitiveServices/accounts/Moneras-Prediction"
)

# General app config, no need to edit here
DIR_PATH = "Training_Images/"
