# 1. Import the library
from inference_sdk import InferenceHTTPClient
import json
import cv2
import copy
import time

########################################################################
#                     Fonction donnée par Roboflow                     #
########################################################################


def yolo(image):
    """

    Execute Yolo sur l'image dont le chemin a été mis en paramètre
    Données par Roboflow

    :param image: image_path
    """

    # 2. Connect to your workflow
    client = InferenceHTTPClient(
        api_url="https://serverless.roboflow.com", api_key="tenUcVkBA4ZvPfzSl4LN"
    )

    # 3. Run your workflow on an image
    result = client.run_workflow(
        workspace_name="adrien-32agi",
        workflow_id="custom-workflow",
        images={"image": image},  # Path to your image file
        use_cache=True,  # Speeds up repeated requests
    )

    return result
    # with open(output, "w", encoding="utf-8") as f:
    #     json.dump(result, f, ensure_ascii=False, indent=4)


##########################################################
#                     Fonction créée                     #
##########################################################


def bounding_box(contour, image_shape, marge=20):
    """
    Renvoie les coordonnées pour créer une bounding box autour du contour
        
    :param contour: contour
    :param image_shape: format de l'image de base, image.shape()
    :param marge: marge à rajouter autour du contour
    """
    h, w = image_shape[:2]

    xs = [p["x"] for p in contour]
    ys = [p["y"] for p in contour]

    x_min = max(int(min(xs) - marge), 0)
    y_min = max(int(min(ys) - marge), 0)
    x_max = min(int(max(xs) + marge), w)
    y_max = min(int(max(ys) + marge), h)

    return x_min, y_min, x_max, y_max


def projection_contour(contour, offset_x, offset_y):
    """
    Remet le contour à sa place dans l'image originale
        
    :param contour: contour
    :param offset_x: abscisse où l'on commence à coller le contour
    :param offset_y: ordonnée où l'on commence à coller le contour
    """
    return [{"x": int(p["x"] + offset_x), "y": int(p["y"] + offset_y)} for p in contour]


def yolo_refinnement(image):
    """
    Fonction qui applique plusieurs fois YOLO, une fois sur toute l'image puis une fois par pièce trouvée
    
    :param image: Description
    """
    # Chargement de l'image pour pouvoir la découper
    image_cv = cv2.imread(image)

    # Première passe YOLO sur l'image complète
    output_v1 = yolo(image)

    contours_v1 = []
    for output in output_v1[0]["predictions"]["predictions"]:
        contours_v1.append(output["points"])

    # Copie complète du résultat initial
    output_final = copy.deepcopy(output_v1)
    output_final[0]["predictions"]["predictions"] = []

    # Raffinement pour chaque contour détecté
    for i in range(len(contours_v1)):
        x_min, y_min, x_max, y_max = bounding_box(
            contours_v1[i], image_cv.shape, marge=20
        )

        # Découpage de la zone d'intérêt
        tmp_image = image_cv[y_min : int(y_max), x_min : int(x_max)].copy()

        cv2.imwrite("tmp.png", tmp_image)
        output_v2 = yolo("tmp.png")

        # Ajout des pièces raffinées
        for piece in output_v2[0]["predictions"]["predictions"]:
            piece_copy = copy.deepcopy(piece)

            contour_v2 = piece_copy["points"]
            contour_final = projection_contour(contour_v2, x_min, y_min)

            piece_copy["points"] = contour_final
            output_final[0]["predictions"]["predictions"].append(piece_copy)

    return output_final

    # if len(contour_final)/len(contours_v1) < 0.95:
    #     return output_final
    # else:
    #     return output_v1


contour = yolo_refinnement("image11.png")

with open("result_im11.json", "w", encoding="utf-8") as f:
    json.dump(contour, f, ensure_ascii=False, indent=4)
