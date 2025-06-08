from openai import OpenAI
from typing import List, Dict, NewType
import json
from os import getcwd, system, name, path
from sys import exit
from rich.console import Console
from rich.markdown import Markdown
from time import sleep
from .llm_logger import Logger, LoggerFactory
import tiktoken

# add custom error types

# History type alias for simplicity
type History = List[Dict[str, str]]

# exception handling done inside the class to help make it more modular and independent
class LLMConnection:
    """
    An interface for sending external Large Language Model API calls, and receiving responses.

    This also includes the use of a custom logger for added log handling.
    """
    def __init__(self) -> None:
        base_url:str = input("Please input the URL to send API requests to: ")
        api_key:str = input("Please input your API key, or enter the relative or absolute path to the file containing the key: ")

        self.__logger = LoggerFactory().getLogger()

        if path.exists(api_key):
                with open(api_key, 'r') as key_file:
                    api_key:str = key_file.readline()
        
        self.__connection:OpenAI = OpenAI(api_key=api_key, base_url=base_url)
        self.__history:History = [{"role": "system", "content": "You are a helpful assistant."}]

    def get_connection(self) -> OpenAI:
        return self.__connection
    
    def set_role(self, role:str) -> None:
        """
        Provide a specific context for the model.
        """
        self.__history[0]["content"] = role

    def get_history(self) -> History:
        return self.__history
    
    def get_logger(self) -> Logger:
        return self.__logger
    
    def count_tokens(self, messages: History, model: str = "deepseek-chat") -> int:
        enc = tiktoken.get_encoding("cl100k_base") # cl100k_base gives an approximate for deepseek
        return sum(len(enc.encode(msg["content"])) for msg in messages)
    
    # trimming context window using FIFO
    def trim_history(self, max_tokens: int = 128000) -> None:
        if self.count_tokens(messages=self.__history, model="deepseek-chat") > max_tokens:
            del self.__history[1]
            self.trim_history()
    
    def chat(self, chat_msg:str, console:Console) -> None:
        try:
            self.__history.append({"role": "user", "content": chat_msg})
            self.trim_history() # trim the context window before continuing

            response = self.__connection.chat.completions.create(
                model="deepseek-chat",
                messages=self.__history, # type: ignore
                stream=False
            ) # type: ignore

            text = response.choices[0].message.content
            console.print(Markdown(text), end="")
        except Exception as e:
            self.__logger.error(str(e) +
                              " Please make sure the API target and API key are correct," +
                              " and the correct API key file path (if used).")
            exit(1)
        else:
            self.__history.append({"role": "assistant", "content": "".join(text)})

    def save_history(self, file_path:str) -> None:
        if path.exists(file_path):
            with open(file_path, 'w') as file:
                json.dump(self.__history, file, indent=2)
            self.__logger.info("History successfully saved to {}.".format(getcwd()+'/'+file_path))
        else:
            self.__logger.error("Unable to save history.")

    def load_history(self, file_path:str) -> None:
        if path.exists(file_path):
            with open(file_path, 'r') as file:
                self.__history = json.load(file)
            self.__logger.info("History successfully loaded.")
        else:
            self.__logger.warning("History file not found. Defaulting to fresh history start.")