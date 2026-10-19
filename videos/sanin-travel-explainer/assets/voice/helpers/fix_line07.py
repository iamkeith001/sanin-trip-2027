from pathlib import Path
import asyncio, importlib.util, sys, json, subprocess
import edge_tts
here=Path(__file__).parent
root=here.parents[2]
for name in ('constants','drm'):
    spec=importlib.util.spec_from_file_location(f'edge_tts.{name}',here/f'{name}_current.py')
    module=importlib.util.module_from_spec(spec)
    sys.modules[f'edge_tts.{name}']=module
    spec.loader.exec_module(module)
    setattr(edge_tts,name,module)
import edge_tts.communicate as communicate
communicate.SEC_MS_GEC_VERSION=sys.modules['edge_tts.constants'].SEC_MS_GEC_VERSION
communicate.DRM=sys.modules['edge_tts.drm'].DRM
spec=importlib.util.spec_from_file_location('voice_meta',str(Path.home()/'.claude/skills/motion-explainer-images/scripts/voice_meta.py'))
vm=importlib.util.module_from_spec(spec);spec.loader.exec_module(vm)
text=vm.script_lines(root)[7].replace('本期展覽已在一月三日結束','本期展覽到一月三日')
fix=root/'assets/voice/fix';fix.mkdir(parents=True,exist_ok=True)
asyncio.run(edge_tts.Communicate(text,'zh-TW-HsiaoChenNeural',rate='+8%').save(str(fix/'07-source.mp3')))
subprocess.run(['ffmpeg','-v','error','-y','-i',str(fix/'07-source.mp3'),'-ar','24000','-ac','1','-c:a','pcm_s16le',str(fix/'07-source.wav')],check=True)
vm.trim(fix/'07-source.wav',fix/'07-trimmed.wav')
spans,total=vm.speech_spans(fix/'07-trimmed.wav')
timed=vm.time_clauses(vm.clauses(text),spans)
target=17.08
ratio=total/target
subprocess.run(['ffmpeg','-v','error','-y','-i',str(fix/'07-trimmed.wav'),'-af',f'atempo={ratio:.12f},apad=whole_dur={target},atrim=duration={target}','-ar','24000','-ac','1','-c:a','pcm_s16le',str(fix/'07.wav')],check=True)
voice={'frame':7,'path':'assets/voice/07.wav','source':'host','speech_s':17.08,'duration_s':17.68,'words':[{'text':t,'start':round(s/ratio,3),'end':round(e/ratio,3)} for t,s,e in timed]}
(fix/'07-meta.json').write_text(json.dumps(voice,ensure_ascii=False,indent=2),encoding='utf-8')
(fix/'07-change-notes.json').write_text(json.dumps({'text':text,'original_trimmed_duration_s':total,'target_speech_s':target,'tempo_ratio':ratio,'actual_duration_s':vm.duration(fix/'07.wav'),'voice':'zh-TW-HsiaoChenNeural','rate':'+8%'},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'voice':voice,'source_duration':total,'atempo':ratio,'actual_duration':vm.duration(fix/'07.wav')},ensure_ascii=False,indent=2))
