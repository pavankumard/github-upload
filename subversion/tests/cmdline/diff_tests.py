import sys, re, os, time, shutil
from svntest import err
def is_absolute_url(target):
  return (target.startswith('file://')
          or target.startswith('http://')
          or target.startswith('https://')
          or target.startswith('svn://')
          or target.startswith('svn+ssh://'))

    if not is_absolute_url(src_label):
      src_label = '.../' + src_label
    src_label = '\t(' + src_label + ')'
    if not is_absolute_url(dst_label):
      dst_label = '.../' + dst_label
    dst_label = '\t(' + dst_label + ')'
                         cp=False, mv=False, copyfrom_path=None):
    output = [
      "Index: " + path_as_shown + "\n",
      "===================================================================\n",
    ]
    output = [
      "Index: " + path_as_shown + "\n",
      "===================================================================\n",
    ]
    output = [
      "Index: " + path_as_shown + "\n",
      "===================================================================\n",
      "copy from " + copyfrom_path + "\n",
    ]
    return [
      "Index: " + path_as_shown + "\n",
      "===================================================================\n",
    ]
    output = [
      "Index: " + path_as_shown + "\n",
      "===================================================================\n",
    ]
  
     PVAL1, new value PVAL2.  PVAL is a single string with no embedded
     newlines.  Return the result as a list of newline-terminated strings."""
      print('Sought: %s' % excluded)
      print('Found:  %s' % line)
    None, 'diff', '-r', '1', os.path.join(wc_dir, 'A', 'D'))
    None, 'diff', '-r', '1', '-N', os.path.join(wc_dir, 'A', 'D'))
    None, 'diff', '-r', '1', os.path.join(wc_dir, 'A', 'D', 'G'))
  svntest.main.file_append(os.path.join(wc_dir, 'A', 'D', 'foo'), "a new file")
    1, 'diff', os.path.join(wc_dir, 'A', 'D', 'foo'))
  theta_path = os.path.join(wc_dir, 'A', 'theta')
  mu_path = os.path.join(sbox.wc_dir, 'A', 'mu')
  svntest.actions.run_and_verify_svn(None, svntest.verify.AnyOutput, [],
  iota_path = os.path.join(sbox.wc_dir, 'iota')
  newfile_path = os.path.join(sbox.wc_dir, 'A', 'D', 'newfile')
  mu_path = os.path.join(sbox.wc_dir, 'A', 'mu')
  A_path = os.path.join(sbox.wc_dir, 'A')
  mu_path = os.path.join(sbox.wc_dir, 'A', 'mu')
  A_alpha = os.path.join(sbox.wc_dir, 'A', 'B', 'E', 'alpha')
  A2_alpha = os.path.join(sbox.wc_dir, 'A2', 'B', 'E', 'alpha')
  A_alpha = os.path.join(sbox.wc_dir, 'A', 'B', 'E', 'alpha')
  A2_alpha = os.path.join(sbox.wc_dir, 'A2', 'B', 'E', 'alpha')
  A_path = os.path.join(sbox.wc_dir, 'A')
  iota_path = os.path.join(sbox.wc_dir, 'iota')
  iota_copy_path = os.path.join(sbox.wc_dir, 'A', 'iota')
  iota_path = os.path.join(sbox.wc_dir, 'iota')
  prefix_path = os.path.join(sbox.wc_dir, 'prefix_mydir')
  other_prefix_path = os.path.join(sbox.wc_dir, 'prefix_other')
    print("src is '%s' instead of '%s' and dest is '%s' instead of '%s'" %
  iota_path = os.path.join(sbox.wc_dir, 'iota')
  iota_path = os.path.join(wc_dir, 'iota')
  svntest.main.run_svn(None,
  # Check a repos->wc diff

  add_diff = \
    make_diff_prop_header("A") + \
    make_diff_prop_added("dirprop", "r2value") + \
    make_diff_prop_header("iota") + \
    make_diff_prop_added("fileprop", "r2value")

  del_diff = \
    make_diff_prop_header("A") + \
    make_diff_prop_deleted("dirprop", "r2value") + \
    make_diff_prop_header("iota") + \
    make_diff_prop_deleted("fileprop", "r2value")


  expected_output_r1_r2 = list(make_diff_header('A', 'revision 1', 'revision 2')
                               + add_diff[:6]
                               + make_diff_header('iota', 'revision 1',
                                                   'revision 2')
                               + add_diff[7:])

  expected_output_r2_r1 = list(make_diff_header('A', 'revision 2',
                                                'revision 1')
                               + del_diff[:6]
                               + make_diff_header('iota', 'revision 2',
                                                  'revision 1')
                               + del_diff[7:])

  expected_output_r1 = list(make_diff_header('A', 'revision 1',
                                             'working copy')
                            + add_diff[:6]
                            + make_diff_header('iota', 'revision 1',
                                               'working copy')
                            + add_diff[7:])
  expected_output_base_r1 = list(make_diff_header('A', 'working copy',
                                                  'revision 1')
                                 + del_diff[:6]
                                 + make_diff_header('iota', 'working copy',
                                                    'revision 1')
                                 + del_diff[7:])
  "@@ -1 +1,2 @@\n",
  " xxx\n",
  "+yyy\n"
  expected_output_base_r2 = make_diff_header("foo", "working copy",
  "@@ -1,2 +1 @@\n",
  " xxx\n",
  "-yyy\n"
  svntest.actions.run_and_verify_svn(None, None, [],
                                     'propset', 'svn:mime-type',
  diff_X_r1_base = make_diff_header("X", "revision 1",
  diff_X_base_r3 = make_diff_header("X", "working copy",
                                                "revision 2") + [
  # Get the differences between a deep newly added dir Issue(4421)
  expected_diff = svntest.wc.State(wc_dir, {
    'Q/R'         : Item(status='A '),
    'Q/R/newfile' : Item(status='A '),
    })
  expected_reverse_diff = svntest.wc.State(wc_dir, {
    'Q/R'         : Item(status='D '),
    'Q/R/newfile' : Item(status='D '),
    })
  svntest.actions.run_and_verify_diff_summarize(expected_diff,
                                                p('Q/R'), '-c3')
  svntest.actions.run_and_verify_diff_summarize(expected_reverse_diff,
                                                p('Q/R'), '-c-3')

  svntest.main.file_write(os.path.join(sbox.wc_dir, 'A', 'mu'),
  C_path = os.path.join(wc_dir, "A", "C")
  D_path = os.path.join(wc_dir, "A", "D")
  diff = make_diff_prop_header(".") + \
         make_diff_prop_added("foo1", "bar1") + \
         make_diff_prop_header("iota") + \
         make_diff_prop_added("foo2", "bar2") + \
         make_diff_prop_header("A") + \
         make_diff_prop_added("foo3", "bar3") + \
         make_diff_prop_header("A/B") + \
         make_diff_prop_added("foo4", "bar4")

  dot_header = make_diff_header(".", "revision 1", "working copy")
  iota_header = make_diff_header('iota', "revision 1", "working copy")
  A_header = make_diff_header('A', "revision 1", "working copy")
  B_header = make_diff_header(B_path, "revision 1", "working copy")

  expected_empty = svntest.verify.UnorderedOutput(dot_header + diff[:7])
  expected_files = svntest.verify.UnorderedOutput(dot_header + diff[:7]
                                                  + iota_header + diff[8:14])
  expected_immediates = svntest.verify.UnorderedOutput(dot_header + diff[:7]
                                                       + iota_header
                                                       + diff[8:14]
                                                       + A_header + diff[15:21])
  expected_infinity = svntest.verify.UnorderedOutput(dot_header + diff[:7]
                                                       + iota_header
                                                       + diff[8:14]
                                                       + A_header + diff[15:21]
                                                       + B_header + diff[22:])

  os.chdir(sbox.wc_dir)

  svntest.actions.run_and_verify_svn(None, None, [],
                                     'propset',
                                     'foo1', 'bar1', '.')
  svntest.actions.run_and_verify_svn(None, None, [],
                                     'propset',
                                     'foo2', 'bar2', 'iota')
  svntest.actions.run_and_verify_svn(None, None, [],
                                     'propset',
                                     'foo3', 'bar3', 'A')
  svntest.actions.run_and_verify_svn(None, None, [],
                                     'propset',
                                     'foo4', 'bar4', os.path.join('A', 'B'))
  svntest.actions.run_and_verify_svn(None, expected_empty, [],
                                     'diff', '--depth', 'empty')
  svntest.actions.run_and_verify_svn(None, expected_files, [],
                                     'diff', '--depth', 'files')
  svntest.actions.run_and_verify_svn(None, expected_immediates, [],
                                     'diff', '--depth', 'immediates')
  svntest.actions.run_and_verify_svn(None, expected_infinity, [],
                                     'diff', '--depth', 'infinity')
  dot_header = make_diff_header(".", "revision 1", "revision 2")
  iota_header = make_diff_header('iota', "revision 1", "revision 2")
  A_header = make_diff_header('A', "revision 1", "revision 2")
  B_header = make_diff_header(B_path, "revision 1", "revision 2")

  expected_empty = svntest.verify.UnorderedOutput(dot_header + diff[:7])
  expected_files = svntest.verify.UnorderedOutput(dot_header + diff[:7]
                                                  + iota_header + diff[8:14])
  expected_immediates = svntest.verify.UnorderedOutput(dot_header + diff[:7]
                                                       + iota_header
                                                       + diff[8:14]
                                                       + A_header + diff[15:21])
  expected_infinity = svntest.verify.UnorderedOutput(dot_header + diff[:6]
                                                       + iota_header
                                                       + diff[8:14]
                                                       + A_header + diff[15:21]
                                                       + B_header + diff[22:])

  svntest.actions.run_and_verify_svn(None, expected_empty, [],
                                     'diff', '-c2', '--depth', 'empty')
  svntest.actions.run_and_verify_svn(None, expected_files, [],
                                     'diff', '-c2', '--depth', 'files')
  svntest.actions.run_and_verify_svn(None, expected_immediates, [],
                                     'diff', '-c2', '--depth', 'immediates')
  svntest.actions.run_and_verify_svn(None, expected_infinity, [],
                                     'diff', '-c2', '--depth', 'infinity')

  diff_wc_repos = \
    make_diff_header("A/B", "revision 2", "working copy") + \
    make_diff_prop_header("A/B") + \
    make_diff_prop_modified("foo4", "bar4", "baz4") + \
    make_diff_header("A", "revision 2", "working copy") + \
    make_diff_prop_header("A") + \
    make_diff_prop_modified("foo3", "bar3", "baz3") + \
    make_diff_header("A/mu", "revision 1", "working copy") + [
    "@@ -1 +1,2 @@\n",
    " This is the file 'mu'.\n",
    "+new text\n",
    ] + make_diff_header("iota", "revision 2", "working copy") + [
    "@@ -1 +1,2 @@\n",
    " This is the file 'iota'.\n",
    "+new text\n",
    ] + make_diff_prop_header("iota") + \
    make_diff_prop_modified("foo2", "bar2", "baz2") + \
    make_diff_header(".", "revision 2", "working copy") + \
    make_diff_prop_header(".") + \
    make_diff_prop_modified("foo1", "bar1", "baz1")

  expected_empty = svntest.verify.UnorderedOutput(diff_wc_repos[49:])
  expected_files = svntest.verify.UnorderedOutput(diff_wc_repos[33:])
  expected_immediates = svntest.verify.UnorderedOutput(diff_wc_repos[13:26]
                                                       +diff_wc_repos[33:])
  expected_infinity = svntest.verify.UnorderedOutput(diff_wc_repos[:])
  svntest.actions.run_and_verify_svn(None, None, [],
                                     'propset',
                                     'foo1', 'baz1', '.')
  svntest.actions.run_and_verify_svn(None, None, [],
                                     'propset',
                                     'foo2', 'baz2', 'iota')
  svntest.actions.run_and_verify_svn(None, None, [],
                                     'propset',
                                     'foo3', 'baz3', 'A')
  svntest.actions.run_and_verify_svn(None, None, [],
                                     'propset',
                                     'foo4', 'baz4', os.path.join('A', 'B'))
  svntest.actions.run_and_verify_svn(None, expected_empty, [],
                                     'diff', '-rHEAD', '--depth', 'empty')
  svntest.actions.run_and_verify_svn(None, expected_files, [],
                                     'diff', '-rHEAD', '--depth', 'files')
  svntest.actions.run_and_verify_svn(None, expected_immediates, [],
                                     'diff', '-rHEAD', '--depth', 'immediates')
  svntest.actions.run_and_verify_svn(None, expected_infinity, [],
                                     'diff', '-rHEAD', '--depth', 'infinity')
  svntest.main.file_append(os.path.join(wc_dir, "A", "mu"), "New mu content")
                       os.path.join(wc_dir, 'iota'))
  tau_path = os.path.join(wc_dir, "A", "D", "G", "tau")
  newfile_path = os.path.join(wc_dir, 'newfile')
  svntest.main.run_svn(None, "mkdir", os.path.join(wc_dir, 'newdir'))
  # 3) Test working copy summarize
  svntest.actions.run_and_verify_diff_summarize_xml(
    ".*Summarizing diff can only compare repository to repository",
    None, wc_dir, None, None, wc_dir)

  paths = ['iota',]
  items = ['none',]
  kinds = ['file',]
  props = ['modified',]
    [], wc_dir, paths, items, props, kinds, '-c2',
    os.path.join(wc_dir, 'iota'))
  paths = ['A/mu', 'iota', 'A/D/G/tau', 'newfile', 'A/B/lambda',
           'newdir',]
  items = ['modified', 'none', 'modified', 'added', 'deleted', 'added',]
  kinds = ['file','file','file','file','file', 'dir',]
  props = ['none', 'modified', 'modified', 'none', 'none', 'none',]

  paths = ['A/mu', 'iota', 'A/D/G/tau', 'newfile', 'A/B/lambda',
           'newdir',]
  items = ['modified', 'none', 'modified', 'added', 'deleted', 'added',]
  kinds = ['file','file','file','file','file', 'dir',]
  props = ['none', 'modified', 'modified', 'none', 'none', 'none',]

  iota_path = os.path.join(sbox.wc_dir, 'iota')
@XFail()
  make_file_edit_del_add(A);
  make_file_edit_del_add(A2);
  iota_path = os.path.join(wc_dir, 'iota')
  mu_path = os.path.join(wc_dir, 'A', 'mu')
  new_path = os.path.join(wc_dir, 'new')
  lambda_path = os.path.join(wc_dir, 'A', 'B', 'lambda')
  lambda_copied_path = os.path.join(wc_dir, 'A', 'B', 'lambda_copied')
  alpha_path = os.path.join(wc_dir, 'A', 'B', 'E', 'alpha')
  alpha_copied_path = os.path.join(wc_dir, 'A', 'B', 'E', 'alpha_copied')
  expected_output = make_git_diff_header(lambda_copied_path,
                                         copyfrom_path="A/B/lambda", cp=True,
  ] + make_git_diff_header(alpha_copied_path, "A/B/E/alpha_copied",
                         "revision 0", "working copy",
                         copyfrom_path="A/B/E/alpha", cp=True,
                         text_changes=True) + [
    " This is the file 'alpha'.\n",
    "+This is a copy of 'alpha'.\n",
  ] +  make_git_diff_header(iota_path, "iota", "revision 1",
                            "working copy") + [
    "@@ -1 +1,2 @@\n",
    " This is the file 'iota'.\n",
    "+Changed 'iota'.\n",
  expected = svntest.verify.UnorderedOutput(expected_output)
                           copyfrom_path="A/D/G/pi", text_changes=False) \
                         copyfrom_path="A/D/G/rho", text_changes=False) \
                         copyfrom_path="A/D/G/tau", text_changes=False)
  expected = svntest.verify.UnorderedOutput(expected_output)
  iota_path = os.path.join(wc_dir, 'iota')
  mu_path = os.path.join(wc_dir, 'A', 'mu')
  new_path = os.path.join(wc_dir, 'new')
  iota_path = os.path.join(wc_dir, 'iota')
  mu_path = os.path.join(wc_dir, 'A', 'mu')
  new_path = os.path.join(wc_dir, 'new')
  iota_path = os.path.join(wc_dir, 'iota')
  iota_path = os.path.join(wc_dir, 'iota')
  iota_path = os.path.join(wc_dir, 'iota')
  new_path = os.path.join(wc_dir, 'new')
  iota_path = os.path.join(wc_dir, 'iota')
  new_path = os.path.join(wc_dir, 'new')
                                         "revision 1", "working copy",
  svntest.main.run_svn(None, 'ps', 'a','b', wc_dir)
  expected_output = make_git_diff_header(".", "", "revision 1",
                    make_diff_prop_added("a", "b")
  A_path = os.path.join(wc_dir, 'A')
  B_abs_path = os.path.abspath(os.path.join(wc_dir, 'A', 'B'))
@Issue(4460)
def diff_repo_wc_file_props(sbox):
  "diff repo to wc file target with props"
  iota = sbox.ospath('iota')
  # add a mime-type and a line to iota to test the binary check
  sbox.simple_propset('svn:mime-type', 'text/plain', 'iota')
  sbox.simple_append('iota','second line\n')
  # test that we get the line and the property add
  expected_output = make_diff_header(iota, 'revision 1', 'working copy') + \
                    [ '@@ -1 +1,2 @@\n',
                      " This is the file 'iota'.\n",
                      "+second line\n", ] + \
                    make_diff_prop_header(iota) + \
                    make_diff_prop_added('svn:mime-type', 'text/plain')
                                     'diff', '-r1', iota)

  # reverse the diff, should get a property delete and line delete
  # skip actually testing the output since apparently 1.7 is busted
  # this isn't related to issue #4460, older versions of 1.7 had the issue
  # as well
  #expected_output = make_diff_header(iota, 'working copy', 'revision 1') + \
  #                  [ '@@ -1,2 +1 @@\n',
  #                    " This is the file 'iota'.\n",
  #                    "-second line\n", ] + \
  #                  make_diff_prop_header(iota) + \
  #                  make_diff_prop_deleted('svn:mime-type', 'text/plain')
  expected_output = None
                                     'diff', '--old', iota,
                                     '--new', iota + '@1')

  # copy iota to test with --show-copies as adds
  sbox.simple_copy('iota', 'iota_copy')
  iota_copy = sbox.ospath('iota_copy')

  # test that we get all lines as added and the property added
  # TODO: We only test that this test doesn't error out because of Issue #4464
  # if and when that issue is fixed this test should check output
  svntest.actions.run_and_verify_svn(None, None, [], 'diff',
                                     '--show-copies-as-adds', '-r1', iota_copy)

  # reverse the diff, should get all lines as a delete and no property
  # TODO: We only test that this test doesn't error out because of Issue #4464
  # if and when that issue is fixed this test should check output
  svntest.actions.run_and_verify_svn(None, None, [], 'diff',
                                     '--old', iota_copy,
                                     '--new', iota + '@1')

  # revert and commit with the eol-style of LF and then update so
  # that we can see a change on either windows or *nix.
  sbox.simple_revert('iota', 'iota_copy')
  sbox.simple_propset('svn:eol-style', 'LF', 'iota')
  sbox.simple_commit() #r2
  # now that we have a LF file on disk switch to CRLF
  sbox.simple_propset('svn:eol-style', 'CRLF', 'iota')

  # test that not only the property but also the file changes
  # i.e. that the line endings substitution works
  if svntest.main.is_os_windows():
    # test suite normalizes crlf output into just lf on Windows.
    # so we have to assume it worked because there is an add and
    # remove line with the same content.  Fortunately, it does't
    # do this on *nix so we can be pretty sure that it works right.
    # TODO: Provide a way to handle this better
    crlf = '\n'
  else:
    crlf = '\r\n'
  expected_output = make_diff_header(iota, 'revision 1', 'working copy') + \
                    [ '@@ -1 +1 @@\n',
                      "-This is the file 'iota'.\n",
                      "+This is the file 'iota'." + crlf ] + \
                    make_diff_prop_header(iota) + \
                    make_diff_prop_added('svn:eol-style', 'CRLF')
  svntest.actions.run_and_verify_svn(None, expected_output, [],
                                     'diff', '-r1', iota)


@Issue(4460)
def diff_repo_repo_added_file_mime_type(sbox):
    "diff repo to repo added file with mime-type"
    sbox.build()
    wc_dir = sbox.wc_dir
    newfile = sbox.ospath('newfile')

    # add a file with a mime-type
    sbox.simple_append('newfile', "This is the file 'newfile'.\n")
    sbox.simple_add('newfile')
    sbox.simple_propset('svn:mime-type', 'text/plain', 'newfile')
    sbox.simple_commit() # r2

    # try to diff across the addition
    expected_output = make_diff_header(newfile, 'revision 1', 'revision 2') + \
                      [ '@@ -0,0 +1 @@\n',
                        "+This is the file 'newfile'.\n" ] + \
                      make_diff_prop_header(newfile) + \
                      make_diff_prop_added('svn:mime-type', 'text/plain')

    svntest.actions.run_and_verify_svn(None, expected_output, [], 'diff',
                                       '-r1:2', newfile)

    # reverse the diff to diff across a deletion
    # Note no property delete is printed when whole file is deleted
    expected_output = make_diff_header(newfile, 'revision 2', 'revision 1') + \
                      [ '@@ -1, +0,0 @@\n',
                        "-This is the file 'newfile'.\n" ]
    svntest.actions.run_and_verify_svn(None, None, [], 'diff',
                                       '-r2:1', newfile)
              diff_repo_wc_file_props,
              diff_repo_repo_added_file_mime_type,