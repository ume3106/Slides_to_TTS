import os
import re
import pickle
from typing import List
from google.cloud import texttospeech
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Slides API scopes
SLIDES_SCOPES = ['https://www.googleapis.com/auth/presentations.readonly']

# Configure Google Application Credentials
# 1) If the environment variable is not set, fall back to local `tts-key.json`
if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
    local_key_path = os.path.join(os.path.dirname(__file__), 'tts-key.json')
    if os.path.exists(local_key_path):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = local_key_path


def authenticate_slides() -> Credentials:
    creds = None
    # Store OAuth tokens and credentials in the same folder as this script
    token_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'token.pickle'))
    creds_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'credentials.json'))

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SLIDES_SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def get_presentation_id_from_url(url: str) -> str:
    if '/presentation/d/' in url:
        start = url.find('/presentation/d/') + len('/presentation/d/')
        end = url.find('/', start)
        if end == -1:
            end = url.find('#', start)
        if end == -1:
            end = len(url)
        return url[start:end]
    return url


def extract_notes_text(notes_page: dict) -> str:
    collected = []
    for element in notes_page.get('pageElements', []):
        shape = element.get('shape')
        if not shape:
            continue
        text_obj = shape.get('text')
        if not text_obj:
            continue
        for t in text_obj.get('textElements', []):
            run = t.get('textRun')
            if run and 'content' in run:
                collected.append(run['content'])
    return ''.join(collected).strip()


def text_to_ssml_with_punct_pause(text: str) -> str:
    # Normalize whitespace
    normalized = re.sub(r"\s+", " ", text)
    # Insert 1s break after full stop '。'
    # Keep the punctuation and add a break
    ssml_body = re.sub(r"。", "。<break time=\"1s\"/>", normalized)
    return f"<speak>{ssml_body}</speak>"


def synthesize_ssml_to_mp3(ssml: str, output_path: str, speaking_rate: float = 1.1) -> None:
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
    voice = texttospeech.VoiceSelectionParams(language_code="ja-JP", name="ja-JP-Standard-B")
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=speaking_rate)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as out:
        out.write(response.audio_content)


def generate_tts_from_slides(slides_input: str, output_dir: str) -> None:
    presentation_id = get_presentation_id_from_url(slides_input)
    creds = authenticate_slides()
    service = build('slides', 'v1', credentials=creds)

    presentation = service.presentations().get(presentationId=presentation_id).execute()
    slides = presentation.get('slides', [])
    print(f"プレゼンテーション名: {presentation.get('title', 'Unknown')} / スライド数: {len(slides)}")

    generated = 0
    for index, slide in enumerate(slides, start=1):
        notes_page_id = slide.get('slideProperties', {}).get('notesPage', {}).get('objectId')
        if not notes_page_id:
            print(f"- スライド {index:02d}: ノートページなし")
            continue

        notes_page = service.presentations().pages().get(presentationId=presentation_id, pageObjectId=notes_page_id).execute()
        notes_text = extract_notes_text(notes_page)

        if not notes_text:
            print(f"- スライド {index:02d}: スピーカーノートなし")
            continue

        ssml = text_to_ssml_with_punct_pause(notes_text)
        filename = f"slide_{index:02d}.mp3"
        output_path = os.path.join(output_dir, filename)
        synthesize_ssml_to_mp3(ssml, output_path, speaking_rate=1.1)
        print(f"✅ {filename} を生成しました（速度1.1・『。』後に1秒）")
        generated += 1

    print(f"\n完了: {generated} 個の音声を出力しました。保存先: {os.path.abspath(output_dir)}")


def main():
    print("=== Google Slides スピーカーノート → TTS(MP3) 生成 ===")
    slides_input = input("Google SlidesのURLまたはプレゼンテーションIDを入力してください: ").strip()
    # default output directory
    output_dir = os.path.join(os.path.dirname(__file__), 'slides')
    generate_tts_from_slides(slides_input, output_dir)


if __name__ == "__main__":
    main()
