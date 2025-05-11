import logging
import base64
from collections.abc import AsyncIterable

from homeassistant.components import stt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from tencentcloud_api import TencentCloudAsrAPi
from tencentcloud_api import ModuleSupportLanguage

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([ASRSTT(hass, config_entry)])


class ASRSTT(stt.SpeechToTextEntity):
    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        secretId = config_entry.data.get("secretid", "")
        secretKey = config_entry.data.get("secretKey", "")
        self.tencentCloudApi = TencentCloudAsrAPi(secretId, secretKey)

        self.model: str = config_entry.data.get("model", "16k_zh")
        # self._attr_name = f"TencentCloud Asr id: ({secretId})"
        self._attr_unique_id = f"{config_entry.entry_id[:7]}-tencentcloud-asr"

    @property
    def supported_languages(self) -> list[str]:
        return ModuleSupportLanguage.get(self.model, ["zh"])

    @property
    def supported_formats(self) -> list[stt.AudioFormats]:
        return [stt.AudioFormats.WAV]

    @property
    def supported_codecs(self) -> list[stt.AudioCodecs]:
        return [stt.AudioCodecs.PCM]

    @property
    def supported_bit_rates(self) -> list[stt.AudioBitRates]:
        return [stt.AudioBitRates.BITRATE_16]

    @property
    def supported_sample_rates(self) -> list[stt.AudioSampleRates]:
        return [stt.AudioSampleRates.SAMPLERATE_16000]

    @property
    def supported_channels(self) -> list[stt.AudioChannels]:
        return [stt.AudioChannels.CHANNEL_MONO]

    async def async_process_audio_stream(
        self, metadata: stt.SpeechMetadata, stream: AsyncIterable[bytes]
    ) -> stt.SpeechResult:
        _LOGGER.debug("process_audio_stream start")

        audio = b""
        async for chunk in stream:
            audio += chunk

        data = base64.b64encode(audio).decode("utf8", "ignore").strip()
        _LOGGER.debug(f"process_audio_stream transcribe: {data}")
        ret, result = self.tencentCloudApi.SentenceRecognition(self.model, data)
        if not ret:
            return stt.SpeechResult(result, stt.SpeechResultState.ERROR)
        if not result:
            return stt.SpeechResult("未识别到有效语音", stt.SpeechResultState.SUCCESS)

        return stt.SpeechResult(result, stt.SpeechResultState.SUCCESS)
