"""
🔴 TDD Step 1: Write a FAILING test first!

This is our first test. We're testing the YouTubeClient class
that doesn't exist yet. That's the point of TDD!

The test describes WHAT we want the code to do.
Then we write code to make it pass.
"""

import pytest


class TestYouTubeClient:
    """Tests for the YouTube API client."""

    def test_client_can_be_instantiated_with_api_key(self):
        """
        🎯 Test: We should be able to create a YouTubeClient with an API key.

        Why this test first?
        - It's the simplest possible test
        - It forces us to create the class
        - It defines the basic interface
        """
        # Arrange: We'll import our client (doesn't exist yet!)
        from ingestion.youtube_client import YouTubeClient

        # Act: Create a client with an API key
        client = YouTubeClient(api_key="test_api_key")

        # Assert: The client should store the API key
        assert client.api_key == "test_api_key"

    def test_get_channel_videos_returns_list_of_video_metadata(self):
        """
        🎯 Test: get_channel_videos should return a list of video info.

        But wait — we don't want to hit the real YouTube API in tests!
        So we'll MOCK it. This is how production code tests external APIs.
        """
        from ingestion.youtube_client import YouTubeClient
        from unittest.mock import Mock, patch

        client = YouTubeClient(api_key="test_key")

        # We expect a method called get_channel_videos
        # that takes a channel_id and returns a list
        # For now, just test the method EXISTS and returns a list
        result = client.get_channel_videos(channel_id="test_channel")

        assert isinstance(result, list)

    def test_get_channel_videos_calls_youtube_api(self, mocker):
        """🎯 Test: Verify that get_channel_videos actually calls the YouTube API.
        We'll use pytest-mock to replace the real API with a fake one."""

        from ingestion.youtube_client import YouTubeClient

        # ARRANGE: Create a mock YouTube API response
        mock_youtube_build = mocker.patch("ingestion.youtube_client.build")
        mock_service = mock_youtube_build.return_value

        # Tell the mock what to return when called
        mock_service.channels().list().execute.return_value = {
            "items": [{"contentDetails": {"relatedPlaylists": {"uploads": "UUxxx"}}}]
        }

        # ACT: Call our method
        client = YouTubeClient(api_key="test_key")
        result = client.get_channel_videos(channel_id="UCtest123")

        # ASSERT: The YouTube API was called with correct parameters
        mock_youtube_build.assert_called_once_with(
            "youtube", "v3", developerKey="test_key"
        )
