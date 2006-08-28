/*
 * mod_dav_svn.c: an Apache mod_dav sub-module to provide a Subversion
 *                repository.
 *
 * ====================================================================
 * Copyright (c) 2000-2004 CollabNet.  All rights reserved.
 *
 * This software is licensed as described in the file COPYING, which
 * you should have received as part of this distribution.  The terms
 * are also available at http://subversion.tigris.org/license-1.html.
 * If newer versions of this license are posted there, you may use a
 * newer version instead, at your option.
 *
 * This software consists of voluntary contributions made by many
 * individuals.  For exact contribution history, see the revision
 * history and logs, available at http://subversion.tigris.org/.
 * ====================================================================
 */

#include <apr_strings.h>

#include <httpd.h>
#include <http_config.h>
#include <http_request.h>
#include <http_log.h>
#include <ap_provider.h>
#include <mod_dav.h>

#include "svn_version.h"
#include "svn_fs.h"
#include "svn_utf.h"
#include "svn_dso.h"
#include "mod_dav_svn.h"

#include "dav_svn.h"


/* This is the default "special uri" used for SVN's special resources
   (e.g. working resources, activities) */
#define SVN_DEFAULT_SPECIAL_URI "!svn"


/* per-server configuration */
typedef struct {
  const char *special_uri;
} server_conf_t;


/* A tri-state enum used for per directory on/off flags.  Note that
   it's important that CONF_FLAG_DEFAULT is 0 to make
   dav_svn_merge_dir_config do the right thing. */
enum conf_flag {
  CONF_FLAG_DEFAULT,
  CONF_FLAG_ON,
  CONF_FLAG_OFF
};


/* per-dir configuration */
typedef struct {
  const char *fs_path;               /* path to the SVN FS */
  const char *repo_name;             /* repository name */
  const char *xslt_uri;              /* XSL transform URI */
  const char *fs_parent_path;        /* path to parent of SVN FS'es  */
  enum conf_flag autoversioning;  /* whether autoversioning is active */
  enum conf_flag do_path_authz;   /* whether GET subrequests are active */
  enum conf_flag list_parentpath; /* whether to allow GET of parentpath */
  enum conf_flag do_native_authz; /* whether native authz is active */
  const char *native_authz_file;     /* rule file for native authz */
} dir_conf_t;


#define INHERIT_VALUE(parent, child, field) \
                ((child)->field ? (child)->field : (parent)->field)


extern module AP_MODULE_DECLARE_DATA dav_svn_module;


static int
init(apr_pool_t *p, apr_pool_t *plog, apr_pool_t *ptemp, server_rec *s)
{
  svn_error_t *serr;
  ap_add_version_component(p, "SVN/" SVN_VER_NUMBER);

  serr = svn_fs_initialize(p);
  if (serr)
    {
      ap_log_perror(APLOG_MARK, APLOG_ERR, serr->apr_err, p,
                    "mod_dav_svn: error calling svn_fs_initialize: '%s'",
                    serr->message ? serr->message : "(no more info)");
      return HTTP_INTERNAL_SERVER_ERROR;
    }

  /* This returns void, so we can't check for error. */
  svn_utf_initialize(p);

  return OK;
}

static int
init_dso(apr_pool_t *pconf, apr_pool_t *plog, apr_pool_t *ptemp)
{
  /* This isn't ideal, we're not actually being called before any
     pool is created, but we are being called before the server or
     request pools are created, which is probably good enough for
     98% of cases. */

  svn_dso_initialize();

  return OK;
}

static void *
create_server_config(apr_pool_t *p, server_rec *s)
{
  return apr_pcalloc(p, sizeof(server_conf_t));
}


static void *
merge_server_config(apr_pool_t *p, void *base, void *overrides)
{
  server_conf_t *parent = base;
  server_conf_t *child = overrides;
  server_conf_t *newconf;

  newconf = apr_pcalloc(p, sizeof(*newconf));

  newconf->special_uri = INHERIT_VALUE(parent, child, special_uri);

  return newconf;
}


static void *
create_dir_config(apr_pool_t *p, char *dir)
{
  /* NOTE: dir==NULL creates the default per-dir config */
  dir_conf_t *conf = apr_pcalloc(p, sizeof(*conf));

  return conf;
}


