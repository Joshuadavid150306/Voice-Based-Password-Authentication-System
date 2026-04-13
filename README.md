# Voice-Based-Password-Authentication-System

A Voice-Based Password Authentication System that allows users to register their voice as a password and also create a backup password for extra security.

## Project Overview

This project uses voice recognition and MFCC (Mel Frequency Cepstral Coefficients) feature extraction to identify whether the spoken voice matches the registered voice sample.

If the voice does not match after multiple attempts, the system asks for the backup password to grant access.

## Features

- Register voice as password
- Authenticate user using voice sample
- Display spoken text using speech recognition
- MFCC feature extraction for voice comparison
- Backup password support
- Maximum 10 authentication attempts
- Remaining attempt counter
- Access granted and denied messages
- User-friendly prompts

## Libraries Used

- SpeechRecognition
- pydub
- librosa
- numpy
- scipy
- google.colab
- IPython.display
- base64
- time

## Installation

```bash
pip install SpeechRecognition pydub librosa numpy scipy# Voice-Based-Password-Authentication-System
Voice-Based Password Authentication System Using MFCC and Backup Password
