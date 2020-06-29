import os
import cv2
import math
import numpy as np
from model import Eye

class EyeTracker():
    """
    EyeTracker implementation based on threshold using OpenCV
    Attributes:
        face_cascade: opencv face classifier
        eye_cascade: opencv eye classifier
        frame: current frame in numpy format
        frame_gray: current frame in gray scale in numpy format
        looking_direction: current looking direction as string (left or right)

    Methods:
        update: update the frame with the one just captured from camera and analize it
        decorate_frame: highlighs and draws the features extracted from face on the frme and return a copy of it
        left_eye: return an object for the left eye with the extracted features
        right_eye: return an object for the right eye with the extracted features
        get_looking_direction: return the current looking direction as string

    """
    def __init__(self):
        # initialize the opencv classifier for face and eye detection
        self.face_cascade = cv2.CascadeClassifier(os.path.join('classifiers', 'haarcascade_frontalface_default.xml'))
#        self.face_cascade = cv2.CascadeClassifier(os.path.join('classifiers', 'haarcascade_frontalface_alt.xml'))
#        self.eye_cascade = cv2.CascadeClassifier(os.path.join('classifiers', 'haarcascade_eye.xml'))
        self.eye_cascade = cv2.CascadeClassifier(os.path.join('classifiers', 'haarcascade_eye_tree_eyeglasses.xml'))

        # FOR BLOB DETECION VERSION
#        detector_params = cv2.SimpleBlobDetector_Params()
#        # Change thresholds
#        detector_params.minThreshold = 0;
#        detector_params.maxThreshold = 255;
#        # Filter by Area.
#        detector_params.filterByArea = True
#        detector_params.minArea = 200
#        detector_params.maxArea = 500
#        # Filter by Circularity
#        detector_params.filterByCircularity = True
#        detector_params.minCircularity = 0.5
#        detector_params.maxCircularity = 1.5
#        # Filter by Inertia
#        detector_params.filterByInertia = True
#        detector_params.minInertiaRatio = 0.5
#        detector_params.maxInertiaRatio = 1.5
#
#        # Blob detector
#        self.blob_detector = cv2.SimpleBlobDetector_create(detector_params)

        self.frame = None
        self.frame_gray = None
        self.left_eye_frame = None
        self.right_eye_frame = None

        self.left_eye_detected = False
        self.right_eye_detected = False
        self.face_bb = None
        self.left_eye_bb = None
        self.right_eye_bb = None

        self.left_pupil_detected = False
        self.right_pupil_detected = False
        self.left_pupil = None
        self.right_pupil = None
        self.left_pupil_radius = None
        self.right_pupil_radius = None

        self.looking_direction = None

    def update(self, frame):
        self.frame = frame
        self._analyze()


    def _analyze(self):
        self.frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        self._extract_face()
        self._extract_eyes()
        if self.left_eye_detected:
            self._extract_pupil("left")

        if self.right_eye_detected:
            self._extract_pupil("right")

        self._extract_looking_direction()


    def left_eye(self):
        if self.left_eye_detected:
            return Eye(self.left_eye_frame.copy(), "left", self.left_pupil, self.left_pupil_radius)
        return None

    def right_eye(self):
        if self.right_eye_detected:
            return Eye(self.right_eye_frame.copy(), "right", self.right_pupil, self.right_pupil_radius)
        return None


    def get_looking_direction(self):
        return self.looking_direction


    def decorate_frame(self):
        frame = self.frame.copy()

        # draw the face bounding box
        x, y, w, h = self.face_bb
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,255,0), 2)

        if self.left_eye_bb:

            if self.left_pupil and self.left_pupil_radius:
                # draw the left pupil
                x, y = self.left_pupil
                x += self.left_eye_bb[0]
                y += self.left_eye_bb[1]
                r = self.left_pupil_radius
                cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)
                cv2.circle(frame, (x, y), r, (0, 255, 0), 1)
