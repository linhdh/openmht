import sys
# import kalmanfilter as kf
import numpy as np
from copy import deepcopy
from tracktree import TrackTree


class OpenMHT:
    """
    Multiple hypothesis tracking.
    """
    def __init__(self, detections):
        self.detections = list(detections)
        self.frame_count, _, self.dimensionality = detections.shape
        self.frame_number = 0
        self.track_trees = []  # Track hypotheses for detections in each frame

    def global_hypothesis(self, trees):
        pass

    def get_detections(self):
        return self.detections.pop()

    def run(self):
        print("Number of frames: {}".format(len(self.detections)))
        while self.detections:
            self.frame_number += 1
            detections = self.detections.pop()
            print("Number of detections: {}".format(len(detections)))

            # Update the previous track trees from the detections
            updated_track_trees = []
            for track_tree in self.track_trees:
                # Generate updated track trees from the detections
                for detection in detections:
                    track_tree_copy = deepcopy(track_tree)
                    track_tree_copy.add_detection(detection)
                    updated_track_trees.append(track_tree_copy)

                # Add a dummy observation to account for missing detections
                track_tree.add_detection(None)
            self.track_trees.extend(updated_track_trees)

            # Generate new track trees from the detections
            for detection in detections:
                track_tree = TrackTree(self.frame_number)
                track_tree.add_detection(detection)
                self.track_trees.append(track_tree)
        print("Done")
        for i in range(len(self.track_trees)):
            # print("\nTrack {}".format(i))
            self.track_trees[i].print_data()