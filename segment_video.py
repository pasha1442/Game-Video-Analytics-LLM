import os
import time
import json
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
from dotenv import load_dotenv
import streamlit as st
from segment_rallies import split_video
from glob import glob


# Initialize constants
MEDIA_FOLDER = 'medias'

def init_app():
    """Initialize the application settings and configurations"""
    if not os.path.exists(MEDIA_FOLDER):
        os.makedirs(MEDIA_FOLDER)
    
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    # Initialize session state for storing analysis results
    if 'analysis_results' not in st.session_state:
        st.session_state['analysis_results'] = None

def get_generation_config():
    """Return the generation configuration for Gemini model"""
    return {
    "temperature": 1,
    "top_p": 0.90, 
    "top_k": 64,
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

def save_uploaded_file(uploaded_file):
    """Save the uploaded file to the media folder and return the file path"""
    file_path = os.path.join(MEDIA_FOLDER, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def analyze_video(file_path):
    """Process the video using Gemini API and return analysis results"""
    with st.spinner("Initializing Gemini model..."):
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=get_generation_config(),
            system_instruction="""As a badminton analysis expert, evaluate each rally in the provided match video based on official badminton rules.
                                Begin a new rally when the shuttlecock touches the floor or if there is a noticeable pause between points. 
                                For each rally, assess the following:
                                Court Reach: Determine how effectively each player covers the court, noting any areas of strength or weakness.
                                Footwork: Analyze the players' footwork techniques and agility, highlighting any breakdowns or strengths.
                                Stamina: Assess the players’ endurance, noting if either shows signs of fatigue.
                                Smashes: Identify and timestamp any smashes, along with their effectiveness and player position.
                                Provide timestamps for specific actions within each rally and track the score incrementally for both players across rallies. 
                                Format the output according to the provided JSON schema, capturing every element accurately."""
        )

    with st.spinner("Uploading video to Gemini..."):
        video_file = genai.upload_file(file_path, mime_type="video/mp4")
        
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Wait for file processing
    while video_file.state.name == "PROCESSING":
        status_text.text("Processing video... Please wait.")
        time.sleep(10)
        video_file = genai.get_file(video_file.name)
        progress_bar.progress(0.5)

    if video_file.state.name == "FAILED":
        st.error("Video processing failed. Please try again.")
        return None

    with st.spinner("Analyzing video..."):
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [video_file],
                }
            ]
        )

        response = chat_session.send_message(
            """Analyze the provided badminton video and output detailed observations and description for each rally.
            A new rally starts each time a player scores a point. Include analysis of each player's court reach, footwork,
            stamina, fouls, smashes, and provide timestamps. Count the shots per rally and dynamically count all rallies within
            the match. Use the provided JSON schema."""
        )
        
        progress_bar.progress(1.0)
        status_text.text("Analysis complete!")
        
        return json.loads(response.text)

def display_analysis_results(results):
    """Display the analysis results in a structured format"""
    if not results or 'match' not in results:
        st.error("No valid analysis results to display")
        return

    match_data = results['match']
    
    # Display match overview
    st.header("Match Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Player 1", match_data['Player1'])
        st.metric("Score", match_data['Player1 Score'])
    with col2:
        st.metric("Total Rallies", match_data['rally_count'])
    with col3:
        st.metric("Player 2", match_data['Player2'])
        st.metric("Score", match_data['Player2 Score'])

    # Display rally details
    st.header("Rally Analysis")
    for idx, rally in enumerate(match_data['Rallies'], 1):
        with st.expander(f"Rally {idx} ({rally['from']} - {rally['to']})"):
            st.metric("Shots in Rally", rally['rally_shots_count'])
            
            # Court Reach Analysis
            st.subheader("Court Reach")
            col1, col2 = st.columns(2)
            with col1:
                st.write("Player 1")
                for desc, time in zip(rally['Court Reach']['Player1']['Description'],
                                    rally['Court Reach']['Player1']['Timestamp']):
                    st.write(f"- {desc} ({time})")
            with col2:
                st.write("Player 2")
                for desc, time in zip(rally['Court Reach']['Player2']['Description'],
                                    rally['Court Reach']['Player2']['Timestamp']):
                    st.write(f"- {desc} ({time})")

            # Stamina Analysis
            st.subheader("Stamina")
            col1, col2 = st.columns(2)
            with col1:
                st.progress(rally['Stamina']['Player1']['percentage'] / 100)
                st.write(rally['Stamina']['Player1']['Description'])
            with col2:
                st.progress(rally['Stamina']['Player2']['percentage'] / 100)
                st.write(rally['Stamina']['Player2']['Description'])

            # Smashes Analysis
            st.subheader("Smashes")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Player 1 Smashes", rally['Smashes']['Player1']['count'])
                if rally['Smashes']['Player1']['Timestamp']:
                    st.write("Timestamps:", ", ".join(rally['Smashes']['Player1']['Timestamp']))
            with col2:
                st.metric("Player 2 Smashes", rally['Smashes']['Player2']['count'])
                if rally['Smashes']['Player2']['Timestamp']:
                    st.write("Timestamps:", ", ".join(rally['Smashes']['Player2']['Timestamp']))

