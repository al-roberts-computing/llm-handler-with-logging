from typing import Optional
from .model import LLMConnection
from rich.markdown import Markdown
from rich.console import Console
from os.path import exists

def main(model:Optional[LLMConnection]=None, console:Optional[Console]=None,
         stop_keyword:str="Goodbye", checked_history:bool=False) -> None:
    current_model = model if model != None else LLMConnection()
    current_console = console if console != None else Console()

    if checked_history == False:
        history_path = input("Please specify the history file path (e.g., ./model_history.json), "+ \
                             "or leave blank if you'd like to start a new history: ")
        if exists(history_path):
            current_model.load_history(history_path)
    
    query = input("Your query (please type 'goodbye' if you wish to exit): ")

    if query.lower() != stop_keyword.lower():
        print("Please wait a moment while your query is processed.", end='\n\n')
        current_model.chat(chat_msg=query, console=current_console)
        return main(model=current_model, console=current_console, checked_history=True)
    else:
        history_response = input("\nWould you like to save your history? (y/n): ")
        if history_response.lower() == 'y' or history_response == "":
            current_model.save_history('model_history.json')

if __name__ == '__main__':
    main()