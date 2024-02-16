import requests
import base64
from typing import Iterator
from langchain.schema import Document
from langchain.document_loaders.blob_loaders import Blob
from langchain.document_loaders.base import BaseBlobParser

class ImageParser(BaseBlobParser):
    """Parser for audio blobs."""

    def __init__(self, key: str):
        self.key = key

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        """Lazily parse the blob."""

        content = ""

        binary_data = blob.as_bytes()

        if len(binary_data) > 20 * 1000000:
            content = "The image is too large for OpenAI to process."
        else:
            base64_image = base64.b64encode(binary_data).decode('utf-8')

            res = requests.post("https://api.openai.com/v1/chat/completions", 
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.key}"
                }, json = {
                    "model": "gpt-4-vision-preview",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "What’s in this image?"
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                }
                        ]
                        }
                    ],
                    "max_tokens": 300
                } 
            )
            json = res.json()
            
            content = json["choices"][0]["message"]["content"]

        yield Document(page_content=content, metadata={"source": "cat_eyes", "name": blob.path.rsplit('.', 1)[0]})
