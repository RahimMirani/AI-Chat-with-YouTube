from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

#print(dir(YouTubeTranscriptApi))


video_id = "suakoHWghfg"
Video1 = YouTubeTranscriptApi.get_transcript(video_id)

print(Video1)


"""
def get_transcript(video_id: str):
   
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([item['text'] for item in transcript_list])
        return transcript_text
    
    except NoTranscriptFound:
        print("No transcript found")
        return None
    
    except Exception as e:
        print(f"Error: {e}")
        return None 
    

video1 = get_transcript("ydTdJDJMiKE")
print(video1)

"""