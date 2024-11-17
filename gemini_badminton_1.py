"""
Install an additional SDK for JSON schema support Google AI Python SDK

$ pip install google.ai.generativelanguage
"""

import os
import time
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

print("Configuring Gemini")
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
print("Configured Gemini")


def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def wait_for_files_active(files):
  
  print("Waiting for file processing...")
  for name in (file.name for file in files):
    file = genai.get_file(name)
    while file.state.name == "PROCESSING":
      print(".", end="", flush=True)
      time.sleep(10)
      file = genai.get_file(name)
    if file.state.name != "ACTIVE":
      raise Exception(f"File {file.name} failed to process")
  print("...all files ready")
  print()


print("Configuring Json for output")







# Configuration for generative model
def create_generation_analyze_config():
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "response_schema": {
        "type": "object",
        "properties": {
            "Rally": {
                "type": "object",
                "properties": {
                    "Player1": { "type": "string" },
                    "Player2": { "type": "string" },
                    "Point_winner": { "type": "string" },
                    "rally_shots_count": { "type": "integer" },
                    "Court Reach": {
                        "type": "object",
                        "properties": {
                            "Player1": {
                                "type": "object",
                                "properties": {
                                    "Description": {
                                        "type": "array",
                                        "items": { "type": "string" }
                                    },
                                    "Timestamp": {
                                        "type": "array",
                                        "items": { "type": "string" }
                                    }
                                },
                                "required": ["Description", "Timestamp"]
                            },
                            "Player2": {
                                "type": "object",
                                "properties": {
                                    "Description": {
                                        "type": "array",
                                        "items": { "type": "string" }
                                    },
                                    "Timestamp": {
                                        "type": "array",
                                        "items": { "type": "string" }
                                    }
                                },
                                "required": ["Description", "Timestamp"]
                            }
                        },
                        "required": ["Player1", "Player2"]
                    },
                    "Footwork": {
                        "type": "object",
                        "properties": {
                            "Player1": {
                                "type": "object",
                                "properties": {
                                    "Description": {
                                        "type": "array",
                                        "items": { "type": "string" }
                                    },
                                    "Timestamp": {
                                        "type": "array",
                                        "items": { "type": "string" }
                                    }
                                },
                                "required": ["Description", "Timestamp"]
                            },
                            "Player2": {
                                "type": "object",
                                "properties": {
                                    "Description": {
                                        "type": "array",
                                        "items": { "type": "string" }
                                    },
                                    "Timestamp": {
                                        "type": "array",
                                        "items": { "type": "string" }
                                    }
                                },
                                "required": ["Description", "Timestamp"]
                            }
                        },
                        "required": ["Player1", "Player2"]
                    },
                    "Stamina": {
                        "type": "object",
                        "properties": {
                            "Player1": {
                                "type": "object",
                                "properties": {
                                    "Description": { "type": "string" },
                                    "percentage": { "type": "integer" }
                                },
                                "required": ["Description", "percentage"]
                            },
                            "Player2": {
                                "type": "object",
                                "properties": {
                                    "Description": { "type": "string" },
                                    "percentage": { "type": "integer" }
                                },
                                "required": ["Description", "percentage"]
                            }
                        },
                        "required": ["Player1", "Player2"]
                    },
                    "Fouls": {
                        "type": "object",
                        "properties": {
                            "Player1": {
                                "type": "object",
                                "properties": {
                                    "Description": {
                                        "type": "array",
                                        "items": { "type": "string" }
                                    },
                                    "Timestamp": {
                                        "type": "array",
                                        "items": { "type": "string" }
                                    }
                                },
                                "required": ["Description", "Timestamp"]
                            },
                            "Player2": {
                                "type": "object",
                                "properties": {
                                
                                    "Description": {
                                        "type": "array",
                                        "items": { "type": "string" }
                                    },
                                    "Timestamp": {
                                        "type": "array",
                                        "items": { "type": "string" }
                                    }
                                },
                                "required": ["Description", "Timestamp"]
                            }
                        },
                        "required": ["Player1", "Player2"]
                    },
                    "Smashes": {
                        "type": "object",
                        "properties": {
                            "Player1": {
                                "type": "object",
                                "properties": {
                                    "count": { "type": "integer" },
                                    "Timestamp": {
                                        "type": "array",
                                        "items": { "type": "string" }
                                    }
                                },
                                "required": ["count", "Timestamp"]
                            },
                            "Player2": {
                                "type": "object",
                                "properties": {
                                    "count": { "type": "integer" },
                                    "Timestamp": {
                                        "type": "array",
                                        "items": { "type": "string" }
                                    }
                                },
                                "required": ["count", "Timestamp"]
                            }
                        },
                        "required": ["Player1", "Player2"]
                    }
                },
                "required": ["Player1", "Player2", "Point_winner", "rally_shots_count", "Court Reach", "Footwork", "Stamina", "Fouls", "Smashes"]
            }
        }
    },
    "response_mime_type": "application/json",
}

    return generation_config

