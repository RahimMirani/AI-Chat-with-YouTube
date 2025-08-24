from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled


def get_transcript(video_id: str):
    try:
        # Prefer manual or auto-generated English transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = None
        try:
            transcript = transcript_list.find_transcript(['en', 'en-US'])
        except NoTranscriptFound:
            try:
                transcript = transcript_list.find_generated_transcript(['en', 'en-US'])
            except NoTranscriptFound:
                transcript = None

        if transcript is not None:
            return transcript.fetch()

        # Fallback: translate first available transcript to English
        for t in transcript_list:
            try:
                return t.translate('en').fetch()
            except Exception:
                continue

        return None

    except (NoTranscriptFound, TranscriptsDisabled) as e:
        print(f"Transcript not available for {video_id}: {e}")
        return None
    except Exception as e:
        print(f"Error fetching transcript for {video_id}: {e}")
        return None
