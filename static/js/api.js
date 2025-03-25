const API = {
  BASE_URL: "/api",

  async getLyrics(query, platform) {
    try {
      const encodedQuery = encodeURIComponent(query);

      const response = await fetch(
        `${this.BASE_URL}/${platform}?query=${encodedQuery}`
      );

      if (!response.ok) {
        try {
          const errorData = await response.json();
          throw new Error(
            errorData.error || `Failed to fetch lyrics (${response.status})`
          );
        } catch (e) {
          throw new Error(`Failed to fetch lyrics (${response.status})`);
        }
      }

      return await response.json();
    } catch (error) {
      console.error("API Error:", error);
      return { error: error.message || "An unexpected error occurred" };
    }
  },

  formatSpotifyLyrics(lyrics) {
    if (!lyrics || lyrics === "Not Found.") {
      return {
        isSynced: false,
        text: "No lyrics found for this track.",
      };
    }

    const hasTimestamps =
      lyrics.includes("[") && /\[\d{2}:\d{2}\.\d{2}\]/.test(lyrics);

    if (!hasTimestamps) {
      return {
        isSynced: false,
        text: lyrics,
      };
    }

    const lines = lyrics.split("\n");
    const formattedLines = [];

    for (const line of lines) {
      const timestampMatch = line.match(/\[(\d{2}):(\d{2}\.\d{2})\](.*)/);

      if (timestampMatch) {
        const minutes = timestampMatch[1];
        const seconds = timestampMatch[2];
        const text = timestampMatch[3].trim();

        if (text) {
          formattedLines.push({
            time: `${minutes}:${seconds}`,
            timeMs: (parseInt(minutes) * 60 + parseFloat(seconds)) * 1000,
            text: text,
          });
        }
      }
    }

    return {
      isSynced: true,
      lines: formattedLines,
      text: formattedLines.map((line) => line.text).join("\n"),
    };
  },
};

export default API;
