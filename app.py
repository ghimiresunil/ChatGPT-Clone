import os
import openai
import gradio as gr

from dotenv import load_dotenv

load_dotenv()

# if you have OpenAI API key as an environment variable, enable the below
openai.api_key = os.getenv("openai_api_key")

# if you have OpenAI API key as a string, enable the below
# openai.api_key = "https://beta.openai.com/account/api-keys"

start_sequence = "\nBot:"
restart_sequence = "\nHuman: "

prompt = """
The following is a conversation with an AI assistant.
The assistant is helpful, creative, clever, and very friendly.
\nHuman: Hello, who are you?
\nBot: I am an AI created by OpenAI. How can I help you today?
\nHuman:
"""


def openai_create(prompt):
    """Function to create a response

    Args:
        prompt (_type_): str
            piece of text or a set of instructions that is provided as input
    Returns:
        str: text
    """
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " Bot:"],
    )

    return response.choices[0].text


def chatgpt_clone(input, history):
    """Function to build Gradio Application

    Args:
        input (_type_): str
            text from user
        history (_type_): str
            stores the state of the current gradio application
            | stores knowledge of context of memory what is happening in past as well
    Returns:
        tuple: output and state
    """
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = " ".join(s)
    output = openai_create(inp)
    history.append((input, output))
    return history, history


## build web applications that combine markdown, HTML, buttons, and interactive components
block = gr.Blocks()


with block:
    gr.Markdown(
        """<h1><center>Build Yo'own ChatGPT with OpenAI API & Gradio</center></h1>
    """
    )
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder=prompt)
    state = gr.State()
    submit = gr.Button("SEND")
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])

block.launch(debug=True)