static void *
merge_dir_config(apr_pool_t *p, void *base, void *overrides)
{
  dir_conf_t *parent = base;
  dir_conf_t *child = overrides;
  dir_conf_t *newconf;

  newconf = apr_pcalloc(p, sizeof(*newconf));

  newconf->fs_path = INHERIT_VALUE(parent, child, fs_path);
  newconf->repo_name = INHERIT_VALUE(parent, child, repo_name);
  newconf->xslt_uri = INHERIT_VALUE(parent, child, xslt_uri);
  newconf->fs_parent_path = INHERIT_VALUE(parent, child, fs_parent_path);
  newconf->autoversioning = INHERIT_VALUE(parent, child, autoversioning);
  newconf->do_path_authz = INHERIT_VALUE(parent, child, do_path_authz);
  newconf->list_parentpath = INHERIT_VALUE(parent, child, list_parentpath);
  newconf->do_native_authz = INHERIT_VALUE(parent, child, do_native_authz);
  newconf->native_authz_file = INHERIT_VALUE(parent, child, native_authz_file);

  return newconf;
}


static const char *
SVNReposName_cmd(cmd_parms *cmd, void *config, const char *arg1)
{
  dir_conf_t *conf = config;

  conf->repo_name = apr_pstrdup(cmd->pool, arg1);

  return NULL;
}


static const char *
SVNIndexXSLT_cmd(cmd_parms *cmd, void *config, const char *arg1)
{
  dir_conf_t *conf = config;

  conf->xslt_uri = apr_pstrdup(cmd->pool, arg1);

  return NULL;
}


static const char *
SVNAutoversioning_cmd(cmd_parms *cmd, void *config, int arg)
{
  dir_conf_t *conf = config;

  if (arg)
    conf->autoversioning = CONF_FLAG_ON;
  else
    conf->autoversioning = CONF_FLAG_OFF;

  return NULL;
}


static const char *
SVNPathAuthz_cmd(cmd_parms *cmd, void *config, int arg)
{
  dir_conf_t *conf = config;

  if (arg)
    conf->do_path_authz = CONF_FLAG_ON;
  else
    conf->do_path_authz = CONF_FLAG_OFF;

  return NULL;
}


static const char *
SVNListParentPath_cmd(cmd_parms *cmd, void *config, int arg)
{
  dir_conf_t *conf = config;

  if (arg)
    conf->list_parentpath = CONF_FLAG_ON;
  else
    conf->list_parentpath = CONF_FLAG_OFF;

  return NULL;
}


static const char *
SVNPath_cmd(cmd_parms *cmd, void *config, const char *arg1)
{
  dir_conf_t *conf = config;

  if (conf->fs_parent_path != NULL)
    return "SVNPath cannot be defined at same time as SVNParentPath.";

  conf->fs_path
    = svn_path_canonicalize(apr_pstrdup(cmd->pool, arg1), cmd->pool);

  return NULL;
}


static const char *
SVNParentPath_cmd(cmd_parms *cmd, void *config, const char *arg1)
{
  dir_conf_t *conf = config;

  if (conf->fs_path != NULL)
    return "SVNParentPath cannot be defined at same time as SVNPath.";

  conf->fs_parent_path
    = svn_path_canonicalize(apr_pstrdup(cmd->pool, arg1), cmd->pool);

  return NULL;
}


static const char *
SVNSpecialURI_cmd(cmd_parms *cmd, void *config, const char *arg1)
{
  server_conf_t *conf;
  char *uri;
  apr_size_t len;

  uri = apr_pstrdup(cmd->pool, arg1);

  /* apply a bit of processing to the thing:
     - eliminate .. and . components
     - eliminate double slashes
     - eliminate leading and trailing slashes
     */
  ap_getparents(uri);
  ap_no2slash(uri);
  if (*uri == '/')
    ++uri;
  len = strlen(uri);
  if (len > 0 && uri[len - 1] == '/')
    uri[--len] = '\0';
  if (len == 0)
    return "The special URI path must have at least one component.";

  conf = ap_get_module_config(cmd->server->module_config,
                              &dav_svn_module);
  conf->special_uri = uri;

  return NULL;
}

