# Copyright MediaControlEnv

import json
from typing import Any, Dict, List, Optional
from MediaControlEnv.tool import Tool


class SearchByArtist(Tool):
    """
    Tool for searching media content by artist name.
    Supports searching for songs and albums by a specific artist.
    """
    
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        artist: str,
        media_type: Optional[str] = None,
        limit: int = 50
    ) -> str:
        """
        Search for media content by artist name.
        
        Args:
            data: The data dictionary containing media information
            artist: Artist name to search for (partial matching supported)
            media_type: Optional filter for media type ('song' or 'album')
            limit: Maximum number of results to return (default: 10)
            
        Returns:
            String containing search results or error message
        """
        try:
            # Get media database
            media_db = data.get("media_database", {})
            if not media_db:
                return "Error: Media database not available"
            
            music_data = media_db.get("music", [])
            if not music_data:
                return "Error: No music data available"
            
            # Search for media by artist
            results = SearchByArtist._find_media_by_artist(music_data, artist, media_type, limit)
            
            if not results:
                return f"No media found for artist '{artist}'"
            
            # Format results
            return SearchByArtist._format_search_results(results, artist)
            
        except Exception as e:
            return f"Error searching by artist: {str(e)}"
    
    @staticmethod
    def _find_media_by_artist(
        music_data: List[Dict[str, Any]], 
        artist: str, 
        media_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Find media items by artist name with optional type filtering.
        
        Args:
            music_data: List of music items from the database
            artist: Artist name to search for
            media_type: Optional filter ('song' or 'album')
            limit: Maximum number of results
            
        Returns:
            List of matching media items
        """
        results = []
        artist_lower = artist.lower()
        
        for item in music_data:
            # Check if artist matches (partial match, case insensitive)
            item_artist = item.get("artist", "").lower()
            if artist_lower in item_artist:
                # Apply media type filter if specified
                if media_type:
                    item_type = item.get("type", "")
                    if item_type != media_type:
                        continue
                
                results.append(item)
                
                # Check limit
                if len(results) >= limit:
                    break
        
        return results
    
    @staticmethod
    def _format_search_results(results: List[Dict[str, Any]], artist: str) -> str:
        """
        Format search results into a readable string.
        
        Args:
            results: List of media items
            artist: The searched artist name
            
        Returns:
            Formatted results string
        """
        output = [f"Found {len(results)} media items for artist '{artist}':\n"]
        
        for i, item in enumerate(results, 1):
            title = item.get("title", "Unknown Title")
            item_type = item.get("type", "unknown")
            artist_name = item.get("artist", "Unknown Artist")
            year = item.get("year", "Unknown")
            duration = item.get("duration", 0)
            item_id = item.get("id", "unknown")
            
            # Format duration
            duration_str = SearchByArtist._format_duration(duration)
            
            # Format genre if available
            genre = item.get("genre", [])
            genre_str = ", ".join(genre) if genre else "Unknown"
            
            output.append(
                f"{i}. [{item_type.upper()}] {title}\n"
                f"   Artist: {artist_name}\n"
                f"   Year: {year} | Duration: {duration_str} | Genre: {genre_str}\n"
                f"   ID: {item_id}\n"
            )
        
        return "".join(output)
    
    @staticmethod
    def _format_duration(seconds: int) -> str:
        """
        Format duration in seconds to readable format.
        
        Args:
            seconds: Duration in seconds
            
        Returns:
            Formatted duration string
        """
        if seconds <= 0:
            return "Unknown"
        
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        
        if minutes >= 60:
            hours = minutes // 60
            remaining_minutes = minutes % 60
            return f"{hours}:{remaining_minutes:02d}:{remaining_seconds:02d}"
        else:
            return f"{minutes}:{remaining_seconds:02d}"
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Get tool information for the function calling interface.
        
        Returns:
            Tool information dictionary with detailed parameter specifications and error cases
        """
        return {
            "type": "function",
            "function": {
                "name": "search_by_artist",
                "description": "Search for media content (songs and albums) by artist name. Supports optional filtering by media type. Returns detailed information including title, artist, year, genre, duration, and media ID for each result.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "artist": {
                            "type": "string",
                            "description": "Artist name to search for. Supports partial matching (case-insensitive). Examples: 'Rihanna', 'Beatles', 'Bob' (matches 'Bob Dylan'), 'JOHNNY' (matches 'Johnny Cash')"
                        },
                        "media_type": {
                            "type": "string",
                            "description": "Optional filter to restrict results to a specific media type. Use 'song' for individual tracks or 'album' for full albums. If not specified, returns both songs and albums matching the artist"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results to return. Default is 50. Use smaller values (1-5) for quick searches, or larger values (20-50) for comprehensive results. Results are returned in database order"
                        }
                    },
                    "required": ["artist"],
                    "additionalProperties": False
                },
                "returns": {
                    "type": "string",
                    "description": "Formatted string containing search results with detailed information for each media item, including: item number, media type (SONG/ALBUM), title, artist name, release year, duration (formatted as MM:SS or H:MM:SS), genre(s), and unique media ID. Returns error message if no results found or if database issues occur."
                },
                "error_cases": [
                    "Empty artist name: The artist parameter is empty or not provided.",
                    "Media database unavailable: The media database is not loaded or accessible.",
                    "No music data: The music section of the media database is empty or missing.",
                    "Invalid media type: The media_type parameter contains a value other than 'song' or 'album'.",
                    "Invalid limit: The limit parameter is less than 1 or greater than 50."
                ]
            }
        }