##                eye_frame = frame[self.left_eye_bb[1]:self.left_eye_bb[1]+self.left_eye_bb[3], self.left_eye_bb[0]:self.left_eye_bb[0]+self.left_eye_bb[2]]
##                cv2.imwrite("images/05_eye_frame.png", eye_frame)

            # draw the left eye bounding box
            x, y, w, h = self.left_eye_bb
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,255), 2)

        if self.right_eye_bb:

            if self.right_pupil and self.right_pupil_radius:
                # draw the right pupil center
                x, y = self.right_pupil
                x += self.right_eye_bb[0]
                y += self.right_eye_bb[1]
                r = self.right_pupil_radius
                cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)
                cv2.circle(frame, (x, y), r, (0, 255, 0), 1)

            # draw the right eye bounding box
            x, y, w, h = self.right_eye_bb
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,255), 2)

        return frame

    def _extract_face(self):

        """
        Extract the box of the face ROI image as opencv format (x, y, w, h) from the current frame
        """
        frame_gray = cv2.GaussianBlur(self.frame_gray, (7, 7), 0)
        faces = self.face_cascade.detectMultiScale(frame_gray, 1.3, 5) 
#        faces = self.face_cascade.detectMultiScale(frame_gray) 

        # detect the best face on the image based on ROI size
        if len(faces) > 1:
            temp = (0, 0, 0, 0)
            for f in faces:
                if f[2]*f[3] > temp[2] * temp[3]:
                    temp = f
            best_face = (temp[0], temp[1], temp[2], temp[3])
        elif len(faces) == 1:
            face = faces[0]
            best_face = (face[0], face[1], face[2], face[3])
        else:
            # if no face is detected return all image as face ROI
            image_height = self.frame_gray.shape[0]
            image_width = self.frame_gray.shape[1]
            best_face = (0, 0, image_width, image_height)

        self.face_bb = best_face

    def _extract_eyes(self):

        """
        Extract the box of the eyes ROI image as opencv format (x, y, w, h) from the current frame
        """
        self.left_eye_detected = False
        self.right_eye_detected = False
        self.left_eye_bb = None
        self.right_eye_bb = None

        x, y, w, h = self.face_bb

        face_frame_gray = self.frame_gray[y:y+h, x:x+w] 
        face_frame_gray = cv2.GaussianBlur(face_frame_gray, (7, 7), 0)

#        eyes = self.eye_cascade.detectMultiScale(face_frame_gray) 
        eyes = self.eye_cascade.detectMultiScale(face_frame_gray, 1.3, 5) 

        for (ex, ey, ew, eh) in eyes:
            # do not consider false eyes detected at the bottom of the face
            if ey > 0.5 * h:
                continue

            remove_eyebrows = np.array([0, int(0.25*eh), int(0), int(-0.25*eh)])
            eye_center = ex + ew / 2
            if eye_center > w * 0.5:
                self.left_eye_detected = True
                left_bb = np.array([ex, ey, ew, eh])
                left_bb += remove_eyebrows
                self.left_eye_bb = (x + left_bb[0], y + left_bb[1], left_bb[2], left_bb[3])
                self.left_eye_frame = self.frame[self.left_eye_bb[1]:self.left_eye_bb[1]+self.left_eye_bb[3], self.left_eye_bb[0]:self.left_eye_bb[0]+self.left_eye_bb[2]]

            else:
                self.right_eye_detected = True
                right_bb = np.array([ex, ey, ew, eh])
                right_bb += remove_eyebrows
                self.right_eye_bb = (x + right_bb[0], y + right_bb[1], right_bb[2], right_bb[3])
                self.right_eye_frame = self.frame[self.right_eye_bb[1]:self.right_eye_bb[1]+self.right_eye_bb[3], self.right_eye_bb[0]:self.right_eye_bb[0]+self.right_eye_bb[2]]


    def _extract_pupil(self, position):

        """
        Extract from the eye frame the coordinates of the center of the pupil (x, y) 
        w.r.t the eye frame and the pupil radius in pixels 
        """

        self.left_pupil_detected = False
        self.right_pupil_detected = False
        pupil_center = None
        pupil_radius = None

        if position == "left":
            eye_frame_gray = self.frame_gray[self.left_eye_bb[1]:self.left_eye_bb[1]+self.left_eye_bb[3], self.left_eye_bb[0]:self.left_eye_bb[0]+self.left_eye_bb[2]]

        if position == "right":
            eye_frame_gray = self.frame_gray[self.right_eye_bb[1]:self.right_eye_bb[1]+self.right_eye_bb[3], self.right_eye_bb[0]:self.right_eye_bb[0]+self.right_eye_bb[2]]


