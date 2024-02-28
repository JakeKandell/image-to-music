import vertexai
from vertexai.vision_models import ImageTextModel, Image
from vertexai.language_models import TextGenerationModel
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy
import os
from django.conf import settings

PROJECT_ID = 'musc102-final-project'


def generate_music(imagePath):
    print("generating music")
    vertexai.init(project=PROJECT_ID)
    model = ImageTextModel.from_pretrained("imagetext@001")

    relative_image_path = os.path.relpath(imagePath)
    print(relative_image_path)
    source_image = Image.load_from_file(location=relative_image_path)

    captions = model.get_captions(
        image=source_image,
        # Optional:
        number_of_results=1,
        language="en",
    )

    specific_caption = captions[0]
    print(specific_caption)

    parameters = {
        "temperature": 0.2,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
        "top_p": 0.8,
        # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    model = TextGenerationModel.from_pretrained("text-bison@001")

    prompt = ("Write a one sentence description for an instrumental song, specifying instruments, style, era, and BPM, "
              "from the following text: ") + specific_caption

    response = model.predict(
        prompt,
        **parameters,
    )

    music_prompt = response.text
    print(music_prompt)

    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

    inputs = processor(text=[music_prompt], padding=True, return_tensors="pt")

    audio_values = model.generate(**inputs, max_new_tokens=800)
    sampling_rate = model.config.audio_encoder.sampling_rate

    musicOutPath = os.path.join(settings.MEDIA_ROOT, 'musicgen_out.wav')
    relMusicOutPath = os.path.relpath(musicOutPath)
    scipy.io.wavfile.write(relMusicOutPath, rate=sampling_rate, data=audio_values[0, 0].numpy())

    print("finished music generation")
    return musicOutPath


