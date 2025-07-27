from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

def get_transcript(video_id: str):
    try:
        transcript_initialize = YouTubeTranscriptApi()
        transcript_list = transcript_initialize.list(video_id)
        transcript = transcript_list.find_transcript(['en', 'en-US'])
        transcript_data = transcript.fetch()
        return " ".join([item.text for item in transcript_data])
    
    except (NoTranscriptFound, TranscriptsDisabled):
        print("No transcript found")
        return None
    
    except Exception as e:
        print(f"Error: {e}")
        return None


Video = get_transcript("ydTdJDJMiKE")
print(Video)