# Configuration for generative model
def create_generation_segment_config():
    return {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "response_mime_type": "application/json",
        "response_schema": {
            "type": "object",
            "properties": {
                "rallies": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "start": {"type": "string"},
                            "end": {"type": "string"}
                        },
                        "required": ["start", "end"]
                    }
                }
            },
            "required": ["rallies"]
        },
    }


# Create the model with system instructions
def create_model(system_instruction,config_type):
    if config_type=="segment":
        print("cosses",config_type)
        generation_config = create_generation_segment_config()
    elif config_type=="analyze":
        generation_config = create_generation_analyze_config()
        
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=system_instruction,
    )
    return model


# Start chat session with the model
def start_chat_session(model, files):
    return model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [files[0]],
            }
        ]
    )

# Send message to get timestamps in JSON format
def get_rally_timestamps(chat_session,prompt):
    response = chat_session.send_message(
        prompt
    )
    return response.text

# Main function to execute the analysis
def analyze_video(file_path,system_instruction,config_type,prompt):
    
    model = create_model(system_instruction,config_type)
    
    # You may need to update the file paths
    files = [
    upload_to_gemini(file_path, mime_type="video/mp4"),
    ]

    # Some files have a processing delay. Wait for them to be ready.
    wait_for_files_active(files)
  
    
    chat_session = start_chat_session(model, files)
    rally_timestamps_json = get_rally_timestamps(chat_session,prompt)
    
    print("Rally Timestamps JSON:", rally_timestamps_json)
    
    # Convert JSON string to a Python dictionary if necessary
    if isinstance(rally_timestamps_json, str):
        rally_timestamps_dict = json.loads(rally_timestamps_json)
    else:
        rally_timestamps_dict = rally_timestamps_json  # Already a dict
        
    return rally_timestamps_dict

def call_to_analyze_video():
    file_path = "/home/auriga/Downloads/videoplayback_4.mp4"
    system_instruction = (
        "As a Badminton Rally Analysis Expert, your task is to analyze each rally video individually, "
        "evaluating both players' court reach, footwork, stamina, fouls, and smashes. For each rally:\n"
        "1. Identify the player who won the point.\n"
        "2. Count the total shots in the rally.\n"
        "3. Assess Court Reach for each player, noting movement across the court and providing descriptive analysis with precise timestamps.\n"
        "4. Analyze Footwork for each player, including descriptions and timestamps for specific movements.\n"
        "5. Evaluate Stamina, describing each player’s energy levels and endurance, with a stamina percentage.\n"
        "6. Track any Fouls, listing the type of foul, descriptions, and timestamps.\n"
        "7. Count and timestamp all Smashes for each player.\n"
        "Generate output in JSON format, using the provided schema for a single rally. Ensure accuracy in timestamps and provide a structured breakdown of the rally dynamics and notable moments for both players."
    )
    config_type = "analyze"
    prompt =  '''"Analyze the provided badminton rally video and output detailed observations. "
                       "A new rally starts each time a player scores a point. Include analysis of each player's court reach, "
                       "footwork, stamina, fouls, smashes, and provide timestamps. Count the shots in this rally only, "
                       "and identify the point winner. Use the provided JSON schema."'''
    final_json = analyze_video(file_path,system_instruction,config_type,prompt)
    print(type(final_json))
    


