import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'app'))
from evidence import lesion_overlay,LESION_PALETTE

def test_zero_proxy_preserves_original_photo():
 base=np.full((8,8,3),(70,40,25),dtype=np.uint8)
 for palette in LESION_PALETTE.values():
  np.testing.assert_array_equal(lesion_overlay(base,np.zeros((8,8)),palette['rgb']),base)

def test_same_proxy_has_distinct_channel_colours_without_changing_values():
 base=np.zeros((8,8,3),dtype=np.uint8);heat=np.full((8,8),.75,dtype=np.float32);original=heat.copy()
 colours={tuple(lesion_overlay(base,heat,p['rgb'])[0,0]) for p in LESION_PALETTE.values()}
 assert len(colours)==5
 np.testing.assert_array_equal(heat,original)
 assert len({p['color'] for p in LESION_PALETTE.values()})==5

def test_invalid_map_values_remain_bounded():
 base=np.full((2,2,3),100,np.uint8);heat=np.array([[np.nan,np.inf],[-1,2]])
 result=lesion_overlay(base,heat,(204,121,167));assert result.dtype==np.uint8
 np.testing.assert_array_equal(result[0,0],base[0,0]);np.testing.assert_array_equal(result[1,0],base[1,0])
