# Mitra Theatre 🎭

**A professional dual-deck media controller designed for seamless presentations and live events.**

Mitra Theatre is a lightweight, cross-platform media playback tool built with Python and PySide6. It is designed specifically for event operators, presentation managers, and theatre technicians who need precise, independent control over visual and audio assets without the complexity of heavy broadcasting software.

---

## ✨ Key Features

* **Dual-Deck Architecture:** 
  * **Deck A (Video/Visuals):** Full video playback control with a built-in live preview monitor. 
  * **Deck B (Background Audio):** Independent audio playback for background music, walk-in tracks, or sound effects.
* **Smart Playlist Management:** Add all your media to a single master playlist. Double-clicking a video file automatically routes it to Deck A, while audio-only files (MP3, WAV, etc.) intelligently route to Deck B.
* **Live Output Blanking (LIVE/BLACK):** Instantly cut the projector feed to black with a single toggle switch, allowing you to queue up and preview the next video privately before pushing it live to the audience.
* **Auto-Screen Routing:** The application automatically detects multiple monitors. The control deck opens on your primary screen, while the projector output window automatically maximizes in fullscreen on your secondary display.
* **Cross-Platform:** Native builds available for Windows, macOS, and Linux.

---

## 📥 Installation & Downloads

You do not need to install Python to run Mitra Theatre. Pre-compiled, ready-to-use binaries are available for all major operating systems.

Go to the [Releases](../../releases/latest) page to download the latest version (v1.2):
* **Windows:** Download the `.exe` installer.
* **macOS:** Download the `.dmg` file.
* **Linux:** Download the `.AppImage` (or `.deb` / Flatpak if available).

---

## 🚀 Usage Guide

1. **Connect your external display** (projector, LED wall, or TV) to your computer *before* launching the application.
2. Launch **Mitra Theatre**. The control interface will appear on your main screen, and a black window will fill the projector screen.
3. Click **+ Add Files to Library** to populate your Master Playlist.
4. **Select Output Device:** Use the dropdown at the top to select which sound card or interface audio should route to.
5. **Load Media:**
   * Double-click a video file to load it into **Deck A**.
   * Double-click an audio file to load it into **Deck B**.
6. **Go Live:** Click **Play** on Deck A. If the output toggle is set to **LIVE**, the audience will see the video. If set to **BLACK**, you will only see it on your local preview monitor until you toggle it.

---

## 🛠️ Building from Source

Automated Builds: This repository is configured with GitHub Actions. Pushing a new tag or code to the main branch will automatically compile and publish the latest Windows, macOS, and Linux binaries to the Releases page.
If you want to build the application from the source code, you will need Python 3.10+ installed.

**1. Clone the repository:**
```bash
git clone [https://github.com/yourusername/mitratheatre.git](https://github.com/yourusername/mitratheatre.git)
cd mitratheatre