def call_to_segment_video():
    file_path = "/home/auriga/Documents/Badmition_Video_Analytics/videos/videoplayback_girl.mp4"
    system_instruction = ("""
            You are a badminton expert tasked with analyzing a match video to segment it into individual rallies. 
            Each rally should be split as follows:
            1. A rally ends when the shuttlecock touches the ground, either within court boundaries or resulting in a point for one of the players.
            2. If the shuttlecock is momentarily out of view, assume it is likely airborne due to a high shot. Do not mark a rally break based solely on this invisibility; only conclude the rally if there is clear evidence of it grounding or a point being scored.
            Ensure each rally segment reflects these conditions accurately and precisely.
        """
        )
    
    config_type = "segment"
    prompt =  """
            Analyze the badminton match video and provide the start and end timestamps for each rally. A rally starts when the 
            shuttlecock is served and ends when it touches the ground or a point is scored. If the shuttlecock is not visible, assume 
            it is in play due to a high shot and do not mark it as a rally break.
            Return all timestamps in the following JSON format
        """
            
    final_json = analyze_video(file_path,system_instruction,config_type,prompt)
    
    print(type(final_json))






call_to_segment_video()
# call_to_analyze_video()










# # Create the model
# generation_config = {
#     "temperature": 1,
#     "top_p": 0.95,
#     "top_k": 64,
#     "response_schema": {
#         "type": "object",
#         "properties": {
#             "Rally": {
#                 "type": "object",
#                 "properties": {
#                     "Player1": { "type": "string" },
#                     "Player2": { "type": "string" },
#                     "Point_winner": { "type": "string" },
#                     "rally_shots_count": { "type": "integer" },
#                     "Court Reach": {
#                         "type": "object",
#                         "properties": {
#                             "Player1": {
#                                 "type": "object",
#                                 "properties": {
#                                     "Description": {
#                                         "type": "array",
#                                         "items": { "type": "string" }
#                                     },
#                                     "Timestamp": {
#                                         "type": "array",
#                                         "items": { "type": "string" }
#                                     }
#                                 },
#                                 "required": ["Description", "Timestamp"]
#                             },
#                             "Player2": {
#                                 "type": "object",
#                                 "properties": {
#                                     "Description": {
#                                         "type": "array",
#                                         "items": { "type": "string" }
#                                     },
#                                     "Timestamp": {
#                                         "type": "array",
#                                         "items": { "type": "string" }
#                                     }
#                                 },
#                                 "required": ["Description", "Timestamp"]
#                             }
#                         },
#                         "required": ["Player1", "Player2"]
#                     },
#                     "Footwork": {
#                         "type": "object",
#                         "properties": {
#                             "Player1": {
#                                 "type": "object",
#                                 "properties": {
#                                     "Description": {
#                                         "type": "array",
#                                         "items": { "type": "string" }
#                                     },
#                                     "Timestamp": {
#                                         "type": "array",
#                                         "items": { "type": "string" }
#                                     }
#                                 },
#                                 "required": ["Description", "Timestamp"]
#                             },
#                             "Player2": {
#                                 "type": "object",
#                                 "properties": {
#                                     "Description": {
#                                         "type": "array",
#                                         "items": { "type": "string" }
#                                     },
#                                     "Timestamp": {
#                                         "type": "array",
#                                         "items": { "type": "string" }
#                                     }
#                                 },
#                                 "required": ["Description", "Timestamp"]
#                             }
#                         },
#                         "required": ["Player1", "Player2"]
#                     },
#                     "Stamina": {
#                         "type": "object",
#                         "properties": {
#                             "Player1": {
#                                 "type": "object",
#                                 "properties": {
#                                     "Description": { "type": "string" },
#                                     "percentage": { "type": "integer" }
#                                 },
#                                 "required": ["Description", "percentage"]
#                             },
#                             "Player2": {
#                                 "type": "object",
#                                 "properties": {
#                                     "Description": { "type": "string" },
#                                     "percentage": { "type": "integer" }
#                                 },
#                                 "required": ["Description", "percentage"]
#                             }
#                         },
#                         "required": ["Player1", "Player2"]
#                     },
#                     "Fouls": {
#                         "type": "object",
#                         "properties": {
#                             "Player1": {
#                                 "type": "object",
#                                 "properties": {
#                                     "Description": {
#                                         "type": "array",
#                                         "items": { "type": "string" }
#                                     },
#                                     "Timestamp": {
#                                         "type": "array",
#                                         "items": { "type": "string" }
#                                     }
#                                 },
#                                 "required": ["Description", "Timestamp"]
#                             },
#                             "Player2": {
#                                 "type": "object",
#                                 "properties": {
                                
