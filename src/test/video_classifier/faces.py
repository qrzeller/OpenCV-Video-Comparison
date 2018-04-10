import cv2
import utils
import numpy as np


def faces_recognition(scene_files, faces_path, faces_cascade_path):

    # Best value found as confidence threshold
    confidence_threshold = 50

    # Extract face from image
    faces_extraction(scene_files, faces_cascade_path, faces_path)

    # Train face extracted and match them with scene image
    dico_match = train_and_match_faces(scene_files, faces_cascade_path, faces_path, confidence_threshold)

    # Clean up match file (video)
    return clean_up_match(scene_files, dico_match), dico_match


def clean_up_match(scene_files, dico_match):

    # Process all image to detect
    for file in scene_files:
        vid_name = utils.get_video_name(file)

        # Process all key
        for k, v in dico_match.items():
            try:
                if k == vid_name:
                    scene_files.remove(file)

                    # Process all value list
                    for val in v:
                        value_vid_name = utils.get_video_name(val)
                        if value_vid_name == vid_name:
                            scene_files.remove(file)
            except ValueError:
                continue
    return scene_files


# Extract face from image
def faces_extraction(scene_files, faces_cascade_path, faces_path, scale_factor=1.2):

    # Get all image
    for image in scene_files:

        # Load and convert the image to gray image as opencv face detector expects gray images
        img = cv2.imread(image, 0)

        # Making a copy of image passed, so that passed image is not changed
        image_copy = img.copy()

        # Load cascade classifier training file for haarcascade
        haar_face_cascade = cv2.CascadeClassifier(faces_cascade_path)

        # Let's detect multiscale (some images may be closer to camera than others) images
        faces = haar_face_cascade.detectMultiScale(image_copy, scaleFactor=scale_factor, minNeighbors=5)

        # Go over list of faces and draw them as rectangles on original colored img
        i = 0
        for (x, y, w, h) in faces:

            # If detect face gen path where to save face
            path = faces_path + str(utils.get_video_name(image)) + "_face" + str(i) + ".png"

            # Extract face and save it as file
            cv2.imwrite(path, image_copy[y:y + h, x:x + w])


def train_and_match_faces(scene_files, faces_cascade_path, faces_path, confidence_threshold):
    dico_match = {}

    # Get face path and the name for each image
    faces, labels, relation = prepare_for_training(faces_path)

    # Create our LBPH face recognizer
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Train our face recognizer of our training faces
    face_recognizer.train(faces, np.array(labels))
    face_recognizer.save('trainer.yml')

    # Process all scene files
    for file in scene_files:

        # Detect face in scene files
        img = cv2.imread(file, 0)
        haar_face_cascade = cv2.CascadeClassifier(faces_cascade_path)
        faces = haar_face_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=5);

        # Compare the detected faces with the extracted faces
        for (x, y, w, h) in faces:
            face_id, conf = face_recognizer.predict(img[y: y + h, x: x + w])

            # A confidence value of 0.0 is a perfect recognition.
            if conf < confidence_threshold:
                found_face = search_face_by_id(relation, face_id)
                if found_face:
                    not_same_video, base, compare = check_if_from_same_video(file, found_face)
                    if not_same_video:
                        dico_match.setdefault(base, []).append(found_face)
    return dico_match


def prepare_for_training(faces_path):
    faces_image = utils.get_files(faces_path)
    faces = []
    labels = []
    relation = {}

    # Get all faces images extracted before
    face_id = 0
    for face in faces_image:

        # Gen int ID cause it must be like that (string => error)
        face_id = face_id + 1
        relation[face_id] = str(face)
        faces.append(cv2.imread(face, 0))
        labels.append(face_id)

    return faces, labels, relation


# Check if the "face file video name" is the same as the "current file video name"
def check_if_from_same_video(current_file, face_id):
    fi = utils.get_video_name(current_file)
    fa = utils.get_video_name(face_id).split("_")[0]
    if fi != fa:
        return True, fi, fa
    return False, None, None


# Search the "face file video name" from his face_id, contained in relation
def search_face_by_id(relation, face_id):
    for k, v in relation.items():
        if int(k) == face_id:
            return v
    return None
