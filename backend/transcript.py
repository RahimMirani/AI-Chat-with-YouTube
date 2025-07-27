from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

def get_transcript(video_id: str):
   
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([item['text'] for item in transcript_list])
        return transcript_text
    except NoTranscriptFound:
        return None
    except Exception as e:
        return None 