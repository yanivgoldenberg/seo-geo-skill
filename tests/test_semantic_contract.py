# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Attribution and required notices: see NOTICE and LICENSE.
"""Synthetic tests: local receipt integrity only, never live observations."""
import copy
import hashlib
import tempfile
import unittest
from pathlib import Path
import importlib.util
SPEC=importlib.util.spec_from_file_location('semantic_contract',Path(__file__).resolve().parents[1]/'scripts/semantic_contract.py')
contract=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(contract)
IDS=('buyer_decision','claim_evidence_status','original_useful_artifact','locale_type_routing','identity_offer_faq_parity','metadata_date_parity','contextual_link_journeys','derived_content_freshness','reader_task_review','measurement_boundaries')
RELEASE=('source_review','local_checks','ci','preview','canonical_readback','production','public_readback')



class SemanticContractTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
  artifact=self.root/'synthetic.txt';artifact.write_text('Synthetic fixture, not real source or business evidence.',encoding='utf-8')
  evidence={'path':'synthetic.txt','sha256':hashlib.sha256(artifact.read_bytes()).hexdigest()}
  self.map={'method_profile':'composed-content/2','revision':'synthetic-revision','inputs':{'source':'synthetic-source'},'pages':[]}
  page={'route':'/example/','locale':'en','content_type':'SERVICE','content_sha256':'b'*64,'method':{'whole_page_review':{'source_sha256':'a'*64}},'subquestions':[{'id':'q1','semantic_journey':{'reader_task':'Choose a useful next step','destination_type':'SERVICE','offer_route':'/example/','next_action':'Read the scope'}}]}
  page['semantic_checks']=[{'id':cid,'status':'PASS','reviewer':'synthetic-reviewer','method':'Synthetic current-scope review','findings':[],'revision':self.map['revision'],'inputs':copy.deepcopy(self.map['inputs']),'locale':'en','source_sha256':'a'*64,'content_sha256':'b'*64,'evidence':copy.deepcopy(evidence)}for cid in IDS]
  self.map['pages']=[page]
  self.map['semantic_acceptance']={'schema':'semantic-content-acceptance/1','phase':'publication','reviewer':'synthetic-reviewer','findings':[],'release_checks':[{'id':rid,'status':'PASS','reviewer':'synthetic-reviewer','revision':self.map['revision'],'inputs':copy.deepcopy(self.map['inputs']),'evidence':copy.deepcopy(evidence)}for rid in RELEASE]}
 def errors(self):return contract.validate_semantic(self.map,self.root,contract.evidence_problem,expected_phase='publication')
 def test_complete_synthetic_contract(self):self.assertEqual(self.errors(),[])
 def test_each_missing_control_is_rejected(self):
  for index in range(len(IDS)):
   data=copy.deepcopy(self.map);data['pages'][0]['semantic_checks'].pop(index);self.assertIn('SEMANTIC_CONTROL_SET:/example/',contract.validate_semantic(data,self.root,contract.evidence_problem))
 def test_pending_cannot_fill_publication_slot(self):
  self.map['semantic_acceptance']['release_checks'][-1]={'id':'public_readback','status':'PENDING','reason':'Not observed'};self.assertIn('SEMANTIC_RELEASE_NOT_PASS:public_readback',self.errors())
 def test_unknown_and_na_are_not_blanket_exemptions(self):
  for status in ['UNKNOWN','NOT_APPLICABLE','PENDING']:
   self.map['pages'][0]['semantic_checks'][0]['status']=status;self.assertIn('SEMANTIC_CONTROL_NOT_PASS:/example/:buyer_decision',self.errors())
 def test_changed_source_copy_locale_and_receipt_are_rejected(self):
  for key,value in [('source_sha256','c'*64),('content_sha256','c'*64),('locale','he')]:
   data=copy.deepcopy(self.map);data['pages'][0]['semantic_checks'][0][key]=value;self.assertIn('SEMANTIC_CONTROL_BINDING:/example/:buyer_decision',contract.validate_semantic(data,self.root,contract.evidence_problem))
  (self.root/'synthetic.txt').write_text('Changed bytes');self.assertTrue(self.errors())
 def test_malformed_whole_review_fails_without_crash(self):
  self.map['pages'][0]['method']['whole_page_review']=None;self.assertIn('SEMANTIC_SOURCE_BINDING:/example/',self.errors())
 def test_missing_pages_and_questions_cannot_pass(self):
  self.map['pages'][0]['subquestions']=[];self.assertIn('SEMANTIC_QUESTION_SET:/example/',self.errors());self.map['pages']=[];self.assertIn('SEMANTIC_PAGE_SET',self.errors())
 def test_evidence_path_guard_preserved(self):
  for name in ['../outside.txt','.hidden.txt','C:/private/example.txt']:
   self.assertEqual(contract.evidence_problem({'path':name,'sha256':'a'*64},self.root),'EVIDENCE_PATH')

def test_generic_shared_examples_do_not_expose_private_values():
 import re
 patterns=[r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',r'(?i)(?:api[_-]?key|secret|password)\s*[:=]\s*[^\s]+',r'(?i)[A-Z]:[/\\](?:Users|private)[/\\]']
 def sensitive(value):return any(re.search(pattern,value)for pattern in patterns)
 assert sensitive('person@contact.invalid')
 assert sensitive('api_key=synthetic_example')
 assert sensitive('C:/private/example.txt')
 assert not sensitive('https://example.com/guide/')
 root=Path(__file__).resolve().parents[1]
 for rel in ['docs/SEMANTIC_ACCEPTANCE.md','scripts/semantic_contract.py']:
  assert not sensitive((root/rel).read_text(encoding='utf-8')),rel

if __name__=='__main__':unittest.main()
