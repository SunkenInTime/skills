#!/usr/bin/env python3
"""Reusable local video preparation and review. Requires ffmpeg and ffprobe."""
import argparse
import json
import math
from pathlib import Path
import re
import subprocess
from fractions import Fraction


def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True)


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]).stdout)


def rate(value):
    n = float(Fraction(str(value)))
    if not math.isfinite(n) or n <= 0:
        raise ValueError('Rate must be positive and finite')
    return n


def output(path, source):
    path = Path(path).resolve()
    if path == Path(source).resolve() or path.exists():
        raise ValueError('Choose a new output path; originals and existing outputs are preserved')
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)


def audio_log(source, filt):
    return run(['ffmpeg', '-hide_banner', '-i', source, '-vn', '-af', filt, '-f', 'null', '-']).stderr


def loudness(source, target=-16, ceiling=-1.5):
    log = audio_log(source, f'loudnorm=I={target}:TP={ceiling}:LRA=11:print_format=json')
    return json.loads(log[log.rfind('{'):log.rfind('}')+1])


def analyze(a):
    info = probe(a.source)
    log = audio_log(a.source, f'silencedetect=noise={a.noise}dB:d={a.min_pause}')
    gaps = [{'start': float(s), 'end': float(e), 'duration': float(e)-float(s)}
            for s,e in re.findall(r'silence_start: ([\d.]+).*?silence_end: ([\d.]+)', log, re.S)]
    return {'media': info, 'loudness': loudness(a.source), 'quiet_candidates': gaps,
            'review': 'Candidates only. Check syllable endings, quiet clip heads/tails, and intentional comedy pauses in playback.'}


def layout(a):
    w,h = a.canvas; sw,sh = a.asset
    left,top,right,bottom = a.region
    center = a.center or [(left+right)/2,(top+bottom)/2]
    cx,cy = center
    max_width,max_height = a.max_size or [w*(440 if a.logo else 940)/1080,h*480/1920]
    values = [w,h,sw,sh,left,top,right,bottom,cx,cy,max_width,max_height]
    if not all(math.isfinite(v) for v in values) or min(w,h,sw,sh,max_width,max_height) <= 0:
        raise ValueError('Dimensions must be positive and all geometry must be finite')
    if not (0 <= left < cx < right <= w and 0 <= top < cy < bottom <= h):
        raise ValueError('Region must fit the canvas and center must lie strictly inside it')
    available_width = 2*min(cx-left,right-cx)
    available_height = 2*min(cy-top,bottom-cy)
    width = min(max_width,available_width,min(max_height,available_height)*sw/sh)
    height = width*sh/sw
    estimate = {'ZoomX':width/w,'ZoomY':width/w,'Tilt':-(cy-h/2)*h/(w*sh/sw)}
    if cx == w/2:
        estimate['Pan'] = 0
    return {'canvas': [w,h], 'asset_size': [width,height], 'center': center,
            'bounds': [cx-width/2,cy-height/2,cx+width/2,cy+height/2],
            'usable_region': [left,top,right,bottom],
            'resolve_width_fit_estimate': estimate,
            'review': 'Fits the supplied region only. Verify platform controls, face clearance, animation peaks, and phone-size legibility in the composite. Resolve offsets are estimates; off-center Pan needs native placement.'}


def read_plan(path):
    p=json.loads(Path(path).read_text()); fps=rate(p['fps'])
    info=probe(p['source']); v=next(s for s in info['streams'] if s['codec_type']=='video')
    source_fps=rate(v['r_frame_rate'])
    if abs(source_fps-fps)>0.005:
        raise ValueError('This preview helper requires plan FPS to match source FPS; conform other rates explicitly')
    count=round(float(v.get('duration',info['format']['duration']))*fps)
    record=0
    for r in p['ranges']:
        s,e=r['start_frame'],r['end_frame']
        if type(s) is not int or type(e) is not int or not 0<=s<e<=count:
            raise ValueError(f'Invalid source range: {r}')
        if 'record_start_frame' in r and r['record_start_frame'] != record:
            raise ValueError('Record ranges must be contiguous for this helper')
        record+=e-s
    if not p['ranges'] or ('frames' in p and p['frames']!=record):
        raise ValueError('Empty plan or incorrect total frames')
    return p, fps, record


def validate(a):
    p,fps,frames=read_plan(a.plan)
    return {'source':p['source'],'ranges':len(p['ranges']),'frames':frames,'duration':frames/fps,
            'review':'Range validity is not editorial or syllable-boundary approval.'}


def preview(a):
    p,fps,frames=read_plan(a.plan)
    speed=rate(a.speed)
    if not 0.5<=speed<=2:
        raise ValueError('Comparison speed must be between 0.5 and 2')
    target=output(a.output,p['source']); filters=[]
    for i,r in enumerate(p['ranges']):
        s,e=r['start_frame'],r['end_frame']
        filters += [f'[0:v]fps={fps},trim=start_frame={s}:end_frame={e},setpts=PTS-STARTPTS[v{i}]',
                    f'[0:a]atrim=start={s/fps}:end={e/fps},asetpts=PTS-STARTPTS[a{i}]']
    filters += [''.join(f'[v{i}][a{i}]' for i in range(len(p['ranges'])))+
                f'concat=n={len(p["ranges"])}:v=1:a=1[v][a]',
                f'[v]setpts=PTS/{speed}[vo]', f'[a]atempo={speed}[ao]']
    run(['ffmpeg','-v','error','-n','-i',p['source'],'-filter_complex',';'.join(filters),
         '-map','[vo]','-map','[ao]','-r',str(fps),'-c:v','libx264','-preset','fast','-crf','18',
         '-threads','4','-c:a','aac','-b:a','320k','-movflags','+faststart',target])
    return {'output':target,'expected_duration':frames/fps/speed,'media':probe(target),
            'note':'Flattened pitch-preserving comparison. Preserve the editable Resolve timeline.'}


