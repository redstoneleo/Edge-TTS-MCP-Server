<img width="2096" height="1306" alt="logo" src="https://github.com/user-attachments/assets/4f15e23b-7e55-4e68-8847-f53932314b20" />

# Microsoft Online Edge TTS & MCP Server

A Model Context Protocol server that enables LLMs to convert text to speech using the free [Microsoft Edge TTS](https://github.com/rany2/edge-tts), API and MCP are available. 
### Online Tool & Demo
https://huggingface.co/spaces/redstoneleo/Edge-TTS-MCP-Server
### Available Tools


-   `list_voices` – Fetches the available voices from Microsoft Edge TTS.
    
    -   **Returns** (object): A dictionary mapping **display names** (e.g., `"en-US-JennyNeural - Female"`) to their corresponding voice metadata, in the form:
        
        ```json
        {
          "Name": "Microsoft Server Speech Text to Speech Voice (zh-CN, XiaoxiaoNeural)",
          "ShortName": "zh-CN-XiaoxiaoNeural",
          "Gender": "Female",
          "Locale": "zh-CN",
          "SuggestedCodec": "audio-24khz-48kbitrate-mono-mp3",
          "FriendlyName": "Microsoft Xiaoxiao Online (Natural) - Chinese (Mainland)",
          "Status": "GA",
          "VoiceTag": {
            "ContentCategories": ["News", "Novel"],
            "VoicePersonalities": ["Warm"]
          }
        }
        
        ```
        


-   `text_to_speech` – Converts input text into speech audio using Microsoft Edge TTS.
    
    -   `text` (string, required): The text content to be synthesized into speech.
        
    -   `voice` (string, required): The selected voice in the format `"ShortName - Gender"`.
        
    -   `rate` (integer, optional): Speech rate adjustment percentage (e.g., `-20%` for slower, `+20%` for faster). Default: `0` means `+0%`.
        
    -   `pitch` (integer, optional): Pitch adjustment in Hz. Default: `0` means `+0Hz`.
        
    -   **Returns** (string): URL to the generated MP3 file.
        


### Prompts

- **list_voices**
  - list all available voice display names

- **text_to_speech**
  - TTS `<your text>` with a proper voice

## Installation and Configuration

 1. ```pip install edge_tts gradio -U``` 
 2. Download `app.py`.
 3. Run  ```python app.py```, then the console will show information
    like this
    
	    * Running on local URL:  http://127.0.0.1:7860
	    * To create a public link, set `share=True` in `launch()`.
	    
	    🔨 Launching MCP server:
	    ** Streamable HTTP URL: http://127.0.0.1:7860/gradio_api/mcp/
	    * [Deprecated] SSE URL: http://127.0.0.1:7860/gradio_api/mcp/sse

You can find the exact config to copy-paste by visiting the  local URL and going to the "Use via API or MCP" link in the footer of your Gradio app, and then clicking on "MCP".
<img width="1919" height="909" alt="mcp-usage-guide" src="https://github.com/user-attachments/assets/ecd85bb7-1043-49e1-85a6-9b392f1b7d85" />

For clients that support SSE (e.g. Cursor, Windsurf, Cline), simply add the following configuration to your MCP config, for detailed steps please refer [here](https://www.gradio.app/guides/using-docs-mcp#installing-in-the-clients).
```json
{
  "mcpServers": {
    "Edge TTS": {
      "url": "http://127.0.0.1:7860/gradio_api/mcp/"
    }
  }
}
```


## License


Edge TTS MCP Server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.
