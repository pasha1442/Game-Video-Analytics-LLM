import os
import time
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

MEDIA_FOLDER = 'medias'

def __init__():
    if not os.path.exists(MEDIA_FOLDER):
        os.makedirs(MEDIA_FOLDER)

    load_dotenv()  ## load all the environment variables
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)

def save_uploaded_file(uploaded_file):
    """Save the uploaded file to the media folder and return the file path."""
    file_path = os.path.join(MEDIA_FOLDER, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.read())
    return file_path

def get_insights(video_path):
    """Extract insights from the video using Gemini Flash."""
    st.write(f"Processing video: {video_path}")

    st.write(f"Uploading file...")
    video_file = genai.upload_file(path=video_path)
    st.write(f"Completed upload: {video_file.uri}")

    while video_file.state.name == "PROCESSING":
        st.write('Waiting for video to be processed.')
        time.sleep(10)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError(video_file.state.name)
    
    prompt = """
            Analyze the badminton video to extract detailed insights on the following points:

            1. **Rally Duration**: Identify each rally, defined as the continuous gameplay between players from the start of a serve until the shuttlecock touches the floor. Measure the duration of each rally.

            2. **Rally End Points**: Mark the exact timestamp at which each rally ends, specifically when the shuttlecock touches the floor.

            3. **Player Expressions**: Analyze and describe the facial expressions of both players throughout each rally, noting significant moments like rally starts, key shots, and rally ends.

            4. **Score Tracking**: Track the score count, indicating changes after each rally end.

            Provide a comprehensive summary of these aspects for each rally in the video, with timestamps and insights on gameplay flow.
        """

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    st.write("Making LLM inference request...")
    response = model.generate_content([prompt, video_file],
                                    request_options={"timeout": 600})
    st.write(f'Video processing complete')
    st.subheader("Insights")
    st.write(response.text)
    genai.delete_file(video_file.name)


def app():
    st.title("Badmition Insights Generator")

    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])

    if uploaded_file is not None:
        file_path = save_uploaded_file(uploaded_file)
        st.video(file_path)
        get_insights(file_path)
        if os.path.exists(file_path):  ## Optional: Removing uploaded files from the temporary location
            os.remove(file_path)

__init__()
app()



