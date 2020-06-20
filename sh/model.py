class Eye:

    """
    Model class for an eye
    Attributes:
        image: eye ROI of original image
        position: string to identify left or right eye
        pupil_center: a tuple (x, y) with the coordinates of the center of the pupil w.r.t the eye ROI image
        pupil_radius: radius of the pupil in pixels
    """

    def __init__(self, frame, position, pupil_center, pupil_radius):
        self.frame = frame
        self.position = position
        self.pupil_center = pupil_center
        self.pupil_radius = pupil_radius

    def __str__(self):
        return "Eye: {}\n\tPupil center: {}\n\tPupil radius: {}\n".format(self.position, self.pupil_center, self.pupil_radius)

