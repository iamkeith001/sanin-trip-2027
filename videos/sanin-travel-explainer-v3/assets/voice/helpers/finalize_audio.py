from pathlib import Path
import json, subprocess, wave, math
import numpy as np
root=Path(__file__).resolve().parents[3]
meta=json.loads((root/'audio_meta.json').read_text())
voices=meta['voices']
# One clause is one cue; timing comes directly from the bundled metadata tool.
def stamp(t):
    ms=round(t*1000); h,ms=divmod(ms,3600000); m,ms=divmod(ms,60000); s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'
cue=[]; offset=0; frame_starts=[]
for v in voices:
    frame_starts.append(offset)
    for w in v['words']:
        cue.append(f"{len(cue)+1}\n{stamp(offset+w['start'])} --> {stamp(offset+w['end'])}\n{w['text']}\n")
    offset+=v['duration_s']
(root/'captions.srt').write_text('\n'.join(cue),encoding='utf-8')
# Two-line review sample with the same 0.6s frame gap as the full video.
sr=24000
sample=[]
for v in voices[:2]:
    with wave.open(str(root/v['path']),'rb') as w: audio=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16)
    sample.extend([audio,np.zeros(round((v['duration_s']-v['speech_s'])*sr),dtype=np.int16)])
with wave.open(str(root/'assets/voice/sample-first-two-lines.wav'),'wb') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(np.concatenate(sample).tobytes())
# Original procedural ambient music: D major pentatonic, low warm pad and sparse plucks.
# No sampled recordings, no borrowed melody, no external music service.
rate=44100; total=offset; N=round(total*rate)
music=np.zeros((N,2),np.float32)
roots=[50,55,59,57] # D3, G3, B3, A3; broad harmonic beds

def note(freq,dur,kind):
    t=np.arange(round(dur*rate),dtype=np.float64)/rate
    if kind=='pad':
        env=np.minimum(t/1.8,1)*np.minimum((dur-t)/2.3,1)
        y=np.sin(2*np.pi*freq*t)+.20*np.sin(2*np.pi*2*freq*t)+.08*np.sin(2*np.pi*3*freq*t)
        y*=env*(.92+.08*np.sin(2*np.pi*.14*t))
    else:
        env=(1-np.exp(-t/.014))*np.exp(-t/1.1)*np.minimum((dur-t)/.4,1)
        y=(np.sin(2*np.pi*freq*t)+.32*np.sin(2*np.pi*2*freq*t)+.09*np.sin(2*np.pi*4*freq*t))*env
    return y.astype(np.float32)

def add(y,start,amp,pan):
    i=round(start*rate); n=min(len(y),N-i)
    if n<=0:return
    music[i:i+n,0]+=y[:n]*amp*math.sqrt((1-pan)/2)
    music[i:i+n,1]+=y[:n]*amp*math.sqrt((1+pan)/2)

# overlapping 12 second chords; pentatonic voicings avoid strong cadences
for k,start in enumerate(np.arange(0,total,11.0)):
    r=roots[k%4]
    for j,semi in enumerate((0,7,14)):
        freq=440*2**((r+semi-69)/12)
        add(note(freq,15,'pad'),float(start),.009,(-.45,0,.45)[j])
# Sparse deterministic figure, with large spaces for speech.
scale=[74,78,81,83,86]
pattern=[0,2,1,4,2,3,1,2,0,3,2,4,1,0,2,3]
for k,start in enumerate(np.arange(3,total-4,2.75)):
    midi=scale[pattern[k%len(pattern)]]
    y=note(440*2**((midi-69)/12),3.6,'pluck')
    add(y,float(start),.014,(-.5,.35,-.2,.55)[k%4])
    add(y,float(start+.21),.0035,.45 if k%2 else -.45)
# Smooth 3s intro and 5s outro.
fade=np.minimum(np.arange(N)/(rate*3),1)*np.minimum((N-np.arange(N))/(rate*5),1)
music*=fade[:,None]
out=root/'assets/audio';out.mkdir(parents=True,exist_ok=True)
with wave.open(str(out/'music-bed.wav'),'wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(rate);w.writeframes((np.clip(music,-1,1)*32767).astype('<i2').tobytes())
# Gentle original two-tone transition chime, intentionally quiet.
dur=1.6;t=np.arange(round(dur*rate))/rate
y=(np.sin(2*np.pi*880*t)+.55*np.sin(2*np.pi*1320*t))*(1-np.exp(-t/.006))*np.exp(-t/0.37)*.018
with wave.open(str(out/'chime.wav'),'wb') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes((y*32767).astype('<i2').tobytes())
(root/'original-music-notes.md').write_text(f'''# Original music and transition cue\n\nGenerated specifically for this travel explainer by Codex, using deterministic NumPy additive synthesis. No music samples, recordings, existing melodies or external music-generation service were used.\n\n- Bed: {total:.2f} s, stereo 44.1 kHz PCM 16-bit, D major pentatonic, warm overlapping pads and sparse original plucks.\n- Transition cue: 1.60 s, mono 44.1 kHz PCM 16-bit, two softly decaying sine tones.\n- Files: `assets/audio/music-bed.wav`, `assets/audio/chime.wav`.\n- Source: `assets/voice/helpers/finalize_audio.py`.\n- Music is deliberately quiet; mix under narration and apply final mix loudness management.\n''',encoding='utf-8')
(root/'narration-notes.md').write_text(f'''# Narration and subtitle generation\n\n- Voice: Microsoft Edge `zh-TW-HsiaoChenNeural`, Taiwanese female voice.\n- Rate: +8%; no pitch shifting or post-generation time stretching.\n- Generation: bundled `edge_tts_voice.py`; installed Edge TTS 7.2.7 initially returned HTTP 403. Current upstream `constants.py` and `drm.py` were loaded locally for compatibility, and the retry succeeded.\n- Raw narration: `assets/voice/raw/01.wav` through `12.wav`.\n- Trimmed playback narration: `assets/voice/01.wav` through `12.wav`, 24 kHz mono PCM 16-bit.\n- Metadata: bundled `voice_meta.py` with 0.60 s scene holds and 1.80 s final hold.\n- Caption text: exact Traditional Chinese script clauses; timing derives from silence spans and clause-length alignment, not word-level recognition. This is clause-level approximate timing.\n- Playback total: {total:.2f} s.\n- Speech file total: {sum(v['speech_s'] for v in voices):.3f} s.\n- Sample: `assets/voice/sample-first-two-lines.wav`.\n- SRT: `captions.srt`, {len(cue)} cues, identical clause timestamps to `audio_meta.json`.\n\n## Scene timing\n\n|Frame|Start|Duration|\n|---|---:|---:|\n'''+'\n'.join(f"|{v['frame']}|{start:.2f}|{v['duration_s']:.2f}|" for start,v in zip(frame_starts,voices))+'\n',encoding='utf-8')
print(json.dumps({'duration_s':total,'speech_s':sum(v['speech_s'] for v in voices),'captions':len(cue),'frame_starts':frame_starts,'music_peak':float(np.max(np.abs(music)))},indent=2))
