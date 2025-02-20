import pytest
import numpy as np
from bhvstats.phylo_split import PhyloSplit
from bhvstats.phylo_tree import PhyloTree
from bhvstats.project_trees import (
    projection_matrix,
    surviving_splits,
    project_tree,
    proj_trees,
)


def get_reference_tree() -> PhyloTree:
    T = PhyloTree(7)
    T.add_split([1, 2, 3], 1)
    T.add_split([4, 5, 6], 1)
    T.add_split([4, 5], 1)
    return T


def get_test_splits() -> tuple[PhyloSplit, PhyloSplit]:
    s1 = PhyloSplit([1, 3], 7)
    s2 = PhyloSplit([4, 5, 6, 7], 7)
    return s1, s2


def get_test_tree() -> PhyloTree:
    T = PhyloTree(7)
    s1, s2 = get_test_splits()
    T.add_split(s1, 1)
    T.add_split(s2, 2)
    return T


def test_proj_mat():
    T = get_reference_tree()
    N = T.get_leafcount()
    M = projection_matrix(T)

    M_real = np.eye(N + 1)
    M_real = np.delete(M_real, [4, 5], axis=1)
    assert np.array_equal(M, M_real)


def test_surviving():
    T = get_reference_tree()
    N = T.get_leafcount()

    surv = surviving_splits(T)
    surviver = PhyloSplit([1, 2, 3], N)
    print(surv[0])
    assert surv == [surviver]


def test_projection_single():
    T_ref = get_reference_tree()
    T = get_test_tree()
    surv = surviving_splits(T_ref)

    T_proj = project_tree(T_ref, T, surv)
    s_proj = T_proj.get_splits()
    s_proj_true = [
        PhyloSplit([1, 3], 7),
        PhyloSplit([4, 5, 6, 7], 7),
        PhyloSplit([1, 2, 3], 7),
    ]
    assert s_proj == s_proj_true


def test_projection_full():
    T_ref = get_reference_tree()
    T = get_test_tree()
    X = [T]

    Xproj = proj_trees(T_ref, X)
    T1 = Xproj[0][0]
    s1 = T1.get_splits()[0]
    T2 = Xproj[1][0]
    s2 = T2.get_splits()[0]

    case1 = (s1 == PhyloSplit([1, 3], 7)) and (
        s2 == PhyloSplit([4, 5, 6, 7], 7)
    )
    case2 = (s2 == PhyloSplit([1, 3], 7)) and (
        s1 == PhyloSplit([4, 5, 6, 7], 7)
    )
    assert case1 or case2
