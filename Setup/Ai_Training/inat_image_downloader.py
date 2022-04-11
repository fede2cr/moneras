'''
Código para descargar imágenes por especie, desde una cuenta de inaturalist
Al descargar las imágenes, se salvan en una carpeta con el nombre de la especie
y luego se utilizan para alimentar a Customvision.ai de Microsoft
Nota: Solo se descargan imágenes CC-By
Mejora: Se puede reutilizar el código para descargar todas las especies vistas en la zona
'''

import os
from pyinaturalist import get_observations
import requests

USER='fede2cr'
#SPECIES='Alouatta palliata'
SPECIES='Cebus imitator'

IS_EXIST = os.path.exists(SPECIES)
if not IS_EXIST:
    os.makedirs(SPECIES)

observations = get_observations(user_id=USER, page='all')

for obs in observations['results']:
    if obs["taxon"]["name"] == SPECIES:
        for i in range(0, len(obs["observation_photos"])):
            if obs["observation_photos"][i]["photo"]["license_code"] == "cc-by":
                #print(obs["observation_photos"][i]["photo"])
                ORIG_URL = ("https://inaturalist-open-data.s3.amazonaws.com/photos/"
                    + str(obs["observation_photos"][i]["photo"]["id"]) + "/original.jpeg")
                print("Downloading: ", ORIG_URL)
                r = requests.get(ORIG_URL, allow_redirects=True)
                with open(SPECIES + "/" + str(obs["observation_photos"][i]["photo"]["id"])
                    + '.jpeg', 'wb') as f:
                    f.write(r.content)
    #print(obs.keys())
        print("=" * 80)
