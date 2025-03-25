import API from "./api.js";

const UI = {
  elements: {
    searchInput: document.getElementById("search-input"),
    searchBtn: document.getElementById("search-btn"),
    platformButtons: document.querySelectorAll(".platform-btn"),
    searchStatus: document.getElementById("search-status"),
    resultsContainer: document.getElementById("results-container"),
    loadingIndicator: document.getElementById("loading-indicator"),
    errorContainer: document.getElementById("error-container"),
    errorMessage: document.getElementById("error-message"),
    songTitle: document.getElementById("song-title"),
    songArtist: document.getElementById("song-artist"),
    songCover: document.getElementById("song-cover"),
    coverPlaceholder: document.querySelector(".cover-placeholder"),
    platformBadge: document.getElementById("platform-badge"),
    lyricsContent: document.getElementById("lyrics-content"),
  },

  init(searchCallback) {
    this.elements.searchBtn.addEventListener("click", searchCallback);

    this.elements.searchInput.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        searchCallback();
      }
    });

    this.elements.platformButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        this.elements.platformButtons.forEach((b) =>
          b.classList.remove("active")
        );
        btn.classList.add("active");
        this.updatePlatformBadge(btn.dataset.platform);
      });
    });
  },

  updatePlatformBadge(platform) {
    const badge = this.elements.platformBadge;

    if (platform === "spotify") {
      badge.innerHTML = '<i class="fa-brands fa-spotify"></i> Spotify';
    } else if (platform === "genius") {
      badge.innerHTML = '<i class="fa-solid fa-music"></i> Genius';
    }
  },

  showStatus(element, message, type) {
    if (!element) return;
    element.textContent = message;
    element.className = `status ${type}`;
    setTimeout(() => {
      element.className = "status";
    }, 3000);
  },

  showLoading(show) {
    this.elements.loadingIndicator.classList.toggle("hidden", !show);
  },

  showError(show, message = "Error retrieving lyrics.") {
    this.elements.errorContainer.classList.toggle("hidden", !show);
    this.elements.errorMessage.textContent = message;
  },

  showResults(show) {
    this.elements.resultsContainer.classList.toggle("hidden", !show);
  },

  showToast(message) {
    const existingToast = document.querySelector(".toast");
    if (existingToast) {
      existingToast.remove();
    }

    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
      toast.classList.add("show");
    }, 10);

    setTimeout(() => {
      toast.classList.remove("show");
      setTimeout(() => {
        toast.remove();
      }, 300);
    }, 3000);
  },

  renderSyncedLyrics(lyricsData) {
    const container = this.elements.lyricsContent;
    container.innerHTML = "";

    if (!lyricsData.isSynced) {
      container.textContent = lyricsData.text;
      return;
    }

    lyricsData.lines.forEach((line) => {
      const lineElement = document.createElement("div");
      lineElement.className = "time-synced-line";

      const timestamp = document.createElement("span");
      timestamp.className = "timestamp";
      timestamp.textContent = line.time;

      lineElement.appendChild(timestamp);
      lineElement.appendChild(document.createTextNode(line.text));

      container.appendChild(lineElement);
    });
  },

  updateLyricsInfo(data, platform) {
    this.elements.songTitle.textContent = data.title || "Unknown Title";
    this.elements.songArtist.textContent = data.artist || "Unknown Artist";

    this.updatePlatformBadge(platform);

    if (data.cover) {
      this.elements.songCover.src = data.cover;
      this.elements.songCover.classList.remove("hidden");
      this.elements.coverPlaceholder.classList.add("hidden");
    } else {
      this.elements.songCover.classList.add("hidden");
      this.elements.coverPlaceholder.classList.remove("hidden");
    }

    if (platform === "spotify") {
      const formattedLyrics = API.formatSpotifyLyrics(data.lyrics);
      this.renderSyncedLyrics(formattedLyrics);
    } else {
      this.elements.lyricsContent.textContent =
        data.lyrics || "No lyrics found.";
    }
  },
};

export default UI;
