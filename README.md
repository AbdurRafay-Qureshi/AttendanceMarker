<h2 align="center">AUTOMATED ATTENDING SYSTEM</h2>

<p>The <b><i>Automated Attending Bot</i></b> is a local Python Web Application designed to attend your online meetings and classes <i>for you</i>.</p>
 
Simply provide the link to your Google Meet or Microsoft Teams session, and the bot will launch a stealth-mode browser using your actual Google/Microsoft profile to bypass authentication and bot-detection checks. 

Once inside the meeting, it uses real-time Web Speech API transcription and native caption gathering to monitor the conversation. If your custom enrollment keywords (like your Name or Roll Number) are called out during attendance, the bot automatically injects a pre-recorded audio file of you saying "Present!" directly into the meeting's WebRTC microphone stream.

---

### What Changed? (v2.0 Overhaul)
The application has been completely rebuilt from the ground up:
* **Before:** Relied on fragile, hard-coded `PyAutoGUI` screen coordinates and computationally heavy `PyTesseract` Image Processing. It constantly broke depending on your monitor resolution and could not handle dynamic UI updates.
* **After:** Rebuilt as a robust **Flask + Selenium Web Application** running natively on `localhost:5001`. The bot now hooks directly into the browser DOM using CSS/XPath selectors and executes native JavaScript to handle meeting interactions.
* **New Platform:** Officially added **Microsoft Teams** support alongside Google Meet.
* **Microphone Bypass:** Uses `--use-fake-ui-for-media-stream` and pure Javascript WebRTC interceptors to natively pipe your pre-recorded `.wav` files into the digital microphone channel without relying on your physical speaker/microphone hardware loop!

---

### 🚀 How to Use (Installation Guide)

#### 1. Setup Environment
Ensure you have **Python 3.10+** and either Google Chrome or Microsoft Edge installed.

```bash
# Install dependencies
pip install -r requirements.txt

# Start the application
python app.py
```
*(Alternatively, simply run `start.bat` on Windows)*

Navigate to `http://localhost:5001` in your browser to access the Dashboard!

#### 2. Configure Your Profile
1. **Audio Setup:** Go to the `Settings` tab. Record your voice saying "Present" directly into the browser and enter the trigger words (e.g., your first name, last name, and roll number) you want the bot to listen for.
2. **Browser Binding:** Go to the `Browser Profile` tab. Enter the absolute path to your active Edge or Chrome User Data folder (e.g. `C:\Users\YourName\AppData\Local\Microsoft\Edge\User Data`). The bot uses this to securely inherit your login cookies so you don't have to sign in every time!

#### 3. Join a Meeting
Paste a valid meeting link into the Dashboard and hit **Start Meeting**. The bot will automatically mute the microphone and camera on the pre-join lobby before navigating you inside.

> [!WARNING]
> **CRITICAL: Browser Closures & File Locks**  
> To prevent anti-bot detection walls, this bot uses your *actual* everyday browser profile rather than a disposable proxy. Because Windows strictly restricts file locks (`WinError 32`), the bot **must** temporarily terminate your actively open Edge/Chrome windows the moment you click "Start Meeting" so it can successfully claim the profile.  
> **Always start the meeting bot first** before doing your daily browsing! The bot will graciously restore your Dashboard on a background tab once it launches its own stealth window.

---

### ⚠️ Known Issues
* **Dynamic Selectors:** Because the bot uses CSS selectors to find the "Join Now" and "Mute Microphone" buttons, future UI updates pushed by Google or Microsoft could cause the bot to break. If this happens, developers must manually update the HTML selectors inside `services/teams_selectors.py` and `services/meeting_bot.py`.
* **Teams Captions:** Microsoft Teams does not supply raw audio data to the browser securely. The bot strictly monitors the live Closed Captions for your name. If the meeting host disables captions, the bot will fall back to local Speech Recognition.

---

###  Libraries Used:
1. **Flask:** Local Web Server and Dashboard routing.
2. **Selenium:** Headful browser automation and dynamic DOM interaction.
3. **Pydub:** Local audio file format conversion and normalization.
4. **SQLAlchemy:** Local SQLite database management for settings and session logs.

---

### PLEASE NOTE:
<p>For legal reasons,<br>
This bot was purely made for <b><i>educational</i></b> purposes only and is meant as a fun way to learn and implement the libraries/packages mentioned above. <br>
This bot is not meant to be used in any malicious way and we are not responsible for anyone actually using this bot to wrongfully attend online classes on his/her/their behalf.</p>
