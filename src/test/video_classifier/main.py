import faces
import blur
import utils
import orbmatcher
import scene
from datetime import datetime, date


def main():

    # Time start
    t0 = datetime.now()

    # Path
    video_path = "C:\\Users\\Admin\\PycharmProjects\\video_classifier\\video\\"
    frame_path = "C:\\Users\\Admin\\PycharmProjects\\video_classifier\\frames\\"
    faces_path = "C:\\Users\\Admin\\PycharmProjects\\video_classifier\\face\\"
    faces_cascade_path = "C:\\Users\\Admin\\PycharmProjects\\video_classifier\\detect\\haarcascade_frontalface_alt.xml"
    ffmpeg_path = "C:\\Users\\Admin\\PycharmProjects\\video_classifier\\ffmpeg\\bin\\ffmpeg.exe"

    # Sort video by filename (brand)
    #utils.sort_video_ba_brand(frame_path)

    dico_match = {}

    # Remove special char in filename (ffmpeg => no such file or directory)
    utils.remove_special_char(video_path)

    # Get all video file
    video_files = utils.get_files(video_path)

    # Detect and process scene
    #scene.process_scene(video_path, frame_path, ffmpeg_path)

    # Get all frames
    scene_files = utils.get_files_rec(frame_path)
    print("Scene files number: %s" % str(len(scene_files)))

    # Face detection
    print("[%s] faces_recognition: start" % str(datetime.now().strftime("%d-%m-%Y %H:%M")))
    scene_files, dico_match = faces.faces_recognition(scene_files, faces_path, faces_cascade_path)
    print("Scene files number: %s" % str(len(scene_files)))
    print("[%s] faces_recognition: stop" % str(datetime.now().strftime("%d-%m-%Y %H:%M")))

    # Detect blur file and remove them from list
    print("[%s] blur_detection: start" % str(datetime.now().strftime("%d-%m-%Y %H:%M")))
    scene_files = blur.blur_detection(scene_files)
    print("Scene files number: %s" % str(len(scene_files)))
    print("[%s] blur_detection: stop" % str(datetime.now().strftime("%d-%m-%Y %H:%M")))

    # Match 2 image with ORB matcher => calc Hammin dist
    print("[%s] orb_matcher: start" % str(datetime.now().strftime("%d-%m-%Y %H:%M")))
    dico_match = orbmatcher.orb_matcher(scene_files, dico_match)
    print("[%s] orb_matcher: stop" % str(datetime.now().strftime("%d-%m-%Y %H:%M")))

    # Get time and compare
    t1 = datetime.now()
    print("Duration: %s" % (t1 - t0))

    # Print match on network graph
    utils.display_graph("result.json")


if __name__ == "__main__":
    main()