static const char *
SVNNativeAuthz_cmd(cmd_parms *cmd, void *config, int arg)
{
  dir_conf_t *conf = config;

  if (arg)
    conf->do_native_authz = CONF_FLAG_ON;
  else
    conf->do_native_authz = CONF_FLAG_OFF;

  return NULL;
}


static const char *
SVNNativeAuthzFile_cmd(cmd_parms *cmd, void *config, const char *arg1)
{
  dir_conf_t *conf = config;

  conf->native_authz_file
      = svn_path_canonicalize(apr_pstrdup(cmd->pool, arg1), cmd->pool);

  return NULL;
}


/** Accessor functions for the module's configuration state **/

const char *
dav_svn__get_fs_path(request_rec *r)
{
  dir_conf_t *conf;

  conf = ap_get_module_config(r->per_dir_config, &dav_svn_module);
  return conf->fs_path;
}


const char *
dav_svn__get_fs_parent_path(request_rec *r)
{
  dir_conf_t *conf;

  conf = ap_get_module_config(r->per_dir_config, &dav_svn_module);
  return conf->fs_parent_path;
}


AP_MODULE_DECLARE(dav_error *)
dav_svn_get_repos_path(request_rec *r,
                       const char *root_path,
                       const char **repos_path)
{

  const char *fs_path;        
  const char *fs_parent_path; 
  const char *repos_name;
  const char *ignored_path_in_repos;
  const char *ignored_cleaned_uri;
  const char *ignored_relative;
  int ignored_had_slash;
  dav_error *derr;

  /* Handle the SVNPath case. */
  fs_path = dav_svn__get_fs_path(r);

  if (fs_path != NULL)
    {
      *repos_path = fs_path;
      return NULL;
    }

  /* Handle the SVNParentPath case.  If neither directive was used,
     dav_svn_split_uri will throw a suitable error for us - we do
     not need to check that here. */
  fs_parent_path = dav_svn__get_fs_parent_path(r);

  /* Split the svn URI to get the name of the repository below
     the parent path. */
  derr = dav_svn_split_uri(r, r->uri, root_path,
                           &ignored_cleaned_uri, &ignored_had_slash,
                           &repos_name,
                           &ignored_relative, &ignored_path_in_repos);
  if (derr)
    return derr;

  /* Construct the full path from the parent path base directory
     and the repository name. */
  *repos_path = svn_path_join(fs_parent_path, repos_name, r->pool);
  return NULL;
}


const char *
dav_svn__get_repo_name(request_rec *r)
{
  dir_conf_t *conf;

  conf = ap_get_module_config(r->per_dir_config, &dav_svn_module);
  return conf->repo_name;
}


const char *
dav_svn__get_xslt_uri(request_rec *r)
{
  dir_conf_t *conf;

  conf = ap_get_module_config(r->per_dir_config, &dav_svn_module);
  return conf->xslt_uri;
}


const char *
dav_svn__get_special_uri(request_rec *r)
{
  server_conf_t *conf;

  conf = ap_get_module_config(r->server->module_config,
                              &dav_svn_module);
  return conf->special_uri ? conf->special_uri : SVN_DEFAULT_SPECIAL_URI;
}


svn_boolean_t
dav_svn__get_autoversioning_flag(request_rec *r)
{
  dir_conf_t *conf;

  conf = ap_get_module_config(r->per_dir_config, &dav_svn_module);
  return conf->autoversioning == CONF_FLAG_ON;
}


svn_boolean_t
dav_svn__get_pathauthz_flag(request_rec *r)
{
  dir_conf_t *conf;

  conf = ap_get_module_config(r->per_dir_config, &dav_svn_module);
  return conf->do_path_authz != CONF_FLAG_OFF;
}


svn_boolean_t
dav_svn__get_list_parentpath_flag(request_rec *r)
{
  dir_conf_t *conf;

  conf = ap_get_module_config(r->per_dir_config, &dav_svn_module);
  return conf->list_parentpath == CONF_FLAG_ON;
}


