# -*- encoding: utf-8 -*-

"""
_models/models_generic.py  
- provides the models for all api routes
"""

from log_config import log, pformat

log.debug("... loading models_generic.py ...")


from flask_restplus import fields

### import data serializers
from auth_api._serializers.schema_logs    import *  
from auth_api._serializers.schema_generic import *  
from auth_api._serializers.schema_users   import *  


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / BASIC INFOS 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_basic_infos( ns_, 
                model_name     = "Basic_infos",
                schema         = doc_basics,
                is_user_infos  = False, 
                is_user_light  = False, 
                need_licence   = False,
              ) : 
  """ 
  Basic infos model
  """

  # schema = doc_basics

  if is_user_infos == True : 
    schema = user_basics 
    if is_user_light : 
      schema = user_basics_light 
  
  if need_licence == True : 
    schema = doc_basics_licence 

  basic_infos    = fields.Nested(
    ns_.model( model_name , schema ),
    description = "basic infos about the document"
  )
  return basic_infos


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / FIELD UPDATE
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_field_update( ns_, 
                model_name = "Field_update" 
              ):
  
  """
  Field update
  """
  
  # field_update = fields.Nested( 
  #   ns_.model( model_name, update_field ),
  #   description = "update a field of a document"
  # )

  field_update = ns_.model(model_name, update_field )
  
  return field_update


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / PUBLIC AUTH 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_public_auth(  ns_, 
                model_name = "Public_auth" 
              ):
  
  """
  Public auth model
  """
  
  public_authorizations = fields.Nested( 
    ns_.model( model_name, public_auth ),
    description = "public authorization levels on this document"
  )

  return public_authorizations


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / MULTILANGUAGE 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_translations(  ns_, 
                model_name = "Translations"
              ):
  
  """
  Translations model
  """
  
  translation = fields.Nested( 
    ns_.model( model_name, {
      'locale'          : locale,
      'field_to_translate'      : field_to_translate,
      'translation'          : text_translated,
    })
  )

  translations = fields.List( 
    translation,
    description = "List of {}s on this document".format(model_name), 
    default     = [] 
  ) 

  return translations


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / TEAM 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_team(  ns_, 
            model_name   = "Collaborator",
            is_light  = False
          ):
  
  """
  Team model
  """
  
  team_oids = {
      'oid_usr'  : oid_usr,
    }
  team_infos = {
      'edit_auth'  : edit_auth,
      'added_at'  : added_at,
      'added_by'  : added_by,
    }
  if is_light : 
    team_dict = team_oids
  else : 
    team_dict = {**team_oids, **team_infos}


  collaborator = fields.Nested( 
    ns_.model( model_name, team_dict )
  )

  collaborators = fields.List( 
    collaborator,
    description = "List of {}s on this document".format(model_name), 
    default     = [] 
  ) 

  return collaborators


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / about the user
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_profile(  ns_, 
              model_name = "User_profile" 
            ):
  
  """
  Profile of an user
  """

  profile = fields.Nested( 
      ns_.model(model_name, usr_profile_ )
    )

  return profile


def create_model_auth(  ns_, 
            model_name   = "User_authorizations",
            schema      = user_auth_in
          ):
  
  """
  Authorizations of an user
  """

  auth = fields.Nested( 
      ns_.model(model_name, schema )
    )

  return auth


def create_professional_infos(  ns_, 
                model_name = "Structures"
              ):
    
  """
  Professional infos model  
  """
  
  structure_infos = fields.Nested( 
    ns_.model( model_name, user_struct )
  )

  structures_list = fields.List( 
    structure_infos,
    description   = "Structure informations", 
    default     = [] 
  ) 

  return structures_list


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / USES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_uses(  ns_,   
          model_name    = "Uses", 
          include_used_as = False,
          used_as      = "tax",
          schema_list    = ["prj","dmt","dmf","dsi","dsr","usr","rec"], 
        ):

  """
  Uses model
  """
  
  uses_dict = {}

  for schema in schema_list : 

    doc_uses     = {
      "used_by" : used_by,
    }

    if include_used_as == True and schema == "prj" :
      doc_uses["used_as"] = used_as

    uses_dates = fields.List (
      # used_at ,
      at ,
      description = "Uses dates", 
      default   = [] 
    )

    doc_uses["used_at"] = uses_dates

    uses_infos = fields.Nested( 
      ns_.model( "Used_by_"+schema, doc_uses )
    )

    uses_list = fields.List( 
      uses_infos,
      description = "Uses informations", 
      default   = [] 
    ) 
  
    uses_dict["by_"+schema] = uses_list

  uses = fields.Nested( 
    ns_.model( model_name, uses_dict )
  )

  return uses


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / MODIFICATIONS LOG
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_modif_log(    ns_, 
                model_name   = "Modification", 
                schema    = modification_full, 
              ) :

  """ 
  Modif log model
  """
  
  ### compile the list of modifications
  modifications = fields.List(
    fields.Nested(
        ns_.model( model_name, schema )
    ),
    description = "List of the {}s on this document".format(model_name), 
    default      = [] 
  )

  return modifications


