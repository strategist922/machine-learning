#!/usr/bin/python

## @session_data_append.py
#  This file receives data (i.e. settings), including one or more dataset(s)
#      provided during the current session, and stores them into corresponding
#      database tables. The stored dataset(s) can later be retrieved from
#      'session_data_append.py', or 'session_generate_model.py'.
#
#  Note: the term 'dataset' used throughout various comments in this file,
#        synonymously implies the user supplied 'file upload(s)', and XML url
#        references.
from session.session_data_new import Data_New

## Class: Data_Append, inherit base methods from superclass 'Session_Base'
class Data_Append(Session_Base):

  ## constructor: define class properties using the superclass 'Data_New'
  #               constructor, along with the constructor in this subclass.
  #
  #  @super(), implement 'Data_New' superclass constructor within this
  #      child class constructor.
  #
  #  Note: the superclass constructor expects the same 'svm_data' argument.
  def __init__(self, svm_data):
    super(Data_New, self).__init__(svm_data)

  ## save_svm_entity: update existing entity within corresponding database
  #                   table, 'tbl_dataset_entity'.
  #
  #  @session_id, synonymous to 'entity_id', and provides context to update
  #      'modified_xx' columns within the 'tbl_dataset_entity' database table.
  def save_svm_entity(self, session_type, session_id):
    svm_entity = {'title': json.loads( self.svm_data )['data']['settings'].get('svm_title', None), 'uid': 1, 'id_entity': session_id}
    db_save    = Training( svm_entity, 'save_entity', session_type )

    # save dataset element
    db_return = db_save.db_save_training()

    # return error(s)
    if not db_return['status']:
      self.response_error.append( db_return['error'] )
      return { 'id': None, 'error': self.response_error }

    # return session id
    elif db_return['status'] and session_type == 'data_new':
      return { 'id': db_return['id'], 'error': None }
