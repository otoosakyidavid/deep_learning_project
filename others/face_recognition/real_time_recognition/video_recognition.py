import face_recognition
import cv2
import numpy as np



#video_capture = cv2.VideoCapture(0)
video_capture = cv2.VideoCapture('reg_test.mp4')

# calculate the center of the image
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('reg_vid_result.avi', fourcc, 15, (640, 352))

# Load a second sample picture and learn how to recognize it.
dayo_image = face_recognition.load_image_file("dayo.jpg")
dayo_face_encoding = face_recognition.face_encodings(dayo_image)[0]

# Load a second sample picture and learn how to recognize it.
dare = face_recognition.load_image_file("dare.jpg")
dare_encoding = face_recognition.face_encodings(dare)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    dayo_face_encoding,
    dare_encoding
]

known_face_names = [
    "Dayo",
     "Dare"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    print(ret)
    if ret:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # We need to set resolutions.
        frame_width = int(video_capture.get(3))
        frame_height = int(video_capture.get(4))

        size = (frame_width, frame_height)

        #   Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            print("numbers of faces", len(face_encodings))

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                """" If a match was found in known_face_encodings, just use the first one.
                True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                use the known face with the smallest distance to the new face
                """
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)
    else:
        break
    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        print(frame.shape[0], frame.shape[1])
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


    # Display the resulting image
    out.write(frame)
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
