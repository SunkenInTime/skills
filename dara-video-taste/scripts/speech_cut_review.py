"""Review a source-range edit without exporting video. Requires numpy, Pillow, ffmpeg.
Produces source-context waveforms and flags; never changes editorial boundaries.
"""
import argparse,json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw

def review(plan_path,output):
 p=json.loads(Path(plan_path).read_text());fps=float(p['fps']);out=Path(output);out.mkdir(parents=True,exist_ok=True)
 x=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',p['source'],'-vn','-ac','1','-ar','16000','-f','f32le','-']),np.float32)
 position=0;report=[]
 for i,r in enumerate(p['ranges']):
  s,e=r['start_frame'],r['end_frame'];a,b=s/fps,e/fps
  assert 0<=s<e and r['record_start_frame']==position,(i,'Invalid range or gap/overlap')
  assert r.get('reason'),(i,'Missing editorial reason')
  z=x[round(a*16000):round(b*16000)];step=80;n=len(z)//step;pk=np.max(np.abs(z[:n*step].reshape(n,step)),axis=1);active=np.flatnonzero(pk>.015)
  head=active[0]*.005 if len(active) else b-a;tail=(n-1-active[-1])*.005 if len(active) else b-a
  flags=[]
  if e-s<9:flags.append('SHORT_CLIP_REQUIRES_COMPLETE_WORD_REVIEW')
  if head>.12:flags.append('QUIET_HEAD_REQUIRES_REVIEW')
  if tail>.12:flags.append('QUIET_TAIL_REQUIRES_REVIEW')
  # An energetic edge needs source context. This does not prove a clipped phoneme.
  if np.max(np.abs(z[:160]))>.04:flags.append('ACTIVE_START_REQUIRES_REVIEW')
  if np.max(np.abs(z[-160:]))>.04:flags.append('ACTIVE_END_REQUIRES_REVIEW')
  report.append(dict(index=i,source=[a,b],timeline=[position/fps,(position+e-s)/fps],reason=r['reason'],head_quiet_seconds=head,tail_quiet_seconds=tail,flags=flags))
  position+=e-s
 # Both incoming and outgoing contexts, with discarded sound visible in grey.
 for pg in range(0,len(report),8):
  im=Image.new('RGB',(1600,1440),'white');d=ImageDraw.Draw(im)
  for j,row in enumerate(report[pg:pg+8]):
   y=j*180;d.text((5,y+4),f"{row['index']} {row['reason']} | {','.join(row['flags'])}",fill='black')
   for side,boundary in enumerate(row['source']):
    lo,hi=boundary-.5,boundary+.5;left=side*800+20
    for k in range(750):
     t=lo+k/750;u=lo+(k+1)/750;z=x[max(0,round(t*16000)):max(0,round(u*16000))]
     if len(z):
      amp=min(47,float(np.max(np.abs(z)))*260);color='black' if row['source'][0]<=t<row['source'][1] else '#aaaaaa';d.line((left+k,y+90-amp,left+k,y+90+amp),fill=color)
    xx=left+375;d.line((xx,y+25,xx,y+150),fill='red',width=2);d.text((left,y+154),f"{'IN' if side==0 else 'OUT'} {boundary:.3f} +/- 0.5s",fill='black')
  im.save(out/f'boundaries-{pg//8}.png')
 data=dict(frames=position,duration=position/fps,clips=len(report),review_limit='Flags locate candidates; transcript and waveform checks do not establish perceptual approval.',boundaries=report)
 (out/'report.json').write_text(json.dumps(data,indent=2));print(json.dumps({k:v for k,v in data.items()if k!='boundaries'}));print(json.dumps([r for r in report if r['flags']],indent=2))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('plan');a.add_argument('output');v=a.parse_args();review(v.plan,v.output)
