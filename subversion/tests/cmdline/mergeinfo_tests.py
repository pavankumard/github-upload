#!/usr/bin/env python
#
#  mergeinfo_tests.py:  testing Merge Tracking reporting
#
#  Subversion is a tool for revision control.
#  See http://subversion.tigris.org for more information.
#
# ====================================================================
# Copyright (c) 2007 CollabNet.  All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.  The terms
# are also available at http://subversion.tigris.org/license-1.html.
# If newer versions of this license are posted there, you may use a
# newer version instead, at your option.
#
######################################################################

# General modules
import shutil, sys, re, os

# Our testing module
import svntest
from svntest import wc

# (abbreviation)
Item = wc.StateItem
XFail = svntest.testcase.XFail
Skip = svntest.testcase.Skip
SkipUnless = svntest.testcase.SkipUnless

from svntest.main import SVN_PROP_MERGE_INFO
from svntest.main import server_has_mergeinfo

def adjust_error_for_server_version(expected_err):
  "Return the expected error regexp appropriate for the server version."
  if server_has_mergeinfo():
    return expected_err
  else:
    return "Retrieval of mergeinfo unsupported by '.+'"

######################################################################
# Tests
#
#   Each test must return on success or raise on failure.


#----------------------------------------------------------------------

def no_mergeinfo(sbox):
  "'mergeinfo' on a URL that lacks mergeinfo"

  sbox.build(create_wc=False)
  svntest.actions.run_and_verify_mergeinfo(adjust_error_for_server_version(""),
                                           {sbox.repo_url : {}}, sbox.repo_url)

def mergeinfo(sbox):
  "'mergeinfo' on a path with mergeinfo"

  sbox.build()
  wc_dir = sbox.wc_dir

  # Dummy up some mergeinfo.
  svntest.actions.run_and_verify_svn(None, None, [], "merge", "-c", "1",
                                     "--record-only", sbox.repo_url + "/",
                                     wc_dir)
  svntest.actions.run_and_verify_mergeinfo(adjust_error_for_server_version(""),
                                           {wc_dir : {"/" : ("r0:1", None)}},
                                           wc_dir)

def explicit_mergeinfo_source(sbox):
  "'mergeinfo' with source selection"

  sbox.build()
  wc_dir = sbox.wc_dir
  H_path = os.path.join(wc_dir, 'A', 'D', 'H')
  H2_path = os.path.join(wc_dir, 'A', 'D', 'H2')
  B_url = sbox.repo_url + '/A/B'
  G_url = sbox.repo_url + '/A/D/G'
  H2_url = sbox.repo_url + '/A/D/H2'
  
  # Make a copy, and dummy up some mergeinfo.
  mergeinfo = '/A/B:1\n/A/D/G:1\n'
  svntest.main.run_svn(None, "pset", SVN_PROP_MERGE_INFO, mergeinfo, H_path)
  svntest.main.run_svn(None, "cp", H_path, H2_path)
  svntest.main.run_svn(None, "ci", "-m", "r2", wc_dir)

  # Check using --from-source on each of our recorded merge sources.
  svntest.actions.run_and_verify_mergeinfo(adjust_error_for_server_version(""),
                                           {H_path : {'/A/B' : ("r0:1",
                                                                "r1:2")}},
                                           H_path, '--from-source', B_url)
  svntest.actions.run_and_verify_mergeinfo(adjust_error_for_server_version(""),
                                           {H_path : {'/A/D/G' : ("r0:1",
                                                                  "r1:2")}},
                                           H_path, '--from-source', G_url)

  # Now check on a source we haven't "merged" from.
  svntest.actions.run_and_verify_mergeinfo(adjust_error_for_server_version(""),
                                           {H_path : {'/A/D/H2' : (None,
                                                                   "r1:2")}},
                                           H_path, '--from-source', H2_url)
  

########################################################################
# Run the tests


# list all tests here, starting with None:
test_list = [ None,
              no_mergeinfo,
              mergeinfo,
              explicit_mergeinfo_source,
             ]

if __name__ == '__main__':
  svntest.main.run_tests(test_list)
  # NOTREACHED
