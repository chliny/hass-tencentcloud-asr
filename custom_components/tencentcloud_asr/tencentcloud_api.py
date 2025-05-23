import logging
from homeassistant.components.stt import AudioCodecs
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.asr.v20190614.asr_client import AsrClient
from tencentcloud.asr.v20190614.models import SentenceRecognitionRequest, SentenceRecognitionResponse

_LOGGER = logging.getLogger(__name__)


SentenceRecognitionSourceTypePost = 1
SentenceRecognitionSourceTypeURL = 0
ModuleSupportLanguage = {
    "16k_zh": ["zh-cn"],
    "16k_zh-PY": ["zh-cn", "en", "zh-hk"],
    "16k_en": ["en"],
    "16k_yue": ["zh-hk"],
    "16k_zh_dialect": ["zh"],
}
DefaultModel = "16k_zh"


class TencentCloudAsrAPi(object):
    def __init__(self, secretId, secretKey):
        cred = credential.Credential(secretId, secretKey)
        region = ""
        self.asrClient = AsrClient(cred, region)

    def SentenceRecognition(self, engSerViceType, data: str) -> (tuple[bool, str | None]):
        req = SentenceRecognitionRequest()
        req.EngSerViceType = engSerViceType
        req.SourceType = SentenceRecognitionSourceTypePost
        req.VoiceFormat = AudioCodecs.PCM
        req.ProjectId = 0
        req.SubServiceType = 2
        req.UsrAudioKey = ""
        req.Data = data
        req.DataLen = len(data)
        try:
            res: SentenceRecognitionResponse = self.asrClient.SentenceRecognition(req)
            return True, res.Result
        except TencentCloudSDKException as err:
            _LOGGER.error("recognition failed:%s", err.message)
            return False, str(err)
