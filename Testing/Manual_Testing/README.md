# Manual Testing

Before pluggin the cameras, it's a good idea to test the AI model

## How to test

Copy a couple of "new" images from the species of interest. It's better if it's from the same type of cameras you are planning to use, but they can also be iNaturalist images as well. Just make sure that this images are "new" to the AI, in the sense that it wasn't trained with them.

This code is heavily based on [this tutorial](https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/quickstarts/image-classification?tabs=visual-studio&pivots=programming-language-python), so if you want to learn this topic in depth.

### Setup

```
pip install azure-cognitiveservices-vision-customvision
```

