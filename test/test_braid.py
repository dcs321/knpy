import sys
import os

import pytest
import numpy as np
#IMPORTANT: knpy should be installed first
from knpy import Braid
from knpy import IllegalTransformationException, InvalidBraidException, IndexOutOfRangeException

class TestBraidClassBraidRelationsInit:
    def test_init_empty(self):
        braid = Braid([])
        assert braid._n == 1
        assert braid._braid.shape[0] == 0
    
    def test_init(self):
        braid = Braid([1,2,3])
        assert braid._n == 4
        assert braid._braid.shape[0] == 3
    
    def test_init_from_database(self):
        braid = Braid("3_1")
        assert braid._n == 2
        assert braid._braid.shape[0] == 3
        assert np.all(braid._braid == np.array([1,1,1]))
    
    def test_values(self):
        braid = Braid([1,2,3])
        assert braid._n == braid.values()[0]
        assert braid._braid.shape[0] == braid.values()[1].shape[0]

    def test_init_exception(self):
        with pytest.raises(InvalidBraidException):
            braid = Braid([1,0,-1,2,3])


class TestBraidClassBraidRelationsStabilizationDestabilization:
    def test_is_destabilization_performable_empty(self):
        braid = Braid([])
        assert not braid.is_destabilization_performable()
    
    def test_is_destabilization_performable_true1(self):
        braid = Braid([1, -2, 3, 4])
        assert braid.is_destabilization_performable()
    
    def test_is_destabilization_performable_true2(self):
        braid = Braid([1, -2, -3])
        assert braid.is_destabilization_performable()
    
    def test_is_destabilization_performable_false1(self):
        braid = Braid([-3, 1, -2, -3])
        assert not braid.is_destabilization_performable()

    def test_is_destabilization_performable_false2(self):
        braid = Braid([ 1, -2, -3, 1])
        assert not braid.is_destabilization_performable()

    def test_is_destabilization_performable_false3(self):
        braid = Braid([ 1, -2, -3, 1, 4, -4])
        assert not braid.is_destabilization_performable()

    def test_stabilization_empty(self):
        braid = Braid([])
        braid.stabilization()
        assert braid.values()[0] == 2
        assert braid.values()[1][-1] == 1
        assert len(braid.values()[1]) == 1

    def test_stabilization(self):
        braid = Braid([1, -2, 3])
        braid.stabilization()
        assert braid.values()[0] == 5
        assert braid.values()[1][-1] == 4
        assert len(braid.values()[1]) == 4

    def test_stabilization_inverse(self):
        braid = Braid([1, -2, 3])
        braid.stabilization(inverse=True)
        assert braid.values()[0] == 5
        assert braid.values()[1][-1] == -4
        assert len(braid.values()[1]) == 4

    def test_destabilization_empty(self):
        braid = Braid([])
        with pytest.raises(IllegalTransformationException):
            braid.destabilization() 


    def test_destabilization(self):
        braid = Braid([1, -2, 3])
        braid.destabilization()
        assert braid.values()[0] == 3
        assert len(braid.values()[1]) == 2
    
    def test_destabilization_inverse(self):
        braid = Braid([1, -2, -3])
        braid.destabilization()
        assert braid.values()[0] == 3
        assert len(braid.values()[1]) == 2

    def test_destabilization_exception(self):
        braid = Braid([-3 ,1, -2, 3])
        with pytest.raises(IllegalTransformationException):
            braid.destabilization() 

class TestBraidClassBraidRelationsConjugation:
    def test_is_conjugation_performable_empty(self):
        braid = Braid([])
        assert not braid.is_conjugation_performable(index=1)

    def test_is_conjugation_performable_true1(self):
        braid = Braid([1, -2, 3, 4])
        assert braid.is_conjugation_performable(index=1)
    
    def test_is_conjugation_performable_true2(self):
        braid = Braid([1, -2, 3, 4])
        assert braid.is_conjugation_performable(index=-2)

    def test_is_conjugation_performable_false1(self):
        braid = Braid([1, -2, 3, 4])
        assert not braid.is_conjugation_performable(index=0)
    
    def test_is_conjugation_performable_false2(self):
        braid = Braid([1, -2, 3, 4])
        assert not braid.is_conjugation_performable(index=5)

    def test_is_conjugation_performable_false3(self):
        braid = Braid([1, -2, 3, 4])
        assert not braid.is_conjugation_performable(index=5)
    
    def test_conjugation_empty(self):
        braid = Braid([])
        with pytest.raises(IllegalTransformationException):
            braid.conjugation(index=0) 

    def test_conjugation(self):
        braid = Braid([-1, -2, 3, 4])
        braid.conjugation(index=1)
        values = braid.values()[1]
        assert values[0] == 1 and values[-1] == -1
    
    def test_conjugation_inverse(self):
        braid = Braid([-1, -2, 3, 4])
        braid.conjugation(index=-4)
        values = braid.values()[1]
        assert values[0] == -4 and values[-1] == 4

    def test_conjugation_exception(self):
        braid = Braid([-1, -2, 3, 4])
        with pytest.raises(IllegalTransformationException):
            braid.conjugation(index=5)

