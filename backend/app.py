import datetime
import os
from flask import Flask, jsonify, Flask, request, Response
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random, smtplib
from backend.database_operations.mysql_credentials_reader import MysqlCredentials
from backend.database_operations.mysql_connection import DatabaseConnection
from backend.database_operations.user import UserDAO, UserLogin, UserRegistration
from werkzeug.utils import secure_filename
import mediapipe as mp
import cv2
import numpy as np
import time
import pymysql

app = Flask(__name__)
db_name = "ai_trainer"
credentials = MysqlCredentials.get_mysql_credentials()
connection = DatabaseConnection.connect_to_mysql_server(
    credentials["DBN"],
    credentials["mysql_username"],
    credentials["mysql_pwd"],
    credentials["mysql_host"],
)
connection.cursor()
user_login = UserLogin(connection, db_name)


@app.route("/check_user", methods=["POST"])
def check_user():
    email = request.json["email"]
    user_info = user_login.user_dao.retrieve_user_information(email)
    if user_info is not None:
        return jsonify({"exists": True})
    else:
        return jsonify({"exists": False})


@app.route("/signin", methods=["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]
    authenticated = UserLogin(connection, db_name).authenticate_user(email, password)
    if authenticated:
        # login successful
        return jsonify({"status": True, "message": "Login successful"})
    else:
        # login failed
        return jsonify({"status": False, "message": "Login failed"})


user_registration = UserRegistration(connection, db_name)


@app.route("/register", methods=["POST"])
def register():
    email = request.json["email"]
    username = request.json["username"]
    password = request.json["password"]

    registered = user_registration.register_user(email, username, password)

    if registered:
        return jsonify(
            {"status": True, "message": f"email {email} registered successfully"}
        )
    else:
        return jsonify({"status": False, "message": f"Email {email} is already taken"})


@app.route("/reset_password", methods=["POST"])
def reset_password():
    email = request.json["email"]
    new_password = request.json["new_password"]

    reset_successful = user_login.reset_password(email, new_password)

    if reset_successful:
        return f"Password for email {email} has been reset successfully"
    else:
        return f"Password reset failed for email {email}"


@app.route("/add_user_info", methods=["POST"])
def add_user_info():
    email = request.json["email"]
    height = request.json["height"]
    weight = request.json["weight"]
    age = request.json["age"]

    user_dao = UserDAO(connection, db_name)
    user_info = user_dao.retrieve_user_information(email)

    if user_info is None:
        return f"Email {email} not found in database"

    user_dao.update_user_information(email, height, weight, age)

    return f"User information updated for email {email}"


@app.route("/upload-image", methods=["POST"])
def upload_image():
    print(request.files)
    if "image" not in request.files:
        return "No image file found"
    image = request.files["image"]
    print(image)
    if image.filename == "":
        return "No image selected"
    if image:
        filename = secure_filename(image.filename)
        # image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        dbPath = os.path.join("uploads", filename)
        # Save dbPath to database
        image.save(dbPath)
        return "Image successfully uploaded!"


@app.route("/fit_weight_bmi", methods=["POST"])
def calculate_fit_weight_bmi():
    # Get data
    weight = float(request.json["weight"])
    height = float(request.json["height"])
    gender = request.json["gender"]

    # Calculate BMI
    bmi = weight / (height**2)

    #  weight status based on BMI
    if bmi < 18.4:
        weight_status = "underweight"
    elif 18.5 <= bmi < 24.9:
        weight_status = "normal"
    elif 25.0 <= bmi < 39.9:
        weight_status = "overweight"
    else:
        weight_status = "obese"

    #  ideal BMI based on gender
    if gender == "male":
        ideal_bmi = 23
    else:
        ideal_bmi = 22

    # Calculate fit weight based on ideal BMI and height
    fit_weight = ideal_bmi * (height**2)

    # Construct response message
    response = f"Your BMI is {bmi:.2f} , which is considered {weight_status}. "
    response += f"Your fit weight is {fit_weight:.2f} kg."
    return response


# otp by email
@app.route("/send_otp", methods=["POST"])
def send_otp():
    # Get the email address from the request
    email = request.json["email"]
    user_info = user_login.user_dao.retrieve_user_information(email)
    if user_info is not None:
        # Generate a random 6-digit OTP
        otp = str(random.randint(100000, 999999))
        # Create the email message
        message = MIMEMultipart()
        message["From"] = "amirahelmi01@gmail.com"
        message["To"] = email
        message["Subject"] = "Verification Code for your account"
        body = f"Your code is {otp}"
        message.attach(MIMEText(body, "plain"))
        # Send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("amirahelmi01@gmail.com", "jits fzrx hkwy bnab")
            text = message.as_string()
            server.sendmail("amirahelmi01@gmail.com", email, text)
        return {"message": "Verification Code sent successfully."}
    else:
        return "sorry, can't find the email"


@app.route("/Bicep", methods=["POST"])
def Bicep():
    video = request.files["video"]
    video.save("uploads1/" + video.filename)

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Set up Mediapipe Pose model
    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as pose:
        # Open video file
        cap = cv2.VideoCapture("uploads1/" + video.filename)
        if not cap.isOpened():
            return "Failed to open the video file."

        # Initialize variables
        curl_count = 0
        curl_started = False
        curl_ended = False
        previous_angle = 0

        while True:
            # Read frame from video
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB for Mediapipe Pose model
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process image with Mediapipe Pose model
            results = pose.process(image)

            # Draw landmarks on image
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

            # Extract landmarks of interest
            if results.pose_landmarks is not None:
                right_shoulder = results.pose_landmarks.landmark[
                    mp_pose.PoseLandmark.RIGHT_SHOULDER
                ]
                right_elbow = results.pose_landmarks.landmark[
                    mp_pose.PoseLandmark.RIGHT_ELBOW
                ]
                right_wrist = results.pose_landmarks.landmark[
                    mp_pose.PoseLandmark.RIGHT_WRIST
                ]

                # Calculate angle between arm and body
                a = np.array([right_shoulder.x, right_shoulder.y])
                b = np.array([right_elbow.x, right_elbow.y])
                c = np.array([right_wrist.x, right_wrist.y])
                angle = np.degrees(
                    np.arccos(
                        np.dot(b - a, c - b)
                        / (np.linalg.norm(b - a) * np.linalg.norm(c - b))
                    )
                )

                # Check if bicep curl started or ended
                if angle < 90 and not curl_started:
                    curl_started = True
                elif angle >= 90 and curl_started:
                    curl_count += 1
                    curl_started = False
                    curl_ended = True

                # If bicep curl ended, print number of curls and angle of last curl
                if curl_ended:
                    curl_ended = False
                    print(f"Curls: {curl_count}")
                    print(f"Angle: {previous_angle}")

                previous_angle = angle

            # Display rep counter
            counter_text = f"Curls: {curl_count}"
            cv2.putText(
                image,
                counter_text,
                (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )

            # Display image with landmarks
            cv2.imshow("Bicep Curl Detection", image)

            # Exit program when 'q' key is pressed
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

        # Release video file and close windows
        cap.release()
        cv2.destroyAllWindows()

        return f"Bicep curl done the counts are {curl_count}"


@app.route("/push_up", methods=["POST"])
def push_up():
    video = request.files["video"]
    video.save("uploads1/" + video.filename)

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Set up Mediapipe Pose model
    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as pose:
        # Open video file
        cap = cv2.VideoCapture("uploads1/" + video.filename)
        if not cap.isOpened():
            return "Failed to open the video file."
        # Replace 'path_to_video_file.mp4' with your video file path

        # Initialize variables
        pushup_jack_count = 0
        pushup_jack_started = False
        pushup_jack_ended = False
        previous_angle = 0

        while cap.isOpened():
            # Read frame from video
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB for Mediapipe Pose model
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process image with Mediapipe Pose model
            results = pose.process(image)

            # Draw landmarks on image
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

            # Extract landmarks of interest
            if results.pose_landmarks is not None:
                left_shoulder = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_SHOULDER
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_SHOULDER
                        ].y,
                    ]
                )
                left_elbow = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_ELBOW
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_ELBOW
                        ].y,
                    ]
                )
                left_wrist = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_WRIST
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_WRIST
                        ].y,
                    ]
                )

                # Calculate angle between arm and body
                a = np.linalg.norm(left_shoulder - left_elbow)
                b = np.linalg.norm(left_elbow - left_wrist)
                c = np.linalg.norm(left_shoulder - left_wrist)
                angle = (
                    np.arccos((a**2 + b**2 - c**2) / (2 * a * b)) * 180 / np.pi
                )

                # Check if push-up jack started or ended
                if angle > 160 and not pushup_jack_started:
                    pushup_jack_started = True
                elif angle < 60 and pushup_jack_started:
                    pushup_jack_count += 1
                    pushup_jack_ended = True

                # If push-up jack ended, print number of repetitions and angle of last movement
                if pushup_jack_ended:
                    pushup_jack_started = False
                    pushup_jack_ended = False
                    print(f"Push-Up Jacks: {pushup_jack_count}")
                    print(f"Angle: {previous_angle}")

                # Display rep counter
                counter_text = f"Push-Up Jacks: {pushup_jack_count}"
                cv2.putText(
                    image,
                    counter_text,
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

                previous_angle = angle

            # Display image with landmarks
            cv2.imshow("Push-Up Jack Detection", image)

            # Exit program when 'q' key is pressed
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

        # Release video and close windows
        cap.release()
        cv2.destroyAllWindows()
        return f"push up done the counts are {pushup_jack_count}"


@app.route("/push_up_hold", methods=["POST"])
def push_up_hold():
    video = request.files["video"]
    video.save("uploads1/" + video.filename)
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Set up Mediapipe Pose model
    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as pose:
        # Open video file

        cap = cv2.VideoCapture("uploads1/" + video.filename)
        if not cap.isOpened():
            return "Failed to open the video file."
        # Initialize variables
        pushup_hold_started = False
        pushup_hold_ended = False
        start_time = 0
        duration = 0

        while cap.isOpened():
            # Read frame from video
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB for Mediapipe Pose model
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process image with Mediapipe Pose model
            results = pose.process(image)

            # Draw landmarks on image
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

            # Extract landmarks of interest
            if results.pose_landmarks is not None:
                left_shoulder = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_SHOULDER
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_SHOULDER
                        ].y,
                    ]
                )
                right_shoulder = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_SHOULDER
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_SHOULDER
                        ].y,
                    ]
                )
                left_elbow = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_ELBOW
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_ELBOW
                        ].y,
                    ]
                )
                right_elbow = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_ELBOW
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_ELBOW
                        ].y,
                    ]
                )

                # Calculate angles between shoulders and elbows
                angle_left = np.degrees(
                    np.arctan2(
                        left_elbow[1] - left_shoulder[1],
                        left_elbow[0] - left_shoulder[0],
                    )
                )
                angle_right = np.degrees(
                    np.arctan2(
                        right_elbow[1] - right_shoulder[1],
                        right_elbow[0] - right_shoulder[0],
                    )
                )

                # Check if push-up hold started or ended
                if angle_left < 90 and angle_right < 90 and not pushup_hold_started:
                    pushup_hold_started = True
                    start_time = time.time()
                elif (angle_left >= 90 or angle_right >= 90) and pushup_hold_started:
                    pushup_hold_ended = True

                # If push-up hold ended, print duration of the hold
                if pushup_hold_ended:
                    pushup_hold_started = False
                    pushup_hold_ended = False
                    end_time = time.time()
                    duration = end_time - start_time
                    print(f"Push-Up Hold Time: {duration:.2f} seconds")

                # Display hold duration
                counter_text = (
                    f"Push-Up Hold Time: {duration:.2f} seconds"
                    if pushup_hold_started
                    else ""
                )
                cv2.putText(
                    image,
                    counter_text,
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

            # Display image with landmarks
            cv2.imshow("Push-Up Hold Detection", image)

            # Exit program when 'q' key is pressed
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

        # Release video and close windows
        cap.release()
        cv2.destroyAllWindows()
        return "push up hold detection completed."


@app.route("/shoulder_press", methods=["POST"])
def shoulder_press():
    video = request.files["video"]
    video.save("uploads1/" + video.filename)
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Set up Mediapipe Pose model
    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as pose:
        # Open video file
        cap = cv2.VideoCapture(
            "uploads1/" + video.filename
        )  # Replace 'path_to_video_file.mp4' with your video file path
        if not cap.isOpened():
            return "Failed to open the video file."

        # Initialize variables
        shoulder_press_started = False
        shoulder_press_ended = False
        shoulder_press_counter = 0

        while cap.isOpened():
            # Read frame from video
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB for Mediapipe Pose model
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process image with Mediapipe Pose model
            results = pose.process(image)

            # Draw landmarks on image
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

            # Extract landmarks of interest
            if results.pose_landmarks is not None:
                left_shoulder = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_SHOULDER
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_SHOULDER
                        ].y,
                    ]
                )
                right_shoulder = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_SHOULDER
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_SHOULDER
                        ].y,
                    ]
                )
                left_elbow = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_ELBOW
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_ELBOW
                        ].y,
                    ]
                )
                right_elbow = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_ELBOW
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_ELBOW
                        ].y,
                    ]
                )

                # Calculate angles between shoulders and elbows
                angle_left = np.degrees(
                    np.arctan2(
                        left_elbow[1] - left_shoulder[1],
                        left_elbow[0] - left_shoulder[0],
                    )
                )
                angle_right = np.degrees(
                    np.arctan2(
                        right_elbow[1] - right_shoulder[1],
                        right_elbow[0] - right_shoulder[0],
                    )
                )

                # Check if shoulder press started or ended
                if angle_left < 45 and angle_right < 45 and not shoulder_press_started:
                    shoulder_press_started = True
                elif (angle_left >= 45 or angle_right >= 45) and shoulder_press_started:
                    shoulder_press_counter += 1
                    shoulder_press_started = False

                # Display shoulder press counter
                counter_text = f"Shoulder Press Counter: {shoulder_press_counter}"
                cv2.putText(
                    image,
                    counter_text,
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

            # Display image
            cv2.imshow("Shoulder Press Detection", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Release video capture and close windows
        cap.release()
        cv2.destroyAllWindows()
        return f"shoulder press done the counts are {shoulder_press_counter}"


@app.route("/front_raise", methods=["POST"])
def front_raise():
    video = request.files["video"]
    video.save("uploads1/" + video.filename)
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Set up Mediapipe Pose model
    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as pose:
        # Open video file

        cap = cv2.VideoCapture(
            "uploads1/" + video.filename
        )  # Replace 'path_to_video_file.mp4' with your video file path
        if not cap.isOpened():
            return "Failed to open the video file."
        # Initialize variables
        front_raise_started = False
        front_raise_ended = False
        front_raise_counter = 0

        while cap.isOpened():
            # Read frame from video
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB for Mediapipe Pose model
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process image with Mediapipe Pose model
            results = pose.process(image)

            # Draw landmarks on image
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

            # Extract landmarks of interest
            if results.pose_landmarks is not None:
                left_shoulder = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_SHOULDER
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_SHOULDER
                        ].y,
                    ]
                )
                right_shoulder = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_SHOULDER
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_SHOULDER
                        ].y,
                    ]
                )
                left_elbow = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_ELBOW
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_ELBOW
                        ].y,
                    ]
                )
                right_elbow = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_ELBOW
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_ELBOW
                        ].y,
                    ]
                )

                # Calculate angles between shoulders and elbows
                angle_left = np.degrees(
                    np.arctan2(
                        left_elbow[1] - left_shoulder[1],
                        left_elbow[0] - left_shoulder[0],
                    )
                )
                angle_right = np.degrees(
                    np.arctan2(
                        right_elbow[1] - right_shoulder[1],
                        right_elbow[0] - right_shoulder[0],
                    )
                )

                # Check if front raise started or ended
                if angle_left < 45 or angle_right < 45:
                    if not front_raise_started:
                        front_raise_started = True
                        front_raise_ended = False
                else:
                    if front_raise_started:
                        if not front_raise_ended:
                            front_raise_counter += 1
                            front_raise_ended = True
                        front_raise_started = False

                # Display front raise counter
                counter_text = f"Front Raise Counter: {front_raise_counter}"
                cv2.putText(
                    image,
                    counter_text,
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

            # Display image
            cv2.imshow("Front Raise Detection", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Release video capture and close windows
        cap.release()
        cv2.destroyAllWindows()
        return f"Front Raise done the counts are {front_raise_counter}"


@app.route("/front_squats", methods=["POST"])
def front_squats():
    video = request.files["video"]
    video.save("uploads1/" + video.filename)
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Set up Mediapipe Pose model
    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as pose:
        # Open video file
        cap = cv2.VideoCapture("uploads1/" + video.filename)
        if not cap.isOpened():
            return "Failed to open the video file."
        # Initialize variables
        front_squat_started = False
        front_squat_ended = False
        front_squat_counter = 0

        while cap.isOpened():
            # Read frame from video
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB for Mediapipe Pose model
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process image with Mediapipe Pose model
            results = pose.process(image)

            # Draw landmarks on image
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

            # Extract landmarks of interest
            if results.pose_landmarks is not None:
                left_hip = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_HIP
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_HIP
                        ].y,
                    ]
                )
                right_hip = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_HIP
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_HIP
                        ].y,
                    ]
                )
                left_knee = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_KNEE
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_KNEE
                        ].y,
                    ]
                )
                right_knee = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_KNEE
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_KNEE
                        ].y,
                    ]
                )

                # Calculate angles between hips and knees
                angle_left = np.degrees(
                    np.arctan2(left_knee[1] - left_hip[1], left_knee[0] - left_hip[0])
                )
                angle_right = np.degrees(
                    np.arctan2(
                        right_knee[1] - right_hip[1], right_knee[0] - right_hip[0]
                    )
                )

                # Check if front squat started or ended
                if angle_left < 90 and angle_right < 90:
                    if not front_squat_started:
                        front_squat_started = True
                        front_squat_ended = False
                else:
                    if front_squat_started:
                        if not front_squat_ended:
                            front_squat_counter += 1
                            front_squat_ended = True
                        front_squat_started = False

                # Display front squat counter
                counter_text = f"Front Squat Counter: {front_squat_counter}"
                cv2.putText(
                    image,
                    counter_text,
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

            # Display image
            cv2.imshow("Front Squat Detection", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Release video capture and close windows
        cap.release()
        cv2.destroyAllWindows()
        return f"Front Squats done the counts are {front_squat_counter}"


@app.route("/back_squats", methods=["POST"])
def back_squats():
    video = request.files["video"]
    video.save("uploads1/" + video.filename)

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Set up Mediapipe Pose model
    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as pose:
        # Open video file
        cap = cv2.VideoCapture("uploads1/" + video.filename)
        if not cap.isOpened():
            return "Failed to open the video file."
        # Initialize variables
        back_squat_started = False
        back_squat_ended = False
        back_squat_counter = 0

        while cap.isOpened():
            # Read frame from video
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB for Mediapipe Pose model
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process image with Mediapipe Pose model
            results = pose.process(image)

            # Draw landmarks on image
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

            # Extract landmarks of interest
            if results.pose_landmarks is not None:
                left_hip = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_HIP
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_HIP
                        ].y,
                    ]
                )
                right_hip = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_HIP
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_HIP
                        ].y,
                    ]
                )
                left_knee = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_KNEE
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_KNEE
                        ].y,
                    ]
                )
                right_knee = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_KNEE
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_KNEE
                        ].y,
                    ]
                )
                left_shoulder = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_SHOULDER
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_SHOULDER
                        ].y,
                    ]
                )
                right_shoulder = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_SHOULDER
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_SHOULDER
                        ].y,
                    ]
                )

                # Calculate angles between hips and knees
                angle_left = np.degrees(
                    np.arctan2(left_knee[1] - left_hip[1], left_knee[0] - left_hip[0])
                )
                angle_right = np.degrees(
                    np.arctan2(
                        right_knee[1] - right_hip[1], right_knee[0] - right_hip[0]
                    )
                )

                # Calculate angle between shoulders and knees
                angle_shoulder_knee = np.degrees(
                    np.arctan2(
                        right_knee[1] - right_shoulder[1],
                        right_knee[0] - right_shoulder[0],
                    )
                )

                # Check if back squat started or ended
                if angle_left > 90 and angle_right > 90 and angle_shoulder_knee > 90:
                    if not back_squat_started:
                        back_squat_started = True
                        back_squat_ended = False
                else:
                    if back_squat_started:
                        if not back_squat_ended:
                            back_squat_counter += 1
                            back_squat_ended = True
                        back_squat_started = False

                # Display back squat counter
                counter_text = f"Back Squat Counter: {back_squat_counter}"
                cv2.putText(
                    image,
                    counter_text,
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

            # Display image
            cv2.imshow("Back Squat Detection", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Release video capture and close windows
        cap.release()
        cv2.destroyAllWindows()
        return f"Back Squats done the counts are{back_squat_counter}"


@app.route("/yoga", methods=["POST"])
def yoga():
    video = request.files["video"]
    video.save("uploads1/" + video.filename)
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Initialize the pose detection model
    pose_detection = mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    )

    # Initialize the start time
    start_time = None

    # Define the yoga pose to be detected
    POSE = {
        "Tree Pose": [mp_pose.PoseLandmark.LEFT_ANKLE, mp_pose.PoseLandmark.RIGHT_HIP],
        "Warrior II": [
            mp_pose.PoseLandmark.LEFT_ANKLE,
            mp_pose.PoseLandmark.LEFT_HIP,
            mp_pose.PoseLandmark.LEFT_SHOULDER,
        ],
        "Downward Dog": [
            mp_pose.PoseLandmark.LEFT_ANKLE,
            mp_pose.PoseLandmark.RIGHT_ANKLE,
            mp_pose.PoseLandmark.LEFT_WRIST,
            mp_pose.PoseLandmark.RIGHT_WRIST,
        ],
        # Add more yoga poses here
    }

    # Capture frames from the camera
    cap = cv2.VideoCapture("uploads1/" + video.filename)
    if not cap.isOpened():
        return "Failed to open the video file."

    while True:
        ret, frame = cap.read()

        # Convert the image to RGB for Mediapipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Run pose detection on the image
        results = pose_detection.process(image)

        # Draw the detected landmarks on the image
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
        )

        # Check if a yoga pose is being performed
        if results.pose_landmarks is not None:
            for pose_name, pose_landmarks in POSE.items():
                pose_detected = True
                for landmark in pose_landmarks:
                    if not results.pose_landmarks.landmark[landmark]:
                        pose_detected = False
                        break
                if pose_detected:
                    # If the start time is not set, set it to the current time
                    if start_time is None:
                        start_time = time.time()
                    # Calculate the time duration for which the pose has been held
                    duration = round(time.time() - start_time, 2)
                    # Display the pose name and duration on the screen
                    cv2.putText(
                        image,
                        pose_name + " for " + str(duration) + "s",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2,
                    )
                    break
            else:
                # Reset the start time if no pose is detected
                start_time = None

        # Show the image
        cv2.imshow("MediaPipe Pose", image)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return "Yoga detection completed."


