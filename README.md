# hass-tencentcloud-asr

腾讯云语音识别服务 homeassistantstt集成

## 安装

- 腾讯云上开通[语音识别服务](https://cloud.tencent.com/product/asr)，获取SecretId 和 SecretKey
- HACS -> 集成 -> 右上解选项 -> 自定义存储库
  - 存储库: https://github.com/chliny/hass-tencentcloud-asr
  - 类别: 集成
- 浏览并下载存储库 -> 搜索 TencentCloud ASR 并下载
- 重启Homeassistant
- Homeassistant 添加集成
  - 设置 -> 设备与服务 -> 添加集成 -> 搜索 TencentCloud ASR -> 填入腾讯云API密钥和Secret
  - 提交后稍等片刻，即可看到`tencentcloud_asr`实体

## 模型

| 模型 | 说明 |
|------|------|
|16k_zh| 中文通用|
|16k_zh-PY|中英粤|
|16k_en|英语|
|16k_yue|粤语|
|16k_zh_dialect|多方言|

- 更新模型详细说明，请参考[腾讯云文档](https://cloud.tencent.com/document/product/1093/35646)

