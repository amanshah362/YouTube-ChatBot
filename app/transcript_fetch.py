import os
import re
import logging

from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
)
from youtube_transcript_api.proxies import WebshareProxyConfig, GenericProxyConfig

logger = logging.getLogger(__name__)


def _build_api() -> YouTubeTranscriptApi:
    """
    Cloud provider IPs (AWS, GCP, Azure, etc.) are frequently blocked by
    YouTube. Priority order for routing around this:
      1. Webshare Rotating Residential proxy (paid, most reliable) if
         WEBSHARE_PROXY_USERNAME/PASSWORD are set.
      2. Tor SOCKS5 proxy (free, less reliable) if USE_TOR=true.
      3. Direct connection (fine only on a residential/non-cloud IP).
    """
    proxy_username = os.getenv("WEBSHARE_PROXY_USERNAME")
    proxy_password = os.getenv("WEBSHARE_PROXY_PASSWORD")

    if proxy_username and proxy_password:
        logger.info("Using Webshare proxy for YouTube transcript requests.")
        return YouTubeTranscriptApi(
            proxy_config=WebshareProxyConfig(
                proxy_username=proxy_username,
                proxy_password=proxy_password,
            )
        )

    if os.getenv("USE_TOR", "false").lower() == "true":
        logger.info("Using local Tor SOCKS5 proxy for YouTube transcript requests.")
        return YouTubeTranscriptApi(
            proxy_config=GenericProxyConfig(
                http_url="socks5h://127.0.0.1:9050",
                https_url="socks5h://127.0.0.1:9050",
            )
        )

    logger.warning(
        "No proxy configured (WEBSHARE_PROXY_USERNAME/PASSWORD or USE_TOR not set). "
        "Requests from cloud IPs (AWS/GCP/Azure) may be blocked by YouTube."
    )
    return YouTubeTranscriptApi()


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
        api = _build_api()
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