@app.route("/Bicep_live", methods=["POST"])
def Bicep_live():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Set up Mediapipe Pose model
    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as pose:
        # Open video file
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return "Failed to open the video file."

        # Initialize variables
        curl_count = 0
        curl_started = False
        curl_ended = False
        previous_angle = 0

        while True:
            # Read frame from video
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB for Mediapipe Pose model
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process image with Mediapipe Pose model
            results = pose.process(image)

            # Draw landmarks on image
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

            # Extract landmarks of interest
            if results.pose_landmarks is not None:
                right_shoulder = results.pose_landmarks.landmark[
                    mp_pose.PoseLandmark.RIGHT_SHOULDER
                ]
                right_elbow = results.pose_landmarks.landmark[
                    mp_pose.PoseLandmark.RIGHT_ELBOW
                ]
                right_wrist = results.pose_landmarks.landmark[
                    mp_pose.PoseLandmark.RIGHT_WRIST
                ]

                # Calculate angle between arm and body
                a = np.array([right_shoulder.x, right_shoulder.y])
                b = np.array([right_elbow.x, right_elbow.y])
                c = np.array([right_wrist.x, right_wrist.y])
                angle = np.degrees(
                    np.arccos(
                        np.dot(b - a, c - b)
                        / (np.linalg.norm(b - a) * np.linalg.norm(c - b))
                    )
                )

                # Check if bicep curl started or ended
                if angle < 90 and not curl_started:
                    curl_started = True
                elif angle >= 90 and curl_started:
                    curl_count += 1
                    curl_started = False
                    curl_ended = True

                # If bicep curl ended, print number of curls and angle of last curl
                if curl_ended:
                    curl_ended = False
                    print(f"Curls: {curl_count}")
                    print(f"Angle: {previous_angle}")

                previous_angle = angle

            # Display rep counter
            counter_text = f"Curls: {curl_count}"
            cv2.putText(
                image,
                counter_text,
                (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )

            # Display image with landmarks
            cv2.imshow("Bicep Curl Detection", image)

            # Exit program when 'q' key is pressed
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

        # Release video file and close windows
        cap.release()
        cv2.destroyAllWindows()

        return f"Bicep curl done the counts are {curl_count}"


@app.route("/push_up_live", methods=["POST"])
def push_up_live():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Set up Mediapipe Pose model
    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as pose:
        # Open video file
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return "Failed to open the video file."
        # Replace 'path_to_video_file.mp4' with your video file path

        # Initialize variables
        pushup_jack_count = 0
        pushup_jack_started = False
        pushup_jack_ended = False
        previous_angle = 0

        while cap.isOpened():
            # Read frame from video
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB for Mediapipe Pose model
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process image with Mediapipe Pose model
            results = pose.process(image)

            # Draw landmarks on image
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

            # Extract landmarks of interest
            if results.pose_landmarks is not None:
                left_shoulder = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_SHOULDER
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_SHOULDER
                        ].y,
                    ]
                )
                left_elbow = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_ELBOW
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_ELBOW
                        ].y,
                    ]
                )
                left_wrist = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_WRIST
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_WRIST
                        ].y,
                    ]
                )

                # Calculate angle between arm and body
                a = np.linalg.norm(left_shoulder - left_elbow)
                b = np.linalg.norm(left_elbow - left_wrist)
                c = np.linalg.norm(left_shoulder - left_wrist)
                angle = (
                    np.arccos((a**2 + b**2 - c**2) / (2 * a * b)) * 180 / np.pi
                )

                # Check if push-up jack started or ended
                if angle > 160 and not pushup_jack_started:
                    pushup_jack_started = True
                elif angle < 60 and pushup_jack_started:
                    pushup_jack_count += 1
                    pushup_jack_ended = True

                # If push-up jack ended, print number of repetitions and angle of last movement
                if pushup_jack_ended:
                    pushup_jack_started = False
                    pushup_jack_ended = False
                    print(f"Push-Up Jacks: {pushup_jack_count}")
                    print(f"Angle: {previous_angle}")

                # Display rep counter
                counter_text = f"Push-Up Jacks: {pushup_jack_count}"
                cv2.putText(
                    image,
                    counter_text,
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

                previous_angle = angle

            # Display image with landmarks
            cv2.imshow("Push-Up Jack Detection", image)

            # Exit program when 'q' key is pressed
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

        # Release video and close windows
        cap.release()
        cv2.destroyAllWindows()
        return f"push up done the counts are {pushup_jack_count}"


@app.route("/push_up_hold_live", methods=["POST"])
def push_up_hold_live():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Set up Mediapipe Pose model
    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as pose:
        # Open video file

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return "Failed to open the video file."
        # Initialize variables
        pushup_hold_started = False
        pushup_hold_ended = False
        start_time = 0
        duration = 0

        while cap.isOpened():
            # Read frame from video
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB for Mediapipe Pose model
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process image with Mediapipe Pose model
            results = pose.process(image)

            # Draw landmarks on image
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

            # Extract landmarks of interest
            if results.pose_landmarks is not None:
                left_shoulder = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_SHOULDER
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_SHOULDER
                        ].y,
                    ]
                )
                right_shoulder = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_SHOULDER
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_SHOULDER
                        ].y,
                    ]
                )
                left_elbow = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_ELBOW
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_ELBOW
                        ].y,
                    ]
                )
                right_elbow = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_ELBOW
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_ELBOW
                        ].y,
                    ]
                )

                # Calculate angles between shoulders and elbows
                angle_left = np.degrees(
                    np.arctan2(
                        left_elbow[1] - left_shoulder[1],
                        left_elbow[0] - left_shoulder[0],
                    )
                )
                angle_right = np.degrees(
                    np.arctan2(
                        right_elbow[1] - right_shoulder[1],
                        right_elbow[0] - right_shoulder[0],
                    )
                )

                # Check if push-up hold started or ended
                if angle_left < 90 and angle_right < 90 and not pushup_hold_started:
                    pushup_hold_started = True
                    start_time = time.time()
                elif (angle_left >= 90 or angle_right >= 90) and pushup_hold_started:
                    pushup_hold_ended = True

                # If push-up hold ended, print duration of the hold
                if pushup_hold_ended:
                    pushup_hold_started = False
                    pushup_hold_ended = False
                    end_time = time.time()
                    duration = end_time - start_time
                    print(f"Push-Up Hold Time: {duration:.2f} seconds")

                # Display hold duration
                counter_text = (
                    f"Push-Up Hold Time: {duration:.2f} seconds"
                    if pushup_hold_started
                    else ""
                )
                cv2.putText(
                    image,
                    counter_text,
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

            # Display image with landmarks
            cv2.imshow("Push-Up Hold Detection", image)

            # Exit program when 'q' key is pressed
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

        # Release video and close windows
        cap.release()
        cv2.destroyAllWindows()
        return "push up hold detection completed."


@app.route("/shoulder_press_live", methods=["POST"])
def shoulder_press_live():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Set up Mediapipe Pose model
    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as pose:
        # Open video file
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return "Failed to open the video file."

        # Initialize variables
        shoulder_press_started = False
        shoulder_press_ended = False
        shoulder_press_counter = 0

        while cap.isOpened():
            # Read frame from video
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB for Mediapipe Pose model
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process image with Mediapipe Pose model
            results = pose.process(image)

            # Draw landmarks on image
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

            # Extract landmarks of interest
            if results.pose_landmarks is not None:
                left_shoulder = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_SHOULDER
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_SHOULDER
                        ].y,
                    ]
                )
                right_shoulder = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_SHOULDER
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_SHOULDER
                        ].y,
                    ]
                )
                left_elbow = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_ELBOW
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_ELBOW
                        ].y,
                    ]
                )
                right_elbow = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_ELBOW
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_ELBOW
                        ].y,
                    ]
                )

                # Calculate angles between shoulders and elbows
                angle_left = np.degrees(
                    np.arctan2(
                        left_elbow[1] - left_shoulder[1],
                        left_elbow[0] - left_shoulder[0],
                    )
                )
                angle_right = np.degrees(
                    np.arctan2(
                        right_elbow[1] - right_shoulder[1],
                        right_elbow[0] - right_shoulder[0],
                    )
                )

                # Check if shoulder press started or ended
                if angle_left < 45 and angle_right < 45 and not shoulder_press_started:
                    shoulder_press_started = True
                elif (angle_left >= 45 or angle_right >= 45) and shoulder_press_started:
                    shoulder_press_counter += 1
                    shoulder_press_started = False

                # Display shoulder press counter
                counter_text = f"Shoulder Press Counter: {shoulder_press_counter}"
                cv2.putText(
                    image,
                    counter_text,
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

            # Display image
            cv2.imshow("Shoulder Press Detection", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Release video capture and close windows
        cap.release()
        cv2.destroyAllWindows()
        return f"shoulder press done the counts are {shoulder_press_counter}"


@app.route("/front_raise_live", methods=["POST"])
def front_raise_live():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Set up Mediapipe Pose model
    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as pose:
        # Open video file

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return "Failed to open the video file."
        # Initialize variables
        front_raise_started = False
        front_raise_ended = False
        front_raise_counter = 0

        while cap.isOpened():
            # Read frame from video
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB for Mediapipe Pose model
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process image with Mediapipe Pose model
            results = pose.process(image)

            # Draw landmarks on image
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

            # Extract landmarks of interest
            if results.pose_landmarks is not None:
                left_shoulder = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_SHOULDER
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_SHOULDER
                        ].y,
                    ]
                )
                right_shoulder = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_SHOULDER
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_SHOULDER
                        ].y,
                    ]
                )
                left_elbow = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_ELBOW
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_ELBOW
                        ].y,
                    ]
                )
                right_elbow = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_ELBOW
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_ELBOW
                        ].y,
                    ]
                )

                # Calculate angles between shoulders and elbows
                angle_left = np.degrees(
                    np.arctan2(
                        left_elbow[1] - left_shoulder[1],
                        left_elbow[0] - left_shoulder[0],
                    )
                )
                angle_right = np.degrees(
                    np.arctan2(
                        right_elbow[1] - right_shoulder[1],
                        right_elbow[0] - right_shoulder[0],
                    )
                )

                # Check if front raise started or ended
                if angle_left < 45 or angle_right < 45:
                    if not front_raise_started:
                        front_raise_started = True
                        front_raise_ended = False
                else:
                    if front_raise_started:
                        if not front_raise_ended:
                            front_raise_counter += 1
                            front_raise_ended = True
                        front_raise_started = False

                # Display front raise counter
                counter_text = f"Front Raise Counter: {front_raise_counter}"
                cv2.putText(
                    image,
                    counter_text,
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

            # Display image
            cv2.imshow("Front Raise Detection", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Release video capture and close windows
        cap.release()
        cv2.destroyAllWindows()
        return f"Front Raise done the counts are {front_raise_counter}"


@app.route("/front_squats_live", methods=["POST"])
def front_squats_live():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Set up Mediapipe Pose model
    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as pose:
        # Open video file
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return "Failed to open the video file."
        # Initialize variables
        front_squat_started = False
        front_squat_ended = False
        front_squat_counter = 0

        while cap.isOpened():
            # Read frame from video
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB for Mediapipe Pose model
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process image with Mediapipe Pose model
            results = pose.process(image)

            # Draw landmarks on image
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

            # Extract landmarks of interest
            if results.pose_landmarks is not None:
                left_hip = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_HIP
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_HIP
                        ].y,
                    ]
                )
                right_hip = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_HIP
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_HIP
                        ].y,
                    ]
                )
                left_knee = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_KNEE
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_KNEE
                        ].y,
                    ]
                )
                right_knee = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_KNEE
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_KNEE
                        ].y,
                    ]
                )

                # Calculate angles between hips and knees
                angle_left = np.degrees(
                    np.arctan2(left_knee[1] - left_hip[1], left_knee[0] - left_hip[0])
                )
                angle_right = np.degrees(
                    np.arctan2(
                        right_knee[1] - right_hip[1], right_knee[0] - right_hip[0]
                    )
                )

                # Check if front squat started or ended
                if angle_left < 90 and angle_right < 90:
                    if not front_squat_started:
                        front_squat_started = True
                        front_squat_ended = False
                else:
                    if front_squat_started:
                        if not front_squat_ended:
                            front_squat_counter += 1
                            front_squat_ended = True
                        front_squat_started = False

                # Display front squat counter
                counter_text = f"Front Squat Counter: {front_squat_counter}"
                cv2.putText(
                    image,
                    counter_text,
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

            # Display image
            cv2.imshow("Front Squat Detection", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Release video capture and close windows
        cap.release()
        cv2.destroyAllWindows()
        return f"Front Squats done the counts are {front_squat_counter}"


@app.route("/back_squats_live", methods=["POST"])
def back_squats_live():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Set up Mediapipe Pose model
    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as pose:
        # Open video file
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return "Failed to open the video file."
        # Initialize variables
        back_squat_started = False
        back_squat_ended = False
        back_squat_counter = 0

        while cap.isOpened():
            # Read frame from video
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB for Mediapipe Pose model
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process image with Mediapipe Pose model
            results = pose.process(image)

            # Draw landmarks on image
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

            # Extract landmarks of interest
            if results.pose_landmarks is not None:
                left_hip = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_HIP
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_HIP
                        ].y,
                    ]
                )
                right_hip = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_HIP
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_HIP
                        ].y,
                    ]
                )
                left_knee = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_KNEE
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_KNEE
                        ].y,
                    ]
                )
                right_knee = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_KNEE
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_KNEE
                        ].y,
                    ]
                )
                left_shoulder = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_SHOULDER
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_SHOULDER
                        ].y,
                    ]
                )
                right_shoulder = np.array(
                    [
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_SHOULDER
                        ].x,
                        results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_SHOULDER
                        ].y,
                    ]
                )

                # Calculate angles between hips and knees
                angle_left = np.degrees(
                    np.arctan2(left_knee[1] - left_hip[1], left_knee[0] - left_hip[0])
                )
                angle_right = np.degrees(
                    np.arctan2(
                        right_knee[1] - right_hip[1], right_knee[0] - right_hip[0]
                    )
                )

                # Calculate angle between shoulders and knees
                angle_shoulder_knee = np.degrees(
                    np.arctan2(
                        right_knee[1] - right_shoulder[1],
                        right_knee[0] - right_shoulder[0],
                    )
                )

                # Check if back squat started or ended
                if angle_left > 90 and angle_right > 90 and angle_shoulder_knee > 90:
                    if not back_squat_started:
                        back_squat_started = True
                        back_squat_ended = False
                else:
                    if back_squat_started:
                        if not back_squat_ended:
                            back_squat_counter += 1
                            back_squat_ended = True
                        back_squat_started = False

                # Display back squat counter
                counter_text = f"Back Squat Counter: {back_squat_counter}"
                cv2.putText(
                    image,
                    counter_text,
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

            # Display image
            cv2.imshow("Back Squat Detection", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Release video capture and close windows
        cap.release()
        cv2.destroyAllWindows()
        return f"Back Squats done the counts are {back_squat_counter}"


@app.route("/yoga_live", methods=["POST"])
def yoga_live():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Initialize the pose detection model
    pose_detection = mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    )

    # Initialize the start time
    start_time = None

    # Define the yoga pose to be detected
    POSE = {
        "Tree Pose": [mp_pose.PoseLandmark.LEFT_ANKLE, mp_pose.PoseLandmark.RIGHT_HIP],
        "Warrior II": [
            mp_pose.PoseLandmark.LEFT_ANKLE,
            mp_pose.PoseLandmark.LEFT_HIP,
            mp_pose.PoseLandmark.LEFT_SHOULDER,
        ],
        "Downward Dog": [
            mp_pose.PoseLandmark.LEFT_ANKLE,
            mp_pose.PoseLandmark.RIGHT_ANKLE,
            mp_pose.PoseLandmark.LEFT_WRIST,
            mp_pose.PoseLandmark.RIGHT_WRIST,
        ],
        # Add more yoga poses here
    }

    # Capture frames from the camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Failed to open the video file."

    while True:
        ret, frame = cap.read()

        # Convert the image to RGB for Mediapipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Run pose detection on the image
        results = pose_detection.process(image)

        # Draw the detected landmarks on the image
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
        )

        # Check if a yoga pose is being performed
        if results.pose_landmarks is not None:
            for pose_name, pose_landmarks in POSE.items():
                pose_detected = True
                for landmark in pose_landmarks:
                    if not results.pose_landmarks.landmark[landmark]:
                        pose_detected = False
                        break
                if pose_detected:
                    # If the start time is not set, set it to the current time
                    if start_time is None:
                        start_time = time.time()
                    # Calculate the time duration for which the pose has been held
                    duration = round(time.time() - start_time, 2)
                    # Display the pose name and duration on the screen
                    cv2.putText(
                        image,
                        pose_name + " for " + str(duration) + "s",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2,
                    )
                    break
            else:
                # Reset the start time if no pose is detected
                start_time = None

        # Show the image
        cv2.imshow("MediaPipe Pose", image)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return "Yoga detection completed."


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
