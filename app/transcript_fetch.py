import re
import logging

from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
)

logger = logging.getLogger(__name__)


def extract_video_id(url_or_id: str) -> str:
    """
    YouTube URL ya direct video ID se video ID extract karta hai.
    """

    if not url_or_id:
        raise ValueError("YouTube URL or Video ID is required.")

    url_or_id = url_or_id.strip()

    # Direct YouTube video ID
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url_or_id):
        return url_or_id

    patterns = [
        r"(?:v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/shorts/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/embed/)([A-Za-z0-9_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)

    raise ValueError("Invalid YouTube URL or Video ID.")


def get_english_transcript(url_or_id: str) -> str:
    """
    YouTube video ka English transcript return karta hai.

    Priority:
    1. Manually created English transcript
    2. Generated English transcript
    3. Available transcript + YouTube translation to English
    """

    video_id = extract_video_id(url_or_id)

    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        try:
            transcript = transcript_list.find_manually_created_transcript(["en"])
            logger.info("Using manually created English transcript.")

        except NoTranscriptFound:
            try:
                transcript = transcript_list.find_generated_transcript(["en"])
                logger.info("Using auto-generated English transcript.")

            except NoTranscriptFound:
                transcript = next(iter(transcript_list))
                logger.info(
                    "No English transcript found. Translating from '%s'.",
                    transcript.language_code,
                )

                if transcript.language_code != "en":
                    transcript = transcript.translate("en")

        fetched_transcript = transcript.fetch()

        text = " ".join(item.text for item in fetched_transcript).strip()

        if not text:
            raise ValueError("The transcript was found but contains no text.")

        return text

    except TranscriptsDisabled:
        raise ValueError("Captions are disabled for this YouTube video.")

    except NoTranscriptFound:
        raise ValueError("No transcript was found for this YouTube video.")

    except StopIteration:
        raise ValueError("No transcript is available for this YouTube video.")