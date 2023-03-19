# Talk2GPT

Talk2GPT is a Python-based application that allows users to interact with OpenAI's GPT-3.5 Turbo language model using voice input. The application leverages an Automatic Speech Recognition (ASR) system to transcribe audio input from users and the Whisper API to perform transcription. The GPT-3.5 Turbo model is then used to generate responses to user queries.
In addition, the application utilizes the Google Cloud Text-to-Speech API to convert the generated text responses into speech. This feature enables Talk2GPT to provide a seamless and natural conversation experience for the user. 

Overall, Talk2GPT provides an innovative approach to interacting with GPT-3.5 Turbo and showcases the potential of voice-enabled AI applications. The repository contains all the necessary code and dependencies required to run the application, along with detailed documentation and examples to help users get started.

## Requirements

The following dependencies are required to run Talk2GPT:

    Python 3.7+
    PyAudio
    wave
    audioop
    math
    openai
    pygame
    google-cloud-texttospeech
    pydub
    
    Install the required packages: pip install -r requirements.txt

In addition, you will need to have an OpenAI API key and a Whisper API key in order to use the application.

## Usage

To use Talk2GPT, simply run the talk2gpt.py script from the command line using Python:

    python talk2gpt.py

The application will then prompt you to speak into your microphone. After you speak, the audio will be transcribed and sent to the GPT-3.5 Turbo model, which will generate a response. The response will then be synthesized into audio using Google's Text-to-Speech API and played back through your speakers.

## Contributing

If you would like to contribute to Talk2GPT, please feel free to submit a pull request or open an issue on the repository. Any contributions or feedback are greatly appreciated!

## License

Talk2GPT is licensed under the MIT License. See the LICENSE file for details.
