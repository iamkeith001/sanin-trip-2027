import runpy, sys, importlib.util
import edge_tts
from pathlib import Path
here=Path(__file__).parent
for name in ('constants','drm'):
    spec=importlib.util.spec_from_file_location(f'edge_tts.{name}',here/f'{name}_current.py')
    module=importlib.util.module_from_spec(spec)
    sys.modules[f'edge_tts.{name}']=module
    spec.loader.exec_module(module)
    setattr(edge_tts,name,module)
import edge_tts.communicate as communicate
communicate.SEC_MS_GEC_VERSION=sys.modules['edge_tts.constants'].SEC_MS_GEC_VERSION
communicate.DRM=sys.modules['edge_tts.drm'].DRM
sys.argv=['edge_tts_voice.py','--project',str(here.parents[2]),'--voice','zh-TW-HsiaoChenNeural','--rate','+8%']
runpy.run_path(str(Path.home()/'.claude/skills/motion-explainer-images/scripts/edge_tts_voice.py'),run_name='__main__')