svn_boolean_t
dav_svn__get_native_authz_flag(request_rec *r)
{
    dir_conf_t *conf;

    conf = ap_get_module_config(r->per_dir_config, &dav_svn_module);
    return conf->do_native_authz == CONF_FLAG_ON;
}


const char *
dav_svn__get_native_authz_file(request_rec *r)
{
    dir_conf_t *conf;

    conf = ap_get_module_config(r->per_dir_config, &dav_svn_module);
    return conf->native_authz_file;
}


static void
merge_xml_filter_insert(request_rec *r)
{
  /* We only care about MERGE and DELETE requests. */
  if ((r->method_number == M_MERGE)
      || (r->method_number == M_DELETE))
    {
      dir_conf_t *conf;
      conf = ap_get_module_config(r->per_dir_config, &dav_svn_module);

      /* We only care if we are configured. */
      if (conf->fs_path || conf->fs_parent_path)
        {
          ap_add_input_filter("SVN-MERGE", NULL, r, r->connection);
        }
    }
}


typedef struct {
  apr_bucket_brigade *bb;
  apr_xml_parser *parser;
  apr_pool_t *pool;
} merge_ctx_t;


static apr_status_t
merge_xml_in_filter(ap_filter_t *f,
                    apr_bucket_brigade *bb,
                    ap_input_mode_t mode,
                    apr_read_type_e block,
                    apr_off_t readbytes)
{
  apr_status_t rv;
  request_rec *r = f->r;
  merge_ctx_t *ctx = f->ctx;
  apr_bucket *bucket;
  int seen_eos = 0;

  /* We shouldn't be added if we're not a MERGE/DELETE, but double check. */
  if ((r->method_number != M_MERGE)
      && (r->method_number != M_DELETE))
    {
      ap_remove_input_filter(f);
      return ap_get_brigade(f->next, bb, mode, block, readbytes);
    }

  if (!ctx)
    {
      f->ctx = ctx = apr_palloc(r->pool, sizeof(*ctx));
      ctx->parser = apr_xml_parser_create(r->pool);
      ctx->bb = apr_brigade_create(r->pool, r->connection->bucket_alloc);
      apr_pool_create(&ctx->pool, r->pool);
    }

  rv = ap_get_brigade(f->next, ctx->bb, mode, block, readbytes);

  if (rv != APR_SUCCESS)
    return rv;

  for (bucket = APR_BRIGADE_FIRST(ctx->bb);
       bucket != APR_BRIGADE_SENTINEL(ctx->bb);
       bucket = APR_BUCKET_NEXT(bucket))
    {
      const char *data;
      apr_size_t len;

      if (APR_BUCKET_IS_EOS(bucket))
        {
          seen_eos = 1;
          break;
        }

      if (APR_BUCKET_IS_METADATA(bucket))
        continue;

      rv = apr_bucket_read(bucket, &data, &len, APR_BLOCK_READ);
      if (rv != APR_SUCCESS)
        return rv;

      rv = apr_xml_parser_feed(ctx->parser, data, len);
      if (rv != APR_SUCCESS)
        {
          /* Clean up the parser. */
          (void) apr_xml_parser_done(ctx->parser, NULL);
          break;
        }
    }

  /* This will clear-out the ctx->bb as well. */
  APR_BRIGADE_CONCAT(bb, ctx->bb);

  if (seen_eos)
    {
      apr_xml_doc *pdoc;

      /* Remove ourselves now. */
      ap_remove_input_filter(f);

      /* tell the parser that we're done */
      rv = apr_xml_parser_done(ctx->parser, &pdoc);
      if (rv == APR_SUCCESS)
        {
#if APR_CHARSET_EBCDIC
          apr_xml_parser_convert_doc(r->pool, pdoc, ap_hdrs_from_ascii);
#endif
          /* stash the doc away for mod_dav_svn's later use. */
          rv = apr_pool_userdata_set(pdoc, "svn-request-body",
                                     NULL, r->pool);
          if (rv != APR_SUCCESS)
            return rv;

        }
    }

  return APR_SUCCESS;
}



/** Module framework stuff **/

