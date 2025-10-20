# Conversational-Voice-AI-for-Healthcare-Operations


A voice-based AI agent that can transcribe audio messages, classify intents, and generate appropriate responses for healthcare scenarios.

## Features

- Audio transcription using OpenAI's Whisper
- Intent classification for healthcare scenarios
- Multi-language support
- Modern web interface for audio upload and result display
- Dataset generation for testing and training

## Setup

1. Create Virtual Environment:
- On macOS:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Generating Test Dataset

The project includes a dataset generator that creates audio files for testing the Voice AI Agent. The dataset includes various healthcare scenarios in both English and Spanish.

To generate the dataset:

1. Run the dataset generator:
```bash
python generate_dataset.py
```

This will:
- Create a `test_data` directory
- Generate audio files for different healthcare scenarios
- Create a `dataset_metadata.json` file with information about the generated samples

The generated dataset includes:
- Appointment scheduling
- Insurance coverage inquiries
- Prescription refills
- Billing inquiries
- General inquiries

Each scenario has multiple samples in both English and Spanish.

## Running the Application

1. Start the FastAPI server:
```bash
uvicorn api:app --reload
```

The API will be available at `http://localhost:8000`

2. Use the web interface to:
- Upload audio files
- View transcription results
- See intent classification
- Get AI-generated responses

## Tools and Libraries Used

- **OpenAI Whisper**: For speech-to-text transcription
- **OpenAI GPT-3.5-turbo**: For intent classification and response generation
- **FastAPI**: For API development and web interface
- **langdetect**: For language detection
- **pydub**: For audio file processing
- **gTTS**: For text-to-speech in dataset generation
- **TailwindCSS**: For modern UI design
- **Python-multipart**: For handling file uploads

## Assumptions and Shortcuts

1. **Model Selection**:
   - Using Whisper's "base" model for faster processing
   - Using GPT-3.5-turbo instead of higher models for cost efficiency
   - Language detection based on transcribed text only

2. **Security**:
   - Basic API key authentication
   - No user authentication system
   - No data encryption for stored files

3. **Performance**:
   - No caching mechanism
   - Synchronous processing of audio files
   - No rate limiting

4. **Data Handling**:
   - Temporary file storage only
   - No persistent storage of audio files
   - No data retention policies

## Production Considerations

1. **Security**:
   - Add user login system to protect patient data
   - Encrypt audio files before storing them
   - Keep track of who accesses what data
   - Regularly update dependencies to fix security issues
   - Use HTTPS for all communications

2. **Scalability**:
   - Store processed results in a cache to avoid re-processing
   - Use a database to store user data and results
   - Add a queue system for handling multiple uploads
   - Set up automatic backups of important data
   - Add error handling for common issues

3. **Monitoring and Maintenance**:
   - Add logging to track errors and usage
   - Set up basic monitoring to know when things break
   - Create a simple dashboard to see system health
   - Add automated tests to catch bugs early
   - Plan for regular maintenance and updates

4. **Handling Data**:
   - Set up rules for how long to keep data
   - Create a backup system for important files
   - Remove personal information when not needed
   - Add data validation to catch errors early
   - Follow basic data protection rules

5. **User Experience**:
   - Add loading indicators for long operations
   - Make error messages helpful and clear
   - Add a way for users to report problems
   - Make the interface work well on mobile devices
   - Add more language options for the interface

## Supported Audio Formats
- MP3
- WAV
