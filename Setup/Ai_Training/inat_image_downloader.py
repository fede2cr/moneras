"""
Código para descargar imágenes por especie, desde una cuenta de inaturalist
Al descargar las imágenes, se salvan en una carpeta con el nombre de la especie
y luego se utilizan para alimentar a Customvision.ai de Microsoft
Nota: Solo se descargan imágenes CC-By
Mejora: Se puede reutilizar el código para descargar todas las especies vistas en la zona
"""

import os
from pyinaturalist import get_observations
import requests
import conf


def download_species(species, inat_user):
    """
    This function receives a species name from inaturalist, and a username, and it
    downloads to the conf.DIR_PATH, all of the available images in original format.
    The downloaded images are then used by other script to train CV models.
    """
    img_dir = os.path.join(conf.DIR_PATH, species)
    if_exist = os.path.exists(img_dir)
    if not if_exist:
        os.makedirs(img_dir)

    observations = get_observations(user_id=inat_user, page="all")

    for obs in observations["results"]:
        if obs["taxon"]["name"] == species:
            for i in range(0, len(obs["observation_photos"])):
                if obs["observation_photos"][i]["photo"]["license_code"] == "cc-by":
                    # print(obs["observation_photos"][i]["photo"])
                    orig_url = (
                        "https://inaturalist-open-data.s3.amazonaws.com/photos/"
                        + str(obs["observation_photos"][i]["photo"]["id"])
                        + "/original.jpeg"
                    )
                    print("Downloading: ", orig_url)
                    image = requests.get(orig_url, allow_redirects=True)
                    with open(
                        img_dir
                        + "/"
                        + str(obs["observation_photos"][i]["photo"]["id"])
                        + ".jpeg",
                        "wb",
                    ) as image_file:
                        image_file.write(image.content)
            print("=" * 91)


for inat_species in conf.SPECIES:
    print(f"Downloading species: {inat_species}")
    download_species(inat_species, conf.INAT_USER)
