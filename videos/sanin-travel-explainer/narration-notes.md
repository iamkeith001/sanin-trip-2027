# Narration and subtitle generation

- Voice: Microsoft Edge `zh-TW-HsiaoChenNeural`, Taiwanese female voice.
- Rate: +8%; no pitch shifting or post-generation time stretching.
- Generation: bundled `edge_tts_voice.py`; installed Edge TTS 7.2.7 initially returned HTTP 403. Current upstream `constants.py` and `drm.py` were loaded locally for compatibility, and the retry succeeded.
- Raw narration: `assets/voice/raw/01.wav` through `12.wav`.
- Trimmed playback narration: `assets/voice/01.wav` through `12.wav`, 24 kHz mono PCM 16-bit.
- Metadata: bundled `voice_meta.py` with 0.60 s scene holds and 1.80 s final hold.
- Caption text: exact Traditional Chinese script clauses; timing derives from silence spans and clause-length alignment, not word-level recognition. This is clause-level approximate timing.
- Playback total: 187.62 s.
- Speech file total: 179.210 s.
- Sample: `assets/voice/sample-first-two-lines.wav`.
- SRT: `captions.srt`, 94 cues, identical clause timestamps to `audio_meta.json`.

## Scene timing

|Frame|Start|Duration|
|---|---:|---:|
|1|0.00|11.98|
|2|11.98|14.48|
|3|26.46|15.15|
|4|41.61|15.97|
|5|57.58|16.02|
|6|73.60|15.50|
|7|89.10|17.68|
|8|106.78|17.41|
|9|124.19|15.86|
|10|140.05|16.51|
|11|156.56|16.28|
|12|172.84|14.78|
