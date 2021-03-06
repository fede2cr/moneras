# moneras

Camera traps for following american primates, as well as many other wildlife

## Description

This are camera traps based on stock hardware (ESP32-cameras) that use Microsoft's Computer Vision Platform to identify when primates pass near the camera.

## How they work

There are several platform of cameras that have internet access via Wifi. When they detect movement via several methods (based on the [iot-security project](https://github.com/fede2cr/iot-security)), they take a snapshot, and pass it to AI platforms that detect the presence of human/no-human, or for example if there is a capuchin or a howler monkey present, where the species is defined by where the camera is installed and by which species are interesting to researchers or land owners that want to learn more about biodiversity.

In the configuration interface for your group of cameras, you decide which species are important to you, and if they get detected, you will receive a notification with the cropped image with only the detection part, and a link where you can download the full image. This is important, for let's say, an feline researcher that only gets a couple of chances a month to follow the track of it's animal of interest.

## How to Setup

It is better if you have images from the same cameras from this project, which you can also use to re-train the AI model and improve it. But to start with a working system, this scripts use [INaturalist]() images that have a license that permits their re-use.

```
cd Setup/Ai_Training
pip3 install pyinaturalist # Only do this once
nano inat_image_downloader.py
```

Now that you have a file editor open (called "nano"), change line 13 to define the iNaturalist user to get the images from, and line 15 to define the name of the species (the same that iNaturalist uses).

```
USER='fede2cr'
#SPECIES='Alouatta palliata'
SPECIES='Cebus imitator'
```

Exit the editor (if it is nano, do Ctrl+o, Enter, Ctrl+x). Run the script by executing:

```
python3 inat_image_downloader.py
```

The images are downloaded with each species in a separate folder. Repeat the edit process to add more users, or more species. Then, for example with Customvision.ai, you only need to drag and drop the images, and re-train the model.

It is a good idea to keep a couple of the images out of the model training set, so that you can then test the accuracy of the model, and see how well it predicts the species of the images.

### File deduplication or ``ErrorImageFormat``

This is an optional step, but the following step, where you upload the images to Microsoft's Azure, you could get an error about duplicate file. This is because in iNaturalist, some users upload images twice or more if it includes two individuals or two species that need to be added as an observation. If this is happening for your training data, run:

```
fdupes -fdNr .
```

If you get an error like ``ErrorImageFormat``, it might be that you have extra data on this folders other than images. If so, try to find which file is it, and run something similar to:

```
# This commands removes junk files from MacOS X's Finder
find . -name .DS_Store -exec rm -v {} \;
```

# Computer vision model training

Before pluggin the cameras, it's a good idea to test the AI model

## How to test

Copy a couple of "new" images from the species of interest. It's better if it's from the same type of cameras you are planning to use, but they can also be iNaturalist images as well. Just make sure that this images are "new" to the AI, in the sense that it wasn't trained with them.

This code is heavily based on [this tutorial](https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/quickstarts/image-classification?tabs=visual-studio&pivots=programming-language-python), so if you want to learn this topic in depth.

### Setup

```
pip install azure-cognitiveservices-vision-customvision
```

## AI Platforms

- [Microsoft's Customvision.ai](https://www.customvision.ai)
- [Microsoft's Megadetector](https://github.com/microsoft/CameraTraps/blob/main/megadetector.md)

### Adaptable to
- [Teachable Machine](https://teachablemachine.withgoogle.com/)

## Compatible hardware

- [ESP32-cam](https://www.crcibernetica.com/esp32-with-camera/) - ~$16 in Costa Rica
- (Soon) Raspberry Pi with Low Light Cameras like [IMX462](https://www.youtube.com/watch?v=2QFUMuyiNBE) (not infrared)
- (Future) Adafruit's ESP32S2 camera with CircuitPython
