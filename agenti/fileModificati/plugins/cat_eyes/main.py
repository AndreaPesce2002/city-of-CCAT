from pydantic import BaseModel, Field
from cat.log import log
from cat.mad_hatter.decorators import hook, plugin
from .image_parser import ImageParser

class Settings(BaseModel):
    api_key: str = Field(title="API Key", description="The API key for OpenAI's vision API.", default="")

@plugin
def settings_schema():   
    return Settings.schema()

@hook
def before_rabbithole_splits_text(text: list, cat):
    is_image = text[0].metadata["source"] == "cat_eyes"

    if is_image:
        content = text[0].page_content
        name = text[0].metadata["name"]
        cat.send_ws_message(f"""The image \"`{name}`\" describes:
                            \"{content}\"""", "chat")

    return text

@hook
def rabbithole_instantiates_parsers(file_handlers: dict, cat) -> dict:
    new_file_handlers = file_handlers

    settings = cat.mad_hatter.plugins["cat_eyes"].load_settings()

    if settings == {}:
        log.error("No configuration found for CatEyes")
        cat.send_ws_message("You did not configure the API key for the vision API!", "notification")
        return new_file_handlers

    new_file_handlers["image/png"] = ImageParser(settings["api_key"])
    new_file_handlers["image/jpeg"] = ImageParser(settings["api_key"])
    new_file_handlers["image/webp"] = ImageParser(settings["api_key"])
    new_file_handlers["image/gif"] = ImageParser(settings["api_key"])

    return new_file_handlers
