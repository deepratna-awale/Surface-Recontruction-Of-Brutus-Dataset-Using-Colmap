# Base Code: https://www.thepythoncode.com/article/extract-frames-from-videos-in-python
# The base code extracts all frames from a single video
# I have modified this code to extract one single frame from the start (frame 0) for all videos in a given directory
# A dir "Frames" in the same directory will be created
 
from os import walk
from os.path import isfile, join
from datetime import timedelta
import cv2
import numpy as np
import os


def get_saving_frames_durations(cap, saving_fps, clip_at_secs=None):
    """A function that returns the list of durations where to save the frames"""
    s = []
    # get the clip duration by dividing number of frames by the number of frames per second
    if not clip_at_secs:
        clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / \
            cap.get(cv2.CAP_PROP_FPS)
    else:
        clip_duration = clip_at_secs

    # use np.arange() to make floating-point steps
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s


def extract_frames(video_file, capture_FPS, clip_at_secs):

    file_path, filename = os.path.split(video_file)
    filename, _ = os.path.splitext(filename)
    SAVING_FRAMES_PER_SECOND = int(capture_FPS)
    clip_at_secs = float(clip_at_secs)


    # read the video file
    cap = cv2.VideoCapture(video_file)
    # get the FPS of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    # if the SAVING_FRAMES_PER_SECOND is above video FPS, then set it to FPS (as maximum)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    # get the list of duration spots to save
    saving_frames_durations = get_saving_frames_durations(
        cap, saving_frames_per_second, clip_at_secs)
    # start the loop

    count = 0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            # break out of the loop if there are no frames to read
            break
        # get the duration by dividing the frame count by the FPS
        frame_duration = count / fps
        try:
            # get the earliest duration to save
            closest_duration = saving_frames_durations[0]
        except IndexError:
            # the list is empty, all duration frames were saved
            break
        if frame_duration >= closest_duration:
            # if closest duration is less than or equals the frame duration,
            # then save the frames
            write_path = os.path.join(file_path+"\Frames", f"{filename}.jpg")
            cv2.imwrite(write_path, frame)
            # drop the duration spot from the list, since this duration spot is already saved
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        # increment the frame count
        count += 1


def main(file_directory):
    files = []

    for (dirpath, dirnames, filenames) in walk(file_directory):
        files.extend(filenames)  
        break

    # Keep only mp4 files
    for file in files:
        if 'wav' in file:
            files.remove(file)

    capture_FPS = 1
    clip_at_secs = 1
    
    # make a folder by the name of the video file
    print(f"Creating directory 'Frames' at {file_directory} .")
    frame_dir = os.path.join(file_directory, "Frames")
    if not os.path.isdir(frame_dir):
        os.mkdir(frame_dir)

    print("Extracting Frames.")

    for file in files:
        full_file_path = os.path.join(dirpath, file)
        print(f"Extracting from: {full_file_path}. ", end=' ')
        extract_frames(full_file_path, capture_FPS, clip_at_secs)
        print("Done.")

    print(f"Frames extracted at {frame_dir}.")


if __name__ == "__main__":
    import sys
    dir = sys.argv[1]
    main(dir)