def create_model_log(  ns_, 
            model_name           = "Log", 
            include_counts        = False, 
            counts_name          = "counts",
            include_is_running      = False,
            include_is_loaded      = False,
            include_src_link      = False,
            include_is_linked_to_dmt  = False,
            include_dso_log        = False,
          ) :

  """ 
  Log model
  """

  log_base = {
        'created_at'    : created_at,
        'created_by'    : created_by,
      }

  if include_counts == True :
    log_base[ counts_name ]   = count

  if include_is_running == True :
    log_base[ "is_running" ]   = is_running

  if include_is_loaded == True :
    log_base[ "is_loaded" ]   = is_loaded

  if include_dso_log == True :
    log_base[ "is_buildable" ]   = is_buildable
    log_base[ "needs_rebuild" ] = needs_rebuild

  ### compile the log
  logs = fields.Nested(
    ns_.model( model_name, log_base ),
    description = "{}s concerning this document".format(model_name), 
  )

  return logs


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / SPECS 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_specs(  ns_, 
            model_name           = "Specs", 
            include_src_link      = False,
            include_inherit_from_dmt  = False,
            include_child_of_tag    = False,
            include_is_standard      = False
          ) :
  """
  Specs model 
  """
  
  specs_base = {
          'doc_type'    : doc_type,
        }

  if include_is_standard == True : 
    specs_base['is_standard']    = is_standard

  if include_src_link == True : 
    specs_base['src_link']    = src_link
    specs_base['src_type']    = src_type
    specs_base['src_parser']  = src_parser
    specs_base['src_sep']    = src_sep

  ### TO DO 
  if include_inherit_from_dmt == True :
    pass

  if include_child_of_tag == True :
    pass

  ### compile the document's specs
  doc_specs = fields.Nested( 
    ns_.model( model_name, specs_base )
  )

  return doc_specs


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / DATA RAW  
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_data_raw(   ns_, 
              model_name   = "Data_raw",
              schema      = "tag",
            ) : 
  """ 
  data_raw_fields model
  """

  if schema in ["dmf", "tag" ] : 

    if schema == "tag" : 
      schema_  = f_basics_tag

    if schema == "dmf" : 
      schema_  = f_basics_dmf

    data_raw_fields    = fields.Nested(
      ns_.model( model_name , schema_ ),
      description = "Data_raw"
    )

  if schema in [ "dsi", "dsr", "dso" ] : 
    
    ### JUST A DRAFT
    # raw_nested_fields    = fields.Nested(
    #   ns_.model( model_name , { "arbitrary_field" : RawData} ),
    #   description = "Data_raw"
    # )

    # raw_field = fields.List(
    #   RawData ,  
    #   description = "List of the {}s on this document".format(model_name), 
    #   default    = [] 
    # )

    if schema == "dso" : 
      schema_f  = f_headers_dso
    
    else : 
      schema_f  = f_headers_ds


    f_coll_headers = fields.Nested(
      ns_.model( model_name , schema_f ),
      description = "Coll_headers"
    )

    f_coll_headers_list = fields.List( 
      f_coll_headers,
      description = "List of {}s on this document".format(schema), 
      default     = [] 
    ) 

    schema_ = {
      "f_col_headers" : f_coll_headers_list,
      # "f_col_headers" : f_coll_headers,
      "f_data"    : f_data,
    }
    data_raw_fields    = fields.Nested(
      ns_.model( model_name , schema_ ),
      description = "Data_raw"
    )

  if schema in [ "rec" ] : 

    data_raw_fields    = fields.Nested(
      ns_.model( model_name , f_basics_rec ),
      description = "Data_raw"
    )

  return data_raw_fields

