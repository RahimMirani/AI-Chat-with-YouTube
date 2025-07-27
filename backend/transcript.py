from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound


def get_transcript(video_id: str):
   
    try:
        transcript_initialize = YouTubeTranscriptApi()
        transcript_list = transcript_initialize.fetch(video_id)
        #transcript_text = " ".join([item['text'] for item in transcript_list])
        return transcript_list
    
    except NoTranscriptFound:
        print("No transcript found")
        return None
    
    except Exception as e:
        print(f"Error: {e}")
        return None 
    

Video = get_transcript("ydTdJDJMiKE")
print(Video)