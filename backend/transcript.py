from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

def get_transcript(video_id: str):
    try:
        transcript_initialize = YouTubeTranscriptApi()
        transcript_list = transcript_initialize.list(video_id)
        transcript = transcript_list.find_transcript(['en', 'en-US'])
        transcript_data_raw = transcript.fetch()
        transcript_filtered = " ".join([item.text for item in transcript_data_raw])
        return transcript_filtered
    
    except (NoTranscriptFound, TranscriptsDisabled):
        return ("No transcript found")
    
    except Exception as e:
        return (f"Error: {e}")


Video = get_transcript("ydTdJDJMiKE")
print(Video)