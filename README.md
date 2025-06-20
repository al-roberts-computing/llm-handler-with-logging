# LLM API Connection Handler Example With Logging and Context Trimming
The scale and compute resources required to create and fine-tune Large Language Models (LLMs) are immense. Instead, many LLM service providers offer an Application Programming Interface (API) where certain services can be linked to an LLM without having to go directly through the official company's chat room. This repository contains an example of connecting to the DeepSeek API, and utilising this in the command line / terminal 💻 This also includes a method of context window trimming (so the max token length is not exceeded).
## Setup 🛠️
Download the repository, then install the Python requirements using `pip install -r requirements.txt`.
## Making an API call 📞
`__main__.py` contains some example code to run the application. To run the package, you can execute `python -m llm-handler-with-logging-main`. Any logs are saved to **llm_logs.txt** in the current running directory. The custom logging approach was done using a factory-singleton design pattern method, just to add an extra interesting coding method. If you save the model history, it will be saved to **model_history.json**.
