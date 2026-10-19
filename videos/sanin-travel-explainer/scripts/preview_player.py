"""Local-only player preview with HTTP byte ranges for native video seeking."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os,re

ROOT=Path(__file__).resolve().parents[1]
os.chdir(ROOT)

class VideoHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        self.byte_range=None
        path=Path(self.translate_path(self.path))
        header=self.headers.get('Range','')
        if path.is_file() and header.startswith('bytes='):
            size=path.stat().st_size
            match=re.fullmatch(r'bytes=(\d*)-(\d*)',header.strip())
            if match and size:
                a,b=match.groups()
                start=int(a) if a else max(0,size-int(b or size))
                end=min(int(b) if b and a else size-1,size-1)
                if start>=size or end<start:
                    self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.end_headers();return None
                f=path.open('rb');f.seek(start)
                self.send_response(206)
                self.send_header('Content-Type',self.guess_type(str(path)))
                self.send_header('Accept-Ranges','bytes')
                self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
                self.send_header('Content-Length',str(end-start+1))
                self.end_headers();self.byte_range=(start,end);return f
        return super().send_head()

    def end_headers(self):
        self.send_header('Accept-Ranges','bytes')
        super().end_headers()

    def copyfile(self,source,outputfile):
        try:
            if self.byte_range is None:return super().copyfile(source,outputfile)
            left=self.byte_range[1]-self.byte_range[0]+1
            while left:
                data=source.read(min(256*1024,left))
                if not data:break
                outputfile.write(data);left-=len(data)
        except (BrokenPipeError,ConnectionResetError):
            pass

if __name__=='__main__':
    print('Travel player: http://127.0.0.1:8766/旅程介紹.html',flush=True)
    ThreadingHTTPServer(('127.0.0.1',8766),VideoHandler).serve_forever()
