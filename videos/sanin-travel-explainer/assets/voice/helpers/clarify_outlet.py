"""Regenerate only Day 7 with the user's preferred outlet shopping wording."""
from pathlib import Path
import asyncio,importlib.util,sys,json,subprocess,shutil
import edge_tts
here=Path(__file__).resolve().parent;root=here.parents[2]
for name in ('constants','drm'):
 spec=importlib.util.spec_from_file_location(f'edge_tts.{name}',here/f'{name}_current.py');mod=importlib.util.module_from_spec(spec);sys.modules[f'edge_tts.{name}']=mod;spec.loader.exec_module(mod);setattr(edge_tts,name,mod)
import edge_tts.communicate as c
c.SEC_MS_GEC_VERSION=sys.modules['edge_tts.constants'].SEC_MS_GEC_VERSION;c.DRM=sys.modules['edge_tts.drm'].DRM
spec=importlib.util.spec_from_file_location('voice_meta',str(Path.home()/'.claude/skills/motion-explainer-images/scripts/voice_meta.py'));vm=importlib.util.module_from_spec(spec);spec.loader.exec_module(vm)
text=vm.script_lines(root)[9];fix=root/'assets/voice/fix';fix.mkdir(parents=True,exist_ok=True)
shutil.copy2(root/'assets/voice/09.wav',fix/'09-before-outlet.wav')
asyncio.run(edge_tts.Communicate(text,'zh-TW-HsiaoChenNeural',rate='+8%').save(str(fix/'09-outlet.mp3')))
subprocess.run(['ffmpeg','-v','error','-y','-i',str(fix/'09-outlet.mp3'),'-ar','24000','-ac','1','-c:a','pcm_s16le',str(fix/'09-outlet-source.wav')],check=True)
vm.trim(fix/'09-outlet-source.wav',fix/'09-outlet-trim.wav')
spans,total=vm.speech_spans(fix/'09-outlet-trim.wav');timed=vm.time_clauses(vm.clauses(text),spans)
meta=json.loads((root/'audio_meta.json').read_text());voice=next(v for v in meta['voices'] if v['frame']==9);target=voice['speech_s'];ratio=total/target
subprocess.run(['ffmpeg','-v','error','-y','-i',str(fix/'09-outlet-trim.wav'),'-af',f'atempo={ratio:.12f},apad=whole_dur={target},atrim=duration={target}','-ar','24000','-ac','1','-c:a','pcm_s16le',str(root/'assets/voice/09.wav')],check=True)
voice['words']=[{'text':t,'start':round(s/ratio,3),'end':round(e/ratio,3)} for t,s,e in timed]
(root/'audio_meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'original_s':total,'target_s':target,'ratio':ratio,'spans':len(spans),'words':voice['words']},ensure_ascii=False))