generation_config = {
    "temperature": 1,
    "top_p": 0.95, 
    "top_k": 64,
    # "max_output_tokens": 16384,
    "response_schema": content.Schema(
        type=content.Type.OBJECT,
        required=["match"],
        properties={
            "match": content.Schema(
                type=content.Type.OBJECT,
                properties={
                    "Player1": content.Schema(type=content.Type.STRING),
                    "Player2": content.Schema(type=content.Type.STRING),
                    "Player1 Score": content.Schema(type=content.Type.INTEGER),
                    "Player2 Score": content.Schema(type=content.Type.INTEGER),
                    "rally_count": content.Schema(type=content.Type.INTEGER),
                    "Rallies": content.Schema(
                        type=content.Type.ARRAY,
                        items=content.Schema(
                            type=content.Type.OBJECT,
                            required=["from", "to", "rally_shots_count", "Court Reach", "Footwork", "Stamina", "Fouls", "Smashes"],
                            properties={
                                "from": content.Schema(type=content.Type.STRING),
                                "to": content.Schema(type=content.Type.STRING),
                                "rally_shots_count": content.Schema(type=content.Type.INTEGER),
                                "Court Reach": content.Schema(
                                    type=content.Type.OBJECT,
                                    required=["Player1", "Player2"],
                                    properties={
                                        "Player1": content.Schema(
                                            type=content.Type.OBJECT,
                                            required=["Description", "Timestamp"],
                                            properties={
                                                "Description": content.Schema(type=content.Type.ARRAY, items=content.Schema(type=content.Type.STRING)),
                                                "Timestamp": content.Schema(type=content.Type.ARRAY, items=content.Schema(type=content.Type.STRING)),
                                            },
                                        ),
                                        "Player2": content.Schema(
                                            type=content.Type.OBJECT,
                                            required=["Description", "Timestamp"],
                                            properties={
                                                "Description": content.Schema(type=content.Type.ARRAY, items=content.Schema(type=content.Type.STRING)),
                                                "Timestamp": content.Schema(type=content.Type.ARRAY, items=content.Schema(type=content.Type.STRING)),
                                            },
                                        ),
                                    },
                                ),
                                "Footwork": content.Schema(
                                    type=content.Type.OBJECT,
                                    required=["Player1", "Player2"],
                                    properties={
                                        "Player1": content.Schema(
                                            type=content.Type.OBJECT,
                                            required=["Description", "Timestamp"],
                                            properties={
                                                "Description": content.Schema(type=content.Type.ARRAY, items=content.Schema(type=content.Type.STRING)),
                                                "Timestamp": content.Schema(type=content.Type.ARRAY, items=content.Schema(type=content.Type.STRING)),
                                            },
                                        ),
                                        "Player2": content.Schema(
                                            type=content.Type.OBJECT,
                                            required=["Description", "Timestamp"],
                                            properties={
                                                "Description": content.Schema(type=content.Type.ARRAY, items=content.Schema(type=content.Type.STRING)),
                                                "Timestamp": content.Schema(type=content.Type.ARRAY, items=content.Schema(type=content.Type.STRING)),
                                            },
                                        ),
                                    },
                                ),
                                "Stamina": content.Schema(
                                    type=content.Type.OBJECT,
                                    required=["Player1", "Player2"],
                                    properties={
                                        "Player1": content.Schema(
                                            type=content.Type.OBJECT,
                                            required=["Description", "percentage"],
                                            properties={
                                                "Description": content.Schema(type=content.Type.STRING),
                                                "percentage": content.Schema(type=content.Type.INTEGER),
                                            },
                                        ),
                                        "Player2": content.Schema(
                                            type=content.Type.OBJECT,
                                            required=["Description", "percentage"],
                                            properties={
                                                "Description": content.Schema(type=content.Type.STRING),
                                                "percentage": content.Schema(type=content.Type.INTEGER),
                                            },
                                        ),
                                    },
                                ),
                                "Fouls": content.Schema(
                                    type=content.Type.OBJECT,
                                    required=["Player1", "Player2"],
                                    properties={
                                        "Player1": content.Schema(
                                            type=content.Type.OBJECT,
                                            required=["count", "Description", "Timestamp"],
                                            properties={
                                                "count": content.Schema(type=content.Type.INTEGER),
                                                "Description": content.Schema(type=content.Type.ARRAY, items=content.Schema(type=content.Type.STRING)),
                                                "Timestamp": content.Schema(type=content.Type.ARRAY, items=content.Schema(type=content.Type.STRING)),
                                            },
                                        ),
                                        "Player2": content.Schema(
                                            type=content.Type.OBJECT,
                                            required=["count", "Description", "Timestamp"],
                                            properties={
                                                "count": content.Schema(type=content.Type.INTEGER),
                                                "Description": content.Schema(type=content.Type.ARRAY, items=content.Schema(type=content.Type.STRING)),
                                                "Timestamp": content.Schema(type=content.Type.ARRAY, items=content.Schema(type=content.Type.STRING)),
                                            },
                                        ),
                                    },
                                ),
                                "Smashes": content.Schema(
                                    type=content.Type.OBJECT,
                                    required=["Player1", "Player2"],
                                    properties={
                                        "Player1": content.Schema(
                                            type=content.Type.OBJECT,
                                            required=["count", "Timestamp"],
                                            properties={
                                                "count": content.Schema(type=content.Type.INTEGER),
                                                "Timestamp": content.Schema(type=content.Type.ARRAY, items=content.Schema(type=content.Type.STRING)),
                                            },
                                        ),
                                        "Player2": content.Schema(
                                            type=content.Type.OBJECT,
                                            required=["count", "Timestamp"],
                                            properties={
                                                "count": content.Schema(type=content.Type.INTEGER),
                                                "Timestamp": content.Schema(type=content.Type.ARRAY, items=content.Schema(type=content.Type.STRING)),
                                            },
                                        ),
                                    },
                                ),
                            },
                        ),
                    ),
                },
            ),
        },
    ),
    "response_mime_type": "application/json",
}