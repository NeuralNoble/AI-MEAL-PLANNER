from openai import OpenAI
#from apikey import  apikey
import os
import streamlit as st
from PIL import Image
import requests
from io import BytesIO


########################################
# openAi key setup
########################################

def setup_apikey(apikey):
    os.environ['OPENAI_API_KEY'] = apikey
    OpenAI.api_key = apikey
    client = OpenAI()
    return client

########################################
# openAi audio to text
########################################

def generate_text_from_audio(client , audio_file, model="whisper-1",response_format="text"):
    response = client.audio.transcriptions.create(
        model=model,
        file=audio_file,
        response_format=response_format
    )

    return response

########################################
# openAi generate image
########################################

def generate_image_openai(client ,prompt, model="dall-e-2",size="512x512",n=1):
    resposne = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        n=n,
    )
    image_url = resposne.data[0].url
    img = requests.get(image_url)
    image = Image.open(BytesIO(img.content))
    return image


def generate_text_openai(client,prompt,text_area_placeholder=None,model="gpt-4o",temperature=0.5,max_tokens=1400,top_p=1
                         ,frequency_penalty=0,presence_penalty=0,stream=True,html=False):

    response = client.chat.completions.create(
        model=model,
        messages=[{"role":"user","content":prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stream=stream,
    )
    complete_response = []
    for chunk in response:
        if chunk.choices[0].delta.content:
            complete_response.append(chunk.choices[0].delta.content)
            result_string = ''.join(complete_response)

            #Auto scroll
            lines = result_string.count('\n')+1
            avg_char_per_line = 50
            lines += len(result_string) // avg_char_per_line
            height_per_line = 15
            total_height = lines * height_per_line

            if text_area_placeholder:
                if html:
                    text_area_placeholder.markdown(result_string,unsafe_allow_html=True)
                else:
                    text_area_placeholder.text_area("Generated Text", value=result_string,height=total_height)
    result_string = ''.join(complete_response)
    words = len(result_string.split())
    st.text(f"Total words Generated: {words}")


    return result_string




def main():
    pass
    # client = setup_apikey(apikey)
    #
    # ########### TExt generation with streaming ###########
    # st.title("ChatGPt")
    # prompt = st.text_input("Enter a prompt:")
    # text_area_placeholder = st.empty()
    # if st.button("Generate"):
    #     result = generate_text_openai(client,prompt,text_area_placeholder,html=True)
    #
    #
    #
    # ############## Image Generation ############
    # st.title("Image Generation using Dall-E-2")
    # prompt = st.text_input("Enter your prompt",value="describe your image")
    # if st.button("Generate Image"):
    #     with st.spinner("generating image..."):
    #         image = generate_image_openai(client,prompt)
    #         st.image(image)
    #
    #
    # ######### Audio Transcription ############
    # st.title("Audio transcriptions using whisper")
    # audio_file = st.file_uploader("Choose an audio file", type=["mp3", "wav"])
    # if audio_file:
    #     if st.button("Transcribe"):
    #         st.audio(audio_file,format="audio/wav")
    #         with st.spinner('Transcribing audio...'):
    #             result = generate_text_from_audio(client, audio_file)
    #             st.write(result)



if __name__ == '__main__':
    main()