class TestBraidClassBraidRelationsBraidRelation1:
    
    def test_is_braid_relation1_performable_empty(self):
        braid = Braid([])
        assert not braid.is_braid_relation1_performable(index = 0)
    
    def test_is_braid_relation1_performable_only_true(self):
        braid = Braid([1,2,1])
        assert braid.is_braid_relation1_performable(index = 0)

    def test_is_braid_relation1_performable_middle_true(self):
        braid = Braid([9,3,4,3,3,5])
        assert braid.is_braid_relation1_performable(index = 1)
    
    def test_is_braid_relation1_performable_negatives_true(self):
        braid = Braid([1,-2,-1,3,3,5])
        assert braid.is_braid_relation1_performable(index = 0)
    
    def test_is_braid_relation1_performable_end_true(self):
        braid = Braid([9,3,3,5,4,3,4])
        assert braid.is_braid_relation1_performable(index = 4)
    
    def test_is_braid_relation1_performable_opposite_true(self):
        braid = Braid([9,3,3,-5,4,-5,1,2])
        assert braid.is_braid_relation1_performable(index = 3)

    def test_is_braid_relation1_performable_beginning_true(self):
        braid = Braid([-5,4,-5,1,2])
        assert braid.is_braid_relation1_performable(index = 0)

    def test_is_braid_relation1_performable_multiple_true(self):
        braid = Braid([-5,4,-5,1,2,1,-2,-1])
        assert braid.is_braid_relation1_performable(index = 0)
        assert braid.is_braid_relation1_performable(index = 3) 
        assert braid.is_braid_relation1_performable(index = 4)
        assert braid.is_braid_relation1_performable(index = 4)

    def test_is_braid_relation1_performable_false1(self):
        braid = Braid([9,3,3,1,1,1])
        assert not braid.is_braid_relation1_performable(index = 3)

    
    def test_is_braid_relation1_performable_false2(self):
        braid = Braid([9,3,3,5,3,1])
        assert not braid.is_braid_relation1_performable(index = 0)
    
    def test_is_braid_relation1_performable_indices_empty(self):
        braid = Braid([])
        assert braid.braid_relation1_performable_indices().shape[0] == 0

    def test_braid_relation1_preformable_indices_empty(self):
        braid = Braid([9,3,3,1,1,1])
        assert braid.braid_relation1_performable_indices().shape[0] == 0    
    
    def test_braid_relation1_preformable_indices_one(self):
        braid = Braid([1,2,1])
        performable_indices = braid.braid_relation1_performable_indices()
        assert performable_indices.shape[0] == 1
        assert performable_indices[0] == 0

    def test_braid_relation1_preformable_indices_multiple(self):
        braid = Braid([-5,4,-5,1,2,1,-2,-1])
        performable_indices = braid.braid_relation1_performable_indices()
        assert performable_indices.shape[0] == 4
        assert performable_indices[0] == 0 and performable_indices[1] == 3

    def test_braid_relation1_empty(self):
        braid = Braid([])
        with pytest.raises(IllegalTransformationException):
            braid.braid_relation1(index=0)


class TestBraidClassBraidRelationsBraidRelation2:
    
    def test_is_braid_relation2_performable_empty(self):
        braid = Braid([])
        assert not braid.is_braid_relation2_performable(index = 0)
    
    def test_is_braid_relation2_performable_indices_empty(self):
        braid = Braid([])
        assert braid.braid_relation2_performable_indices().shape[0] == 0
    
    def test_braid_relation2_empty(self):
        braid = Braid([])
        with pytest.raises(IllegalTransformationException):
            braid.braid_relation2(index=0)


class TestBraidClassBraidRelationsShifts:
    
    def test_shift_left_empty(self):
        braid = Braid([])
        braid.shift_left()
        assert braid.values()[1].shape[0] == 0
    
    def test_shift_right_empty(self):
        braid = Braid([])
        braid.shift_right()
        assert braid.values()[1].shape[0] == 0
    
    def test_shift_left_with_amount_empty(self):
        braid = Braid([])
        braid.shift_left_with_amount(amount=2)
        assert braid.values()[1].shape[0] == 0
    
    def test_shift_right_with_amount_empty(self):
        braid = Braid([])
        braid.shift_right_with_amount(amount=2)
        assert braid.values()[1].shape[0] == 0


class TestBraidClassBraidRelationsRemoveSigmaAndInverse:
    
    def test_is_remove_sigma_inverse_pair_performable_empty(self):
        braid = Braid([])
        assert not braid.is_remove_sigma_inverse_pair_performable(index=0)
    
    def test_remove_sigma_inverse_pair_performable_indices_empty(self):
        braid = Braid([])
        assert braid.remove_sigma_inverse_pair_performable_indices().shape[0] == 0
    
    def test_remove_sigma_inverse_pair_empty(self):
        braid = Braid([])
        with pytest.raises(IllegalTransformationException):
            braid.remove_sigma_inverse_pair(index=0)