#                                     "Description": {
#                                         "type": "array",
#                                         "items": { "type": "string" }
#                                     },
#                                     "Timestamp": {
#                                         "type": "array",
#                                         "items": { "type": "string" }
#                                     }
#                                 },
#                                 "required": ["Description", "Timestamp"]
#                             }
#                         },
#                         "required": ["Player1", "Player2"]
#                     },
#                     "Smashes": {
#                         "type": "object",
#                         "properties": {
#                             "Player1": {
#                                 "type": "object",
#                                 "properties": {
#                                     "count": { "type": "integer" },
#                                     "Timestamp": {
#                                         "type": "array",
#                                         "items": { "type": "string" }
#                                     }
#                                 },
#                                 "required": ["count", "Timestamp"]
#                             },
#                             "Player2": {
#                                 "type": "object",
#                                 "properties": {
#                                     "count": { "type": "integer" },
#                                     "Timestamp": {
#                                         "type": "array",
#                                         "items": { "type": "string" }
#                                     }
#                                 },
#                                 "required": ["count", "Timestamp"]
#                             }
#                         },
#                         "required": ["Player1", "Player2"]
#                     }
#                 },
#                 "required": ["Player1", "Player2", "Point_winner", "rally_shots_count", "Court Reach", "Footwork", "Stamina", "Fouls", "Smashes"]
#             }
#         }
#     },
#     "response_mime_type": "application/json",
# }


# print("Configured Json for output")

# print("Configuring Model for Prompt")


# model = genai.GenerativeModel(
#   model_name="gemini-1.5-pro",
#   generation_config=generation_config,
#    system_instruction=(
#         "As a Badminton Rally Analysis Expert, your task is to analyze each rally video individually, "
#         "evaluating both players' court reach, footwork, stamina, fouls, and smashes. For each rally:\n"
#         "1. Identify the player who won the point.\n"
#         "2. Count the total shots in the rally.\n"
#         "3. Assess Court Reach for each player, noting movement across the court and providing descriptive analysis with precise timestamps.\n"
#         "4. Analyze Footwork for each player, including descriptions and timestamps for specific movements.\n"
#         "5. Evaluate Stamina, describing each player’s energy levels and endurance, with a stamina percentage.\n"
#         "6. Track any Fouls, listing the type of foul, descriptions, and timestamps.\n"
#         "7. Count and timestamp all Smashes for each player.\n"
#         "Generate output in JSON format, using the provided schema for a single rally. Ensure accuracy in timestamps and provide a structured breakdown of the rally dynamics and notable moments for both players."
#     ))

# print("Configured Model for Prompt")



# # TODO Make these files available on the local file system
# print("Video File Uploading")

# # You may need to update the file paths
# files = [
#   upload_to_gemini("/home/auriga/Downloads/videoplayback.mp4", mime_type="video/mp4"),
# ]

# # Some files have a processing delay. Wait for them to be ready.
# wait_for_files_active(files)

# chat_session = model.start_chat(
#   history=[
#     {
#       "role": "user",
#       "parts": [
#         files[0],
#       ],
#     }
#   ]
# )

# response = chat_session.send_message("Analyze the provided badminton rally video and output detailed observations. "
#                        "A new rally starts each time a player scores a point. Include analysis of each player's court reach, "
#                        "footwork, stamina, fouls, smashes, and provide timestamps. Count the shots in this rally only, "
#                        "and identify the point winner. Use the provided JSON schema.")

# print(response.text)

# # Count tokens in the text prompt
# text_token_count = model.count_tokens("Analyze the provided badminton video and output detailed observations and description for each rally. A new rally starts each time a player scores a point. Include analysis of each player's court reach, footwork, stamina, fouls, smashes, and provide timestamps. Count the shots per rally and dynamically count all rallies within the match. Use the provided JSON schema.")
# print(f"Text prompt tokens: {text_token_count}")


# if hasattr(response, 'usage_metadata'):
#     print(f"""
#     Token Usage:
#     - Prompt tokens: {response.usage_metadata.prompt_token_count}
#     - Response tokens: {response.usage_metadata.candidates_token_count}
#     - Total tokens: {response.usage_metadata.total_token_count}
#     """)