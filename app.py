import gradio as gr
import edge_tts
import aiohttp

import asyncio
import tempfile, time
from typing import TypedDict, List, Dict
from pathlib import Path



class VoiceTag(TypedDict, total=False):
    ContentCategories: List[str]
    VoicePersonalities: List[str]


class VoiceMetadata(TypedDict, total=False):
    Name: str
    ShortName: str
    Gender: str
    Locale: str
    SuggestedCodec: str
    FriendlyName: str
    Status: str
    VoiceTag: VoiceTag


async def list_voices() -> Dict[str, VoiceMetadata]:
    """
    Fetch available voices from Microsoft Edge TTS.

    Returns:
        Dict[str, VoiceMetadata]: A dictionary mapping display names
        (e.g. "en-US-JennyNeural - Female") to their corresponding in the form like { 'Name': 'Microsoft Server Speech Text to Speech Voice (zh-CN, XiaoxiaoNeural)', 'ShortName': 'zh-CN-XiaoxiaoNeural', 'Gender': 'Female', 'Locale': 'zh-CN', 'SuggestedCodec': 'audio-24khz-48kbitrate-mono-mp3', 'FriendlyName': 'Microsoft Xiaoxiao Online (Natural) - Chinese (Mainland)', 'Status': 'GA', 'VoiceTag': { 'ContentCategories': ['News', 'Novel'], 'VoicePersonalities': ['Warm'] } }
    """



    priority_order = [
        "zh",       # 中文优先
        "en-US",    # 美式英语
        "en-GB",    # 英式英语
        "en",       # 其他英语
        "hi",       # 印地语
        "es",       # 西班牙语
        "ar",       # 现代标准阿拉伯语
        "fr",       # 法语
        "bn",       # 孟加拉语
        "pt",       # 葡萄牙语
        "ru",       # 俄语
        "id",       # 印尼语
        "ur",       # 乌尔都语
        "de",       # 德语
        "ja",       # 日语
        "pcm",      # 尼日利亚皮钦语
        "ar-EG",    # 埃及阿拉伯语
        "mr",       # 马拉地语
        "vi",       # 越南语
        "te",       # 泰卢固语
        "ha",       # 豪萨语
        "tr",       # 土耳其语
        "pa",       # 西旁遮普语
        "sw",       # 斯瓦希里语
        "fil",      # 他加禄语
        "ta",       # 泰米尔语
        "yue",      # 粤语
        "wuu",      # 吴语
        "fa",       # 波斯语
        "ko",       # 韩语
        "th",       # 泰语
        "jv",       # 爪哇语
    ]

    lang_priority = {lang: i for i, lang in enumerate(priority_order)}

    def get_priority(short_name: str) -> tuple[int, str]:
        """
        Return (priority_rank, short_name) for stable sorting.
        """
        for prefix, rank in lang_priority.items():
            if short_name.startswith(prefix):
                return (rank, short_name)
        return (len(priority_order), short_name)  # 其他语言排最后，内部按 short_name

    n = 5
    for i in range(n):
        try:
            voices = await edge_tts.list_voices()
            break
        except Exception as e:
            time.sleep(1 * i)
            print("Retrying due to handshake error:", e)
            if i == n - 1:
                raise e

    # ✅ 先按优先级，再按 short_name 排序，保证同类不乱
    voices_sorted = sorted(voices, key=lambda v: get_priority(v["ShortName"]))

    return {f"{v['ShortName']} - {v['Gender']}": v for v in voices_sorted}


async def text_to_speech(text: str, voice: str, rate: int = 0, pitch: int = 0) -> str:
    """
    Convert input text to speech using Microsoft Edge TTS.

    Args:
        text (str): The text to synthesize into speech.
        voice (str): The selected voice in the format "ShortName - Gender".
        rate (int, optional): Speech rate adjustment percentage. Default is 0.
        pitch (int, optional): Pitch adjustment in Hz. Default is 0.

    Returns:
        str: Path to the generated MP3 file.
    """

    voice_short_name = voice.split(" - ")[0]
    rate_str = f"{rate:+d}%"
    pitch_str = f"{pitch:+d}Hz"

    n = 5
    for i in range(n):
        try:
            communicate = edge_tts.Communicate(
                text, voice_short_name, rate=rate_str, pitch=pitch_str
            )
            break
        except aiohttp.client_exceptions.WSServerHandshakeError as e:
            time.sleep(1 * i)
            print("Retrying due to handshake error:", e)
            if i == n - 1:
                raise e

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_path = tmp_file.name
        await communicate.save(tmp_path)

    path = Path(tmp_path)
    return path.as_posix()#后面output到gr.Audio上，通过程序交互的时候gradio会将其转化为url，很神奇！


i18n = gr.I18n(
    en={"pageTitle": "# 🎙️ Microsoft Online Edge TTS & MCP Server", 
    "generateSpeech": "Generate Speech",
    'description':"""Convert text to speech using the free [Microsoft Edge TTS](https://github.com/rany2/edge-tts), API and MCP are available. Made by [MathJoy](https://www.cnblogs.com/imath).""",
    "selectVoice":"Select Voice",
    "speechRateAdjustment":"Speech Rate Adjustment (%)",
    "pitchAdjustment":"Pitch Adjustment (Hz)",
    "inputText":"Input Text"
    },
    zh={"pageTitle": "# 🎙️ 微软线上 Edge TTS & MCP", 
    "generateSpeech": "生成语音",
    'description':"""文本语音合成，基于免费的[Microsoft Edge TTS](https://github.com/rany2/edge-tts)，由[MathJoy](https://www.cnblogs.com/imath)精心制作，也可通过API或MCP来使用。""",
    "selectVoice":"选择音色",
    "speechRateAdjustment":"语速调整 (%)",
    "pitchAdjustment":"音量调整 (Hz)",
    "inputText":"输入文字"
    }
)

async def create_UI():


    voices = await list_voices()
    
    with gr.Blocks(title="Microsoft Edge TTS & MCP",analytics_enabled=False) as UI:
        gr.api(#默认只在fn处暴露工具，这里主动暴露这个tool
            list_voices
        )

        gr.Markdown(i18n("pageTitle"))
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown(i18n("description"))
                
        with gr.Row():
            with gr.Column():
                text_input = gr.Textbox(label=i18n("inputText"), lines=5,value='Your text here')
                
                voiceList=list(voices.keys())
                voice_dropdown = gr.Dropdown(
                    choices=voiceList,
                    label=i18n("selectVoice"),
                    value=voiceList[0])

                rate_slider = gr.Slider(
                    minimum=-50, maximum=50, value=0,
                    label=i18n("speechRateAdjustment"), step=1
                )

                pitch_slider = gr.Slider(
                    minimum=-20, maximum=20, value=0,
                    label=i18n("pitchAdjustment"), step=1
                )
                
                generate_btn = gr.Button(i18n("generateSpeech"), variant="primary")
                audio_output = gr.Audio(label="Generated Audio", type="filepath",autoplay=True)
                
                generate_btn.click(
                    fn=text_to_speech,
                    inputs=[text_input, voice_dropdown, rate_slider, pitch_slider],
                    outputs=[audio_output]
                )
    
    return UI


async def main():
    UI = await create_UI()
    UI.queue(default_concurrency_limit=50)
    UI.launch(
        # show_api=False,
        i18n=i18n,
        mcp_server=True  # ✅ make this an MCP server
    )

if __name__ == "__main__":
    asyncio.run(main())
