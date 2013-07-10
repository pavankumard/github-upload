/**
 * @copyright
 * ====================================================================
 *    Licensed to the Apache Software Foundation (ASF) under one
 *    or more contributor license agreements.  See the NOTICE file
 *    distributed with this work for additional information
 *    regarding copyright ownership.  The ASF licenses this file
 *    to you under the Apache License, Version 2.0 (the
 *    "License"); you may not use this file except in compliance
 *    with the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *    Unless required by applicable law or agreed to in writing,
 *    software distributed under the License is distributed on an
 *    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 *    KIND, either express or implied.  See the License for the
 *    specific language governing permissions and limitations
 *    under the License.
 * ====================================================================
 * @endcopyright
 *
 * @file svn_repos_private.h
 * @brief Subversion-internal repos APIs.
 */

#ifndef SVN_REPOS_PRIVATE_H
#define SVN_REPOS_PRIVATE_H

#include <apr_pools.h>

#include "svn_types.h"
#include "svn_repos.h"
#include "svn_editor.h"

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */


/** Validate that property @a name with @a value is valid (as an addition
 * or edit or deletion) in a Subversion repository.  Return an error if not.
 *
 * If @a value is NULL, return #SVN_NO_ERROR to indicate that any property
 * may be deleted, even an invalid one.  Otherwise, if the @a name is not
 * of kind #svn_prop_regular_kind (see #svn_prop_kind_t), return
 * #SVN_ERR_REPOS_BAD_ARGS.  Otherwise, for some "svn:" properties, also
 * perform some validations on the @a value (e.g., for such properties,
 * typically the @a value must be in UTF-8 with LF linefeeds), and return
 * #SVN_ERR_BAD_PROPERTY_VALUE if it is not valid.
 *
 * Validations may be added in future releases, for example, for
 * newly-added #SVN_PROP_PREFIX properties.  However, user-defined
 * (non-#SVN_PROP_PREFIX) properties will never have their @a value
 * validated in any way.
 *
 * Use @a pool for temporary allocations.
 *
 * @note This function is used to implement server-side validation.
 * Consequently, if you make this function stricter in what it accepts, you
 * (a) break svnsync'ing of existing repositories that contain now-invalid
 * properties, (b) do not preclude such invalid values from entering the
 * repository via tools that use the svn_fs_* API directly (possibly
 * including svnadmin and svnlook).  This has happened before and there
 * are known (documented, but unsupported) upgrade paths in some cases.
 *
 * @since New in 1.7.
 */
svn_error_t *
svn_repos__validate_prop(const char *name,
                         const svn_string_t *value,
                         apr_pool_t *pool);

/**
 * Given the error @a err from svn_repos_fs_commit_txn(), return an
 * string containing either or both of the svn_fs_commit_txn() error
 * and the SVN_ERR_REPOS_POST_COMMIT_HOOK_FAILED wrapped error from
 * the post-commit hook.  Any error tracing placeholders in the error
 * chain are skipped over.
 *
 * This function does not modify @a err.
 *
 * ### This method should not be necessary, but there are a few
 * ### places, e.g. mod_dav_svn, where only a single error message
 * ### string is returned to the caller and it is useful to have both
 * ### error messages included in the message.
 *
 * Use @a pool to do any allocations in.
 *
 * @since New in 1.7.
 */
const char *
svn_repos__post_commit_error_str(svn_error_t *err,
                                 apr_pool_t *pool);

/* A repos version of svn_fs_type */
svn_error_t *
svn_repos__fs_type(const char **fs_type,
                   const char *repos_path,
                   apr_pool_t *pool);


/* Create a commit editor for REPOS, based on REVISION.  */
svn_error_t *
svn_repos__get_commit_ev2(svn_editor_t **editor,
                          svn_repos_t *repos,
                          svn_authz_t *authz,
                          const char *authz_repos_name,
                          const char *authz_user,
                          apr_hash_t *revprops,
                          svn_commit_callback2_t commit_cb,
                          void *commit_baton,
                          svn_cancel_func_t cancel_func,
                          void *cancel_baton,
                          apr_pool_t *result_pool,
                          apr_pool_t *scratch_pool);

svn_error_t *
svn_repos__replay_ev2(svn_fs_root_t *root,
                      const char *base_dir,
                      svn_revnum_t low_water_mark,
                      svn_editor_t *editor,
                      svn_repos_authz_func_t authz_read_func,
                      void *authz_read_baton,
                      apr_pool_t *scratch_pool);


#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SVN_REPOS_PRIVATE_H */