def audio_copy(a):
    target=output(a.output,a.source)
    duration=float(probe(a.source)['format']['duration'])
    if a.mode=='dialogue':
        m=loudness(a.source,a.target,a.ceiling)
        if not all(math.isfinite(float(m[k])) for k in ['input_i','input_tp','input_lra','input_thresh','target_offset']):
            raise ValueError('No usable measured dialogue')
        filt=(f'loudnorm=I={a.target}:TP={a.ceiling}:LRA=11:measured_I={m["input_i"]}:'
              f'measured_TP={m["input_tp"]}:measured_LRA={m["input_lra"]}:'
              f'measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}:linear=true')
    else:
        if a.peak is None or a.fade_start is None or not 0<=a.fade_start<duration:
            raise ValueError('SFX mode needs --peak and --fade-start within the file duration')
        log=audio_log(a.source,'volumedetect')
        peak=float(re.search(r'max_volume: ([-\d.]+)',log)[1])
        filt=f'volume={a.peak-peak}dB,afade=t=in:d=0.003,afade=t=out:st={a.fade_start}:d={duration-a.fade_start}:curve=qsin'
    run(['ffmpeg','-v','error','-n','-i',a.source,'-vn','-af',filt,'-ar','48000','-ac','2','-c:a','pcm_s24le',target])
    return {'output':target,'loudness':loudness(target),'review':'Audition with speech; source peak targets alone do not establish the mix.'}


def still(a):
    target=output(a.output,a.source)
    if a.duration<=0: raise ValueError('Duration must be positive')
    run(['ffmpeg','-v','error','-n','-loop','1','-i',a.source,'-t',str(a.duration),'-r',str(rate(a.fps)),
         '-c:v','png','-pix_fmt','rgba',target])
    return {'output':target,'media':probe(target)}


def frames(a):
    folder=Path(a.output).resolve();folder.mkdir(parents=True,exist_ok=True)
    duration=float(probe(a.source)['format']['duration']);results=[]
    for i,t in enumerate(a.times):
        if not 0<=t<duration: raise ValueError('Frame time outside video')
        target=output(folder/f'{i:03d}-{t:.3f}s.png',a.source)
        run(['ffmpeg','-v','error','-n','-ss',str(t),'-i',a.source,'-frames:v','1',target]);results.append(target)
    return {'frames':results,'review':'Inspect these rendered frames. Motion and audio still require contextual playback.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('analyze');p.add_argument('source');p.add_argument('--noise',type=float,default=-32);p.add_argument('--min-pause',type=float,default=.12);p.set_defaults(fn=analyze)
    p=sub.add_parser('layout');p.add_argument('--canvas',nargs=2,type=float,default=[1080,1920]);p.add_argument('--asset',nargs=2,type=float,required=True);p.add_argument('--logo',action='store_true')
    p.add_argument('--region',nargs=4,type=float,required=True,metavar=('LEFT','TOP','RIGHT','BOTTOM'),help='Usable pixel bounds after reserving face and platform UI space')
    p.add_argument('--center',nargs=2,type=float,help='Desired center in pixels; defaults to the region midpoint')
    p.add_argument('--max-size',nargs=2,type=float,help='Maximum asset width and height in pixels')
    p.set_defaults(fn=layout)
    p=sub.add_parser('validate-plan');p.add_argument('plan');p.set_defaults(fn=validate)
    p=sub.add_parser('preview');p.add_argument('plan');p.add_argument('output');p.add_argument('--speed',default='1');p.set_defaults(fn=preview)
    p=sub.add_parser('audio-copy');p.add_argument('source');p.add_argument('output');p.add_argument('--mode',choices=['dialogue','sfx'],required=True);p.add_argument('--target',type=float,default=-16);p.add_argument('--ceiling',type=float,default=-1.5);p.add_argument('--peak',type=float);p.add_argument('--fade-start',type=float);p.set_defaults(fn=audio_copy)
    p=sub.add_parser('still-clip');p.add_argument('source');p.add_argument('output');p.add_argument('--duration',type=float,required=True);p.add_argument('--fps',default='30000/1001');p.set_defaults(fn=still)
    p=sub.add_parser('frames');p.add_argument('source');p.add_argument('output');p.add_argument('--times',nargs='+',type=float,required=True);p.set_defaults(fn=frames)
    a=parser.parse_args()
    try: print(json.dumps(a.fn(a),indent=2))
    except (ValueError,KeyError,StopIteration,subprocess.CalledProcessError) as e:
        parser.exit(1,str(e)+'\n'+getattr(e,'stderr',''))

if __name__=='__main__':main()
