#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  9 19:32:28 2022

@author: oliverpage

Extract all frames from a clip and automate distributing them amongst training
and validation data. 
"""
from datetime import timedelta
from time import time_ns
from numpy.random import choice
import cv2
import numpy as np
import os

# i.e if video of duration 30 seconds, saves 10 frame per second = 300 frames saved in total
SAVING_FRAMES_PER_SECOND = 30


data_path = '/Users/oliverpage/Desktop/Stuff/Taser Kart/Computer vision/TaserKart/'
train_hit = 'train/hit'
train_safe = 'train/safe'
valid_hit = 'valid/hit'
valid_safe = 'valid/safe'

def train_or_valid_hit():
    return data_path + choice([train_hit, valid_hit])

def train_or_valid_safe():
    return data_path + choice([train_safe, valid_safe])

def get_destination():
    folder = os.getcwd().split('/')[-1]
    
    if folder == 'hit':
        return data_path + choice([train_hit, valid_hit]) 
    else:
        return data_path + choice([train_safe, valid_safe])
    



def format_timedelta(td):
    """Utility function to format timedelta objects in a cool way (e.g 00:00:20.05)
    omitting microseconds and retaining milliseconds"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return result + ".00".replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")


def get_saving_frames_durations(cap, saving_fps):
    """A function that returns the list of durations where to save the frames"""
    s = []
    # get the clip duration by dividing number of frames by the number of frames per second
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    # use np.arange() to make floating-point steps
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s

def main(video_file):
    filename, _ = os.path.splitext(video_file)
    # filename += "-opencv"
    # make a folder by the name of the video file
    if not os.path.isdir(filename):
        os.mkdir(filename)
    # read the video file
    cap = cv2.VideoCapture(video_file)
    # get the FPS of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    # if the SAVING_FRAMES_PER_SECOND is above video FPS, then set it to FPS (as maximum)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    # get the list of duration spots to save
    saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
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
            # then save the frame
            frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            cv2.imwrite(os.path.join(filename, f"frame{frame_duration_formatted}"+str(time_ns())+".jpg"), frame)
            # drop the duration spot from the list, since this duration spot is already saved
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        # increment the frame count
        count += 1


if __name__ == "__main__":
    import sys
    video_file = sys.argv[1]
    main(video_file)
