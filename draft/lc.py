from typing import *
import random


# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None


"""
%% Definition for a binary tree node.
%%
%% -record(tree_node, {val = 0 :: integer(),
%%                     left = null  :: 'null' | #tree_node{},
%%                     right = null :: 'null' | #tree_node{}}).

-spec is_same_tree(P :: #tree_node{} | null, Q :: #tree_node{} | null) -> boolean().
is_same_tree(#tree_node{val = V1,left=L1,right=R1}, #tree_node{val = V2,left=L2,right=R2})->
    V1 =:= V2 andalso is_same_tree(L1,L2) andalso is_same_tree(R1,R2);
     
is_same_tree(A,B)->A=:=B;
"""