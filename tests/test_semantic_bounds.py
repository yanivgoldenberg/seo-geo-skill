# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Attribution and required notices: see NOTICE and LICENSE.
"""Synthetic proposed-copy and bounded-file regressions; no live evidence."""
from pathlib import Path
import contextlib,copy,hashlib,importlib.util,io,json,sys,tempfile,types,unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
MODULE=next(p for p in [ROOT/'semantic_contract.py',ROOT/'gsc_site/semantic_contract.py',ROOT/'scripts/semantic_contract.py']if p.is_file())
spec=importlib.util.spec_from_file_location('bounded_semantic_fixture',MODULE);contract=importlib.util.module_from_spec(spec);spec.loader.exec_module(contract)
CAP=16*1024*1024

class SemanticBoundTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
  f=self.root/'fixture.txt';f.write_bytes(b'Synthetic evidence only.');ev={'path':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
  self.data={'method_profile':contract.PROFILE,'revision':'synthetic','inputs':{'source':'fixture'},'pages':[]}
  p={'route':'/example/','locale':'en','content_type':'SERVICE','content_sha256':'b'*64,'method':{'whole_page_review':{'source_sha256':'a'*64}},'subquestions':[{'id':'q1','semantic_journey':{'reader_task':'Read scope','destination_type':'SERVICE','offer_route':'/example/','next_action':'Review scope'}}]}
  p['semantic_checks']=[{'id':cid,'status':'PASS','reviewer':'synthetic','method':'Synthetic bounded check','findings':[],'revision':'synthetic','inputs':copy.deepcopy(self.data['inputs']),'locale':'en','source_sha256':'a'*64,'content_sha256':'b'*64,'evidence':copy.deepcopy(ev)}for cid in contract.CONTROLS]
  self.data['pages']=[p];self.data['semantic_acceptance']={'schema':'semantic-content-acceptance/1','phase':'publication','reviewer':'synthetic','findings':[],'release_checks':[{'id':rid,'status':'PASS','reviewer':'synthetic','revision':'synthetic','inputs':copy.deepcopy(self.data['inputs']),'evidence':copy.deepcopy(ev)}for rid in contract.RELEASE_STAGES]}
 def errors(self):return contract.validate_semantic(self.data,self.root,contract.evidence_problem)
 def test_valid_copy_hash(self):self.assertEqual(self.errors(),[])
 def test_missing_equal_copy_hash_cannot_pass(self):
  p=self.data['pages'][0];p.pop('content_sha256');[r.pop('content_sha256')for r in p['semantic_checks']];self.assertIn('SEMANTIC_COPY_BINDING:/example/',self.errors())
 def test_invalid_equal_copy_hash_cannot_pass(self):
  for bad in ['not-a-hash','B'*64,'b'*63,None]:
   with self.subTest(bad=bad):
    p=self.data['pages'][0];p['content_sha256']=bad
    for r in p['semantic_checks']:r['content_sha256']=bad
    self.assertIn('SEMANTIC_COPY_BINDING:/example/',self.errors())
 def stale_stat(self,path):
  original=Path.stat
  def stale(p,*args,**kwargs):
   st=original(p,*args,**kwargs)
   return types.SimpleNamespace(st_mode=st.st_mode,st_size=1)if p==path else st
  return patch.object(Path,'stat',stale)
 def test_evidence_growth_after_stat_rejects(self):
  f=self.root/'grown.txt';f.write_bytes(b' '*(CAP+1));ev={'path':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
  with self.stale_stat(f):self.assertIsNotNone(contract.evidence_problem(ev,self.root))
 def test_record_growth_after_stat_rejects(self):
  f=self.root/'grown.json';f.write_bytes(b'{}'+b' '*CAP)
  with self.stale_stat(f),patch.object(sys,'argv',['semantic_contract.py',str(f),'--evidence-root',str(self.root),'--phase','publication']),contextlib.redirect_stdout(io.StringIO())as captured:self.assertEqual(contract.main(),2)
  self.assertEqual(json.loads(captured.getvalue())['status'],'INPUT_REFUSED')

if __name__=='__main__':unittest.main()
