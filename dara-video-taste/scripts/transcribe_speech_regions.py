"""Independent CTC word evidence for short source regions; no video export.
Recognition can miss names and punctuation. Compare with contextual ASR and waveform.
"""
import argparse,json,subprocess
from pathlib import Path
import numpy as np
import torch
from transformers import Wav2Vec2Processor,Wav2Vec2ForCTC

def main():
 p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('regions',help='JSON list of objects containing start and end seconds');p.add_argument('output');a=p.parse_args()
 regions=json.loads(Path(a.regions).read_text());x=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',a.source,'-vn','-ac','1','-ar','16000','-f','f32le','-']),np.float32)
 name='facebook/wav2vec2-base-960h';processor=Wav2Vec2Processor.from_pretrained(name);model=Wav2Vec2ForCTC.from_pretrained(name).eval();step=model.config.inputs_to_logits_ratio/16000
 out=[]
 for region in regions:
  start,end=float(region['start']),float(region['end']);assert 0<=start<end<=len(x)/16000
  data=processor(x[round(start*16000):round(end*16000)],sampling_rate=16000,return_tensors='pt')
  with torch.inference_mode():ids=model(**data).logits.argmax(-1)[0]
  decoded=processor.tokenizer.decode(ids,output_word_offsets=True)
  out.append(dict(start=start,end=end,text=decoded.text,words=[dict(word=w['word'],start=round(start+w['start_offset']*step,3),end=round(start+w['end_offset']*step,3))for w in decoded.word_offsets]))
 dest=Path(a.output);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(dict(model=name,review_limit='Approximate recognition spans, not safe edit boundaries. Inspect phoneme context before applying cuts.',regions=out),indent=2));print(f'Wrote {len(out)} source regions to {dest}')
if __name__=='__main__':main()