##        if position == "left":
##            cv2.imwrite("images/00_eye_frame_gray.png", eye_frame_gray)


#        eye_frame_gray = cv2.GaussianBlur(eye_frame_gray, (7, 7), 0)
#        eye_frame_gray = cv2.medianBlur(eye_frame_gray, 7)
        eye_frame_gray = cv2.equalizeHist(eye_frame_gray)

##        if position == "left":
##            cv2.imwrite("images/01_eye_frame_equalized.png", eye_frame_gray)

#        threshold = 25
        threshold = cv2.getTrackbarPos('threshold', 'frame')

        _, eye_frame_th = cv2.threshold(eye_frame_gray, threshold, 255, cv2.THRESH_BINARY)

##        if position == "left":
##            cv2.imwrite("images/02_eye_frame_threshold.png", eye_frame_th)

        eye_frame_th = cv2.erode(eye_frame_th, None, iterations=2)
        eye_frame_th = cv2.dilate(eye_frame_th, None, iterations=4)

        eye_frame_th = cv2.medianBlur(eye_frame_th, 7)

##        if position == "left":
##            cv2.imwrite("images/03_eye_frame_medianBlur.png", eye_frame_th)

        contours, _ = cv2.findContours(eye_frame_th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x))

        for cnt in contours:
            cnt = cv2.convexHull(cnt)
            area = cv2.contourArea(cnt)
            if area < 10:
                continue
            circumference = cv2.arcLength(cnt, True)
            circularity = circumference ** 2 / (4*math.pi*area)
#            if circularity < 0.5 and circularity > 1.5:
#                continue

#            (x,y), radius = cv2.minEnclosingCircle(cnt)
#            pupil_center = (int(x),int(y))

            radius = circumference / (2 * math.pi)
            pupil_radius = int(radius)
            m = cv2.moments(cnt)
            if m['m00'] != 0:
                pupil_center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                break

        # FOR BLOB DETECTION VERSION
#        keypoints = self.blob_detector.detect(eye_frame_th)
#        if len(keypoints) > 0:
#            pupil_center = (int(keypoints[0].pt[0]), int(keypoints[0].pt[1]))
#            pupil_radius = int(keypoints[0].size / 2)

        if position == "left":
            if pupil_center != None and pupil_radius != None:
                self.left_pupil_detected = True
            self.left_pupil = pupil_center
            self.left_pupil_radius = pupil_radius

        if position == "right":
            if pupil_center != None and pupil_radius != None:
                self.right_pupil_detected = True
            self.right_pupil = pupil_center
            self.right_pupil_radius = pupil_radius


    def _extract_looking_direction(self):
        """
        Extract the looking direction from the current extracted features
        """

        direction = None
        directionR = None
        directionL = None

        if self.left_eye_detected and self.left_pupil:
            w = self.left_eye_frame.shape[1]
            if self.left_pupil[0] < 0.45 * w:
                directionL = "right"
            if self.left_pupil[0] > 0.55 * w:
                directionL = "left"
            direction = directionL

        if self.right_eye_detected and self.right_pupil:
            w = self.right_eye_frame.shape[1]
            if self.right_pupil[0] < 0.45 * w:
                directionR = "right"
            if self.right_pupil[0] > 0.55 * w:
                directionR = "left"
            direction = directionR

        if directionL == directionR:
            direction = directionL
        elif directionL == None and directionR:
            direction = directionR
        elif directionR == None and directionL:
            direction = directionL
        else:
            direction = None

        self.looking_direction = direction
