#!/usr/bin/env python3
"""Exact integer arithmetic only. External Hermite inputs are documented separately."""
import json
from pathlib import Path
E9=21870

def first_true(pred):
    lo,hi=0,1
    while not pred(hi): hi*=2
    while hi-lo>1:
        mid=(lo+hi)//2
        if pred(mid):hi=mid
        else:lo=mid
    assert not pred(hi-1) and pred(hi)
    return hi

def determinant_round(d):
    while d%4 not in (0,3):d+=1
    return d

rows={}
for name, pred in [
 ('classical_mordell', lambda d:d**63*2**90>=E9**70),
 ('neumaier_theorem_3_4',lambda d:d**9*16**10>E9**10*7**10),
 ('using_gamma9_equals2',lambda d:d**36*2**45>=E9**40),
]:
    first=first_true(pred)
    rows[name]={'first_integer':first,'first_allowed_determinant':determinant_round(first)}
assert rows['classical_mordell']['first_allowed_determinant']==24663
assert rows['neumaier_theorem_3_4']['first_allowed_determinant']==26495
assert rows['using_gamma9_equals2']['first_allowed_determinant']==27911
D=54672
assert 54675%4==3 and max(x for x in range(54675) if x%4 in (0,3))==D
bounds=[
 ('classical_mordell',lambda k:k**70<=2**90*D**63),
 ('neumaier_theorem_3_4',lambda k:k**10*7**10<16**10*D**9),
 ('using_gamma9_equals2',lambda k:k**40<=2**45*D**36),
]
for name,pred in bounds:
    last=first_true(lambda k:not pred(k))-1
    rows[name]['rank9_upper_floor']=last
    rows[name]['rank9_even_upper']=last-last%2
assert rows['classical_mordell']['rank9_even_upper']==44774
assert rows['neumaier_theorem_3_4']['rank9_even_upper']==41976
assert rows['using_gamma9_equals2']['rank9_even_upper']==40054
result={'E9':E9,'strict_counterexample_upper':D,'bounds':rows,'status':'EXACT_INTEGER_ENDPOINTS_PASS'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

# Additional structural inputs, proved in separate companion certificates:
# (1) every rank9 equality lattice is K9, which contains sqrt(3)E8;
# (2) any rank10 lattice containing sqrt(3)E8 has determinant >=54675.
# Hence a strict rank10 counterexample has shortest-dual rank9 parent det>=21872.
E=21872
structural={}
for name,pred in [
 ('classical_mordell',lambda d:d**63*2**90>=E**70),
 ('neumaier_theorem_3_4',lambda d:d**9*16**10>E**10*7**10),
 ('using_gamma9_equals2',lambda d:d**36*2**45>=E**40),
]:
 first=first_true(pred)
 structural[name]={'first_integer':first,'first_allowed_determinant':determinant_round(first)}
assert structural['classical_mordell']['first_allowed_determinant']==24664
assert structural['neumaier_theorem_3_4']['first_allowed_determinant']==26499
assert structural['using_gamma9_equals2']['first_allowed_determinant']==27915
result['with_unique_rank9_and_E8_codim2_theorems']={'rank9_parent_floor':E,'bounds':structural}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print('STRUCTURAL_REFINEMENT_EXACT_ENDPOINTS_PASS')
print(json.dumps(structural,indent=2))

# Further NEW companion input (equality/rank9_gap.py): under gamma9=2,
# the only rank9 min6 even lattice of determinant <=24444 is K9.
# A strict rank10 counterexample has no sqrt3E8, hence has parentdet>=24446.
Eg=24446
pred=lambda d:d**36*2**45>=Eg**40
ceilgap=first_true(pred)
gapbound=determinant_round(ceilgap)
assert ceilgap==31587 and gapbound==31587
# Check the gap theorem's determinant window arithmetically.
assert 2**9*24444**8<15909**9
assert 2**9*24446**8>=15909**9
result['with_rank9_gap_and_E8_codim2_theorems']={
 'rank9_parent_floor':Eg,'Hermite_input':'public gamma9=2 and Mordell',
 'first_integer':ceilgap,'first_allowed_determinant':gapbound,
 'gap_window_endpoint_check':'2^9*24444^8 <15909^9 <=2^9*24446^8'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print('RANK9_GAP_REFINEMENT_EXACT_ENDPOINTS_PASS',gapbound)

# FINAL stable gap certificate: expanded equality boundary windows allow15909;
# rank8 determinants next jump to15912. The completed scan covers D9<=24450.
Eg=24452
pred=lambda d:d**36*2**45>=Eg**40
ceilgap=first_true(pred)
gapbound=determinant_round(ceilgap)
assert ceilgap==31595 and gapbound==31595
assert 2**9*24450**8<15912**9
assert 2**9*24452**8>=15912**9
result['final_gap_refinement']={
 'rank9_parent_floor':Eg,'rank9_gap_through':24450,
 'Hermite_input':'public gamma9=2 and Mordell',
 'first_integer':ceilgap,'first_allowed_determinant':gapbound,
 'gap_window_endpoint_check':'2^9*24450^8 <15912^9 <=2^9*24452^8',
 'rank10_interval':[gapbound,54675]}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print('FINAL_STABLE_RANK9_GAP_REFINEMENT_EXACT_ENDPOINTS_PASS',gapbound)
