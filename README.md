# LyricHub

A centralized API hub for retrieving lyrics from multiple music platforms.

## Supported Platforms

- Genius: Standard formatted lyrics (using official Genius API)
- Spotify: Time-synchronized lyrics
- More platforms coming soon

## Features

- Search for songs by artist and title
- Retrieve lyrics from different music platforms
- Clean JSON responses with song metadata
- Platform-specific API endpoints

## Getting Started

### Prerequisites

- Python 3.9+
- Genius API client (for Genius authentication)
- Spotify account (for Spotify authentication)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/imjyotiraditya/lyrichub.git
   cd lyrichub
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your environment:
   ```bash
   cp .env.example .env
   ```

5. Edit `.env` and add your credentials:
   ```
   SPOTIFY_DC=your_spotify_dc_cookie_value
   GENIUS_ACCESS_TOKEN=your_genius_access_token
   ```

   To get your Genius access token:
   - Create an API client at [Genius API Clients](https://genius.com/api-clients)
   - Generate an access token in your client settings
   - Copy the access token

   To get your `sp_dc` cookie:
   - Log in to [Spotify Web Player](https://open.spotify.com)
   - Open browser developer tools (F12)
   - Go to Application/Storage > Cookies > https://open.spotify.com
   - Find the `sp_dc` cookie and copy its value

### Running the API

Start the development server:

```bash
uvicorn api.main:app --reload
```

The API will be available at http://localhost:8000

## API Usage

### Endpoints

- `GET /api/genius?query=your+search+query` - Get lyrics from Genius
- `GET /api/spotify?query=your+search+query` - Get lyrics from Spotify
- Additional platforms may be added in future versions

### Example Request

```bash
curl "http://localhost:8000/api/genius?query=swim+chase+atlantic"
```

### Response Format

All endpoints return the same JSON structure:

```json
{
  "title": "Song Title",
  "artist": "Artist Name",
  "cover": "https://cover-image-url.jpg",
  "lyrics": "Lyrics content..."
}
```

Note: Different platforms provide lyrics in different formats:
- Genius: Standard text lyrics with formatting
- Spotify: Time-synchronized lyrics with timestamps (e.g., `[00:12.79]Lyrics line`)

## Deployment

This project includes configuration for deployment on Vercel:

```bash
vercel
```

For Vercel deployment, make sure to set the environment variables:
- `GENIUS_ACCESS_TOKEN`
- `SPOTIFY_DC`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This project is for educational purposes only. Use of the music platforms' APIs (listed under Supported Platforms) may be subject to their respective terms of service.
