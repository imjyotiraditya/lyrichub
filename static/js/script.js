import API from "./api.js";
import UI from "./ui.js";

async function searchLyrics() {
  const query = UI.elements.searchInput.value.trim();
  if (!query) {
    UI.showStatus(
      UI.elements.searchStatus,
      "Please enter a song or artist name",
      "error"
    );
    return;
  }

  try {
    UI.showResults(false);
    UI.showError(false);
    UI.showLoading(true);
    UI.elements.searchBtn.disabled = true;

    const platform = document.querySelector(".platform-btn.active").dataset
      .platform;

    const result = await API.getLyrics(query, platform);

    if (result.error) {
      throw new Error(result.error);
    }

    UI.updateLyricsInfo(result, platform);

    UI.showLoading(false);
    UI.showResults(true);
  } catch (error) {
    console.error("Error:", error);
    UI.showLoading(false);
    UI.showError(true, error.message);
  } finally {
    UI.elements.searchBtn.disabled = false;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  UI.init(searchLyrics);
});

export { searchLyrics };
