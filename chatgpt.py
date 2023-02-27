import openai
import streamlit as st
from streamlit_chat import message


# Call OpenAI API to receive response
def generate_response(prompt, model_engine, temperature=0.4, presence_penalty=0, frequency_penalty=0):

    # concat context
    context = ''
    for i in range(len(st.session_state.past)):
        context += f"question {i + 1}: {st.session_state.past[i]}" + "\n"
        context += f"ans {i + 1}: {st.session_state.generated[i]}" + "\n"

    # package context with prompt
    prompt_with_context = f"context: {context}" + "\n" + f"prompt: {prompt}" + "\n"

    # get response
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt_with_context,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=temperature,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty
    )
    message = completions.choices[0].text
    return message


def chat_page():

    openai.api_key = st.secrets['OPENAI_API_KEY']
    model_engine = st.secrets['MODEL_ENGINE']

    # Page setup
    # Disable hamburger & footer
    hide_menu_style = """
            <style>
            MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after{
                content: "Copyright @ 2023 Artefact. All Rights Reserved";
                visibility: visible;
                display: block;
                position: relative;
                color: #66CCCC;
                padding: 5px;
                top: 2px;
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    # Header setup
    header = """
            <h1 style="color:#ff0066;font-size:43px;">
            Artefact ChatBot
            </h1>
            """
    st.markdown(header, unsafe_allow_html=True)

    # Sidebar setup, with About, Parameter sliders & Doc reference
    with st.sidebar:
        st.image('artefact.png', use_column_width='always')
        st.write('\n')
        header1 = """
                <h1 style="color:#ff0066;font-size:20px;">
                About
                </h1>
                """
        st.markdown(header1, unsafe_allow_html=True)
        st.write('This is a ChatBot powered by OpenAI & Streamlit for Artefact internal use. Currently, the model engine it loads is text-davinci-003.')
        header2 = """
                <h1 style="color:#ff0066;font-size:20px;">
                Available Parameters
                </h1>
                """
        st.markdown(header2, unsafe_allow_html=True)
        temp_inst= """
                <h2 style="color:#66CCCC;font-size:17px;">
                temperature
                </h2>
                """
        st.markdown(temp_inst, unsafe_allow_html=True)
        temperature = st.slider(
        "Randomness of response. Lower temperatures tend to give more robust responses. Default = 0.4", 0.0, 2.0, 0.4, 0.01, key="temperature")
        pres_inst= """
                <h2 style="color:#66CCCC;font-size:17px;">
                presence_penalty
                </h2>
                """
        st.markdown(pres_inst, unsafe_allow_html=True)
        presence_penalty = st.slider(
        "Increase to encourage model to talk about new topic. Default = 0", -2.0, 2.0, 0.0, 0.01, key="presence_penalty")
        freq_inst= """
                <h2 style="color:#66CCCC;font-size:17px;">
                frequency_penalty
                </h2>
                """
        st.markdown(freq_inst, unsafe_allow_html=True)
        frequency_penalty = st.slider(
        "Increase to penalize model for repeating the same line verbatim. Default = 0", -2.0, 2.0, 0.0, 0.01, key="frequency_penalty")
        header3 = """
                <h1 style="color:#ff0066;font-size:20px;">
                Help
                </h1>
                """
        st.markdown(header3, unsafe_allow_html=True)
        st.write("Please refer to [OpenAI API documentation](https://platform.openai.com/docs/api-reference/completions/create) for detailed information about the parameters.",
                 unsafe_allow_html=True)

    # Storing the chat
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    if 'return_text' not in st.session_state:
        st.session_state['return_text'] = ''

    # Chat now!
    text_form = st.form(key='my_form', clear_on_submit=True)
    user_input = text_form.text_input(label="You:", value='', placeholder="Hello, how are you?")
    submit_button = text_form.form_submit_button(label='Submit')

    if submit_button:
        output = generate_response(prompt=user_input,
                                   model_engine=model_engine,
                                   temperature=st.session_state.temperature,
                                   presence_penalty=st.session_state.presence_penalty,
                                   frequency_penalty=st.session_state.frequency_penalty)

        # store the output
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    if st.session_state['generated']:
        # enable codes below to test parameter changes
        # message(f"""
        # Current temperature is {st.session_state.temperature},
        # presence_penalty is {st.session_state.presence_penalty},
        # frequency_penalty is {st.session_state.frequency_penalty}
        # """)
        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