def main():
    
    timestamps = {
        "rallies": [
            { "start": 0.05, "end": 0.2 },
            { "start": 0.24, "end": 0.39 },
            { "start": 0.41, "end": 0.47 },
            { "start": 0.49, "end": 0.77 },
            { "start": 0.79, "end": 1.13 },
            { "start": 1.17, "end": 1.21 },
            { "start": 1.24, "end": 1.3 },
            { "start": 1.32, "end": 1.43 },
            { "start": 1.45, "end": 2.01 },
            { "start": 2.03, "end": 2.18 },
            { "start": 2.19, "end": 2.23 },
            { "start": 2.26, "end": 2.31 },
            { "start": 2.33, "end": 2.37 },
            { "start": 2.38, "end": 2.51 }
        ]
    }
    st.set_page_config(page_title="Badminton Match Analyzer", layout="wide")
    init_app()
    
    st.title("🏸 Badminton Match Analysis")
    st.write("Upload a badminton match video for detailed analysis of player performance, rallies, and statistics.")
    
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])
    
    if uploaded_file:
        st.video(uploaded_file)
        
        if st.button("Analyze Video"):
            file_path = save_uploaded_file(uploaded_file)
            split_video(file_path, timestamps)         

            segments_dir = "/home/auriga/Documents/Badmition_Video_Analytics/video_segments"
            
            try:
                # Get all video segments
                video_segments = glob(os.path.join(segments_dir, "*.[mM][pP]4"))
                
                if not video_segments:
                    st.error("No video segments found after splitting.")
                    return
                
                # Create progress bar
                progress_bar = st.progress(0)
                all_results = []
                
                # Process each segment
                for idx, segment_path in enumerate(video_segments):
                    st.write(f"Analyzing rally {idx + 1}/{len(video_segments)}")
                    print("==========================================",segment_path)
                    
                    try:
                        # Analyze current segment
                        segment_results = analyze_video(segment_path)
                        
                        if segment_results:
                            # Add segment identifier
                            segment_results['segment_id'] = idx + 1
                            segment_results['timestamp'] = timestamps['rallies'][idx]
                            all_results.append(segment_results)
                            
                            # Show individual segment results
                            with st.expander(f"Rally {idx + 1} Analysis"):
                                display_analysis_results(segment_results)
                    
                    except Exception as e:
                        st.error(f"Error analyzing rally {idx + 1}: {str(e)}")
                    
                    # Update progress
                    progress_bar.progress((idx + 1) / len(video_segments))
                
                # Store and display combined results
                if all_results:
                    combined_results = {
                        'individual_rallies': all_results,
                        'total_rallies': len(all_results),
                        'timestamps': timestamps,
                        'summary': calculate_summary(all_results)  # You'll need to implement this
                    }
                    
                    st.session_state['analysis_results'] = combined_results
                    
                    st.write("### Overall Match Analysis")
                    display_combined_results(combined_results)  # You'll need to implement this
                    
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
            finally:
                # Cleanup
                if os.path.exists(file_path):
                    os.remove(file_path)
                # Optionally, clean up segments:
                # for segment in video_segments:
                #     if os.path.exists(segment):
                #         os.remove(segment)
    
    # Display previous results if they exist
    elif st.session_state.get('analysis_results'):
        display_analysis_results(st.session_state['analysis_results'])
        
    def calculate_summary(all_results):
        """
        Calculate summary statistics from all rally results
        Implement based on your specific metrics
        """
        summary = {
            'total_points': len(all_results),
            'average_rally_duration': 0,
            'longest_rally': 0,
            'shortest_rally': float('inf'),
            'player_statistics': {}
        }
        
        for rally in all_results:
            # Add your specific summary calculations here
            # This is just an example structure
            pass
        
        return summary

    def display_combined_results(combined_results):
        """
        Display the combined analysis results
        Implement based on your specific visualization needs
        """
        st.write(f"Total Rallies Analyzed: {combined_results['total_rallies']}")
        
        # Add your specific visualization code here
        # For example:
        # - Overall match statistics
        # - Rally distribution charts
        # - Player performance summaries
        # - Timeline visualization
        pass

if __name__ == "__main__":
    main()