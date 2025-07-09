
Layout
-
Phase 1: Setup the brain of the bot (Multimodal LLM)
* Setup Groq API key 
* Convert image to required format 
* Setup multimodal LLM 

Phase 2: Setup voice of the patient 
* Setup Audio recorder (ffmpeg & portaudio)
* Setup Speech-to-text (STT) model for transcription

Phase 3: Setup voice of the bot
* Setup TTS model (gTTS & ElevenLabs)
* Use model for text output to voice

Phase 4: Setup UI for the VoiceBot
* VoiceBot UI with Gradio

Tools and Technologies
- 
* Groq for AI Inference
* OpenAI Whisper (One of the best open source models for transcription)
* Llama 3 Vision (Open source by Meta)
* gTTS & ElevenLabs (Text to Speech)
* Gradio for UI 
* Python
* VS Code
* Docker

Notes
-
* base64: Python library which uses base64 encoding. Converts data in bits/bytes to string. Neccessary for encoding/decoding of data when transferring in between systems to prevent corruption.
* ffmpeg: System-wide library. free and open-source software suite used for handling multimedia files like videos and audio.
* PyAudio: PyAudio provides Python bindings for PortAudio v19, the cross-platform audio I/O library. With PyAudio, you can easily use Python to play and record audio on a variety of platforms.

Docker
-
Docker is a tool that packages applications. It's like a universal shipping box for software.
* Consists of portable, self-contained "containers".
* Containers bundle everything an app needs to run(code, libraries, settings) so it works identically on any machine.

Any code which runs locally but does not work during production is useless as it is close to impossible to find errors during debugging

Why Docker? - It is lightwight, works in isolation, is fast, and works everywhere.