static const command_rec cmds[] =
{
  /* per directory/location */
  AP_INIT_TAKE1("SVNPath", SVNPath_cmd, NULL, ACCESS_CONF,
                "specifies the location in the filesystem for a Subversion "
                "repository's files."),

  /* per server */
  AP_INIT_TAKE1("SVNSpecialURI", SVNSpecialURI_cmd, NULL, RSRC_CONF,
                "specify the URI component for special Subversion "
                "resources"),

  /* per directory/location */
  AP_INIT_TAKE1("SVNReposName", SVNReposName_cmd, NULL, ACCESS_CONF,
                "specify the name of a Subversion repository"),

  /* per directory/location */
  AP_INIT_TAKE1("SVNIndexXSLT", SVNIndexXSLT_cmd, NULL, ACCESS_CONF,
                "specify the URI of an XSL transformation for "
                "directory indexes"),

  /* per directory/location */
  AP_INIT_TAKE1("SVNParentPath", SVNParentPath_cmd, NULL, ACCESS_CONF,
                "specifies the location in the filesystem whose "
                "subdirectories are assumed to be Subversion repositories."),

  /* per directory/location */
  AP_INIT_FLAG("SVNAutoversioning", SVNAutoversioning_cmd, NULL,
               ACCESS_CONF|RSRC_CONF, "turn on deltaV autoversioning."),

  /* per directory/location */
  AP_INIT_FLAG("SVNPathAuthz", SVNPathAuthz_cmd, NULL,
               ACCESS_CONF|RSRC_CONF,
               "control path-based authz by enabling/disabling subrequests"),

  /* per directory/location */
  AP_INIT_FLAG("SVNListParentPath", SVNListParentPath_cmd, NULL,
               ACCESS_CONF|RSRC_CONF, "allow GET of SVNParentPath."),

  /* per directory/location */
  AP_INIT_FLAG("SVNNativeAuthz", SVNNativeAuthz_cmd, NULL,
               ACCESS_CONF|RSRC_CONF,
               "use mod_dav_svn native path-based authorization"),

  /* per directory/location */
  AP_INIT_TAKE1("SVNNativeAuthzFile", SVNNativeAuthzFile_cmd, NULL,
                ACCESS_CONF|RSRC_CONF,
                "Text file containing permissions of repository paths "
                "for mod_dav_svn native path-based authorization"),

  { NULL }
};


static dav_provider provider =
{
  &dav_svn__hooks_repository,
  &dav_svn__hooks_propdb,
  &dav_svn__hooks_locks,
  &dav_svn__hooks_vsn,
  NULL,                       /* binding */
  NULL                        /* search */
};


static void
register_hooks(apr_pool_t *pconf)
{
  ap_hook_pre_config(init_dso, NULL, NULL, APR_HOOK_REALLY_FIRST);
  ap_hook_post_config(init, NULL, NULL, APR_HOOK_MIDDLE);

  /* our provider */
  dav_register_provider(pconf, "svn", &provider);

  /* input filter to read MERGE bodies. */
  ap_register_input_filter("SVN-MERGE", merge_xml_in_filter, NULL,
                           AP_FTYPE_RESOURCE);
  ap_hook_insert_filter(merge_xml_filter_insert, NULL, NULL,
                        APR_HOOK_MIDDLE);

  /* live property handling */
  dav_hook_gather_propsets(dav_svn__gather_propsets, NULL, NULL,
                           APR_HOOK_MIDDLE);
  dav_hook_find_liveprop(dav_svn__find_liveprop, NULL, NULL, APR_HOOK_MIDDLE);
  dav_hook_insert_all_liveprops(dav_svn__insert_all_liveprops, NULL, NULL,
                                APR_HOOK_MIDDLE);
  dav_register_liveprop_group(pconf, &dav_svn__liveprop_group);
}


module AP_MODULE_DECLARE_DATA dav_svn_module =
{
  STANDARD20_MODULE_STUFF,
  create_dir_config,    /* dir config creater */
  merge_dir_config,     /* dir merger --- default is to override */
  create_server_config, /* server config */
  merge_server_config,  /* merge server config */
  cmds,                 /* command table */
  register_hooks,       /* register hooks */
};
