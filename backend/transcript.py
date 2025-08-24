from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled


def get_transcript(video_id: str):
    try:
        ytt_api = YouTubeTranscriptApi()
        fetched = ytt_api.fetch(video_id, languages=['en', 'en-US'])
        return fetched.to_raw_data()
    except NoTranscriptFound:
        try:
            ytt_api = YouTubeTranscriptApi()
            fetched = ytt_api.fetch(video_id, languages=['en'])
            return fetched.to_raw_data()
        except (NoTranscriptFound, TranscriptsDisabled) as e:
            print(f"Transcript not available for {video_id}: {e}")
            return None
        except Exception as e:
            print(f"Error on fallback fetch for {video_id}: {e}")
            return None
    except TranscriptsDisabled as e:
        print(f"Transcripts disabled for {video_id}: {e}")
        return None
    except Exception as e:
        print(f"Error fetching transcript for {video_id}: {e}")
        return None
