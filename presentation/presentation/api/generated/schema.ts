// Generated from the API description. Regenerate; do not edit.
export interface paths {
  '/entity/user/add': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Add
     * @description Store one new Entity instance and return the stored Entity, including generated values.
     */
    post: operations['add_entity_user_add_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/user/update': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    /**
     * Update
     * @description Replace every mutable Field of the stored record of an Entity instance; None when it does not exist.
     */
    put: operations['update_entity_user_update_put']
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/user/list': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * List
     * @description Return the matching Entity instances; a zero or negative limit means no limit.
     */
    post: operations['list_entity_user_list_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/user/get_by_id/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Get By Id
     * @description Return the Entity with that id, or None when no record exists.
     */
    get: operations['get_by_id_entity_user_get_by_id__id__get']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/user/delete/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Delete
     * @description Remove the record and return the deleted Entity, or None when no record exists.
     */
    delete: operations['delete_entity_user_delete__id__delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/user/enable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Enable
     * @description Set only is_active to true and return the final Entity, or None when no record exists.
     */
    patch: operations['enable_entity_user_enable__id__patch']
    trace?: never
  }
  '/entity/user/disable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Disable
     * @description Set only is_active to false and return the final Entity, or None when no record exists.
     */
    patch: operations['disable_entity_user_disable__id__patch']
    trace?: never
  }
  '/entity/user/count': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Count
     * @description Return the number of matching records.
     */
    post: operations['count_entity_user_count_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/user/sum': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Sum
     * @description Return the total of a numeric Field, ignoring null values, or zero when nothing matches.
     */
    post: operations['sum_entity_user_sum_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/user/min': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Min
     * @description Return the smallest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['min_entity_user_min_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/user/max': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Max
     * @description Return the largest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['max_entity_user_max_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/user/truncate': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Truncate
     * @description Remove every record of the Entity, keep its Table, and return the deleted count.
     */
    delete: operations['truncate_entity_user_truncate_delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trading_platform/add': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Add
     * @description Store one new Entity instance and return the stored Entity, including generated values.
     */
    post: operations['add_entity_trading_platform_add_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trading_platform/update': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    /**
     * Update
     * @description Replace every mutable Field of the stored record of an Entity instance; None when it does not exist.
     */
    put: operations['update_entity_trading_platform_update_put']
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trading_platform/list': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * List
     * @description Return the matching Entity instances; a zero or negative limit means no limit.
     */
    post: operations['list_entity_trading_platform_list_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trading_platform/get_by_id/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Get By Id
     * @description Return the Entity with that id, or None when no record exists.
     */
    get: operations['get_by_id_entity_trading_platform_get_by_id__id__get']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trading_platform/delete/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Delete
     * @description Remove the record and return the deleted Entity, or None when no record exists.
     */
    delete: operations['delete_entity_trading_platform_delete__id__delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trading_platform/enable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Enable
     * @description Set only is_active to true and return the final Entity, or None when no record exists.
     */
    patch: operations['enable_entity_trading_platform_enable__id__patch']
    trace?: never
  }
  '/entity/trading_platform/disable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Disable
     * @description Set only is_active to false and return the final Entity, or None when no record exists.
     */
    patch: operations['disable_entity_trading_platform_disable__id__patch']
    trace?: never
  }
  '/entity/trading_platform/count': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Count
     * @description Return the number of matching records.
     */
    post: operations['count_entity_trading_platform_count_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trading_platform/sum': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Sum
     * @description Return the total of a numeric Field, ignoring null values, or zero when nothing matches.
     */
    post: operations['sum_entity_trading_platform_sum_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trading_platform/min': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Min
     * @description Return the smallest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['min_entity_trading_platform_min_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trading_platform/max': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Max
     * @description Return the largest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['max_entity_trading_platform_max_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trading_platform/truncate': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Truncate
     * @description Remove every record of the Entity, keep its Table, and return the deleted count.
     */
    delete: operations['truncate_entity_trading_platform_truncate_delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/instance/add': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Add
     * @description Store one new Entity instance and return the stored Entity, including generated values.
     */
    post: operations['add_entity_instance_add_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/instance/update': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    /**
     * Update
     * @description Replace every mutable Field of the stored record of an Entity instance; None when it does not exist.
     */
    put: operations['update_entity_instance_update_put']
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/instance/list': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * List
     * @description Return the matching Entity instances; a zero or negative limit means no limit.
     */
    post: operations['list_entity_instance_list_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/instance/get_by_id/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Get By Id
     * @description Return the Entity with that id, or None when no record exists.
     */
    get: operations['get_by_id_entity_instance_get_by_id__id__get']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/instance/delete/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Delete
     * @description Remove the record and return the deleted Entity, or None when no record exists.
     */
    delete: operations['delete_entity_instance_delete__id__delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/instance/enable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Enable
     * @description Set only is_active to true and return the final Entity, or None when no record exists.
     */
    patch: operations['enable_entity_instance_enable__id__patch']
    trace?: never
  }
  '/entity/instance/disable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Disable
     * @description Set only is_active to false and return the final Entity, or None when no record exists.
     */
    patch: operations['disable_entity_instance_disable__id__patch']
    trace?: never
  }
  '/entity/instance/count': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Count
     * @description Return the number of matching records.
     */
    post: operations['count_entity_instance_count_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/instance/sum': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Sum
     * @description Return the total of a numeric Field, ignoring null values, or zero when nothing matches.
     */
    post: operations['sum_entity_instance_sum_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/instance/min': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Min
     * @description Return the smallest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['min_entity_instance_min_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/instance/max': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Max
     * @description Return the largest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['max_entity_instance_max_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/instance/truncate': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Truncate
     * @description Remove every record of the Entity, keep its Table, and return the deleted count.
     */
    delete: operations['truncate_entity_instance_truncate_delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/currency/add': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Add
     * @description Store one new Entity instance and return the stored Entity, including generated values.
     */
    post: operations['add_entity_currency_add_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/currency/update': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    /**
     * Update
     * @description Replace every mutable Field of the stored record of an Entity instance; None when it does not exist.
     */
    put: operations['update_entity_currency_update_put']
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/currency/list': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * List
     * @description Return the matching Entity instances; a zero or negative limit means no limit.
     */
    post: operations['list_entity_currency_list_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/currency/get_by_id/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Get By Id
     * @description Return the Entity with that id, or None when no record exists.
     */
    get: operations['get_by_id_entity_currency_get_by_id__id__get']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/currency/delete/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Delete
     * @description Remove the record and return the deleted Entity, or None when no record exists.
     */
    delete: operations['delete_entity_currency_delete__id__delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/currency/enable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Enable
     * @description Set only is_active to true and return the final Entity, or None when no record exists.
     */
    patch: operations['enable_entity_currency_enable__id__patch']
    trace?: never
  }
  '/entity/currency/disable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Disable
     * @description Set only is_active to false and return the final Entity, or None when no record exists.
     */
    patch: operations['disable_entity_currency_disable__id__patch']
    trace?: never
  }
  '/entity/currency/count': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Count
     * @description Return the number of matching records.
     */
    post: operations['count_entity_currency_count_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/currency/sum': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Sum
     * @description Return the total of a numeric Field, ignoring null values, or zero when nothing matches.
     */
    post: operations['sum_entity_currency_sum_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/currency/min': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Min
     * @description Return the smallest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['min_entity_currency_min_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/currency/max': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Max
     * @description Return the largest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['max_entity_currency_max_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/currency/truncate': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Truncate
     * @description Remove every record of the Entity, keep its Table, and return the deleted count.
     */
    delete: operations['truncate_entity_currency_truncate_delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/broker/add': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Add
     * @description Store one new Entity instance and return the stored Entity, including generated values.
     */
    post: operations['add_entity_broker_add_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/broker/update': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    /**
     * Update
     * @description Replace every mutable Field of the stored record of an Entity instance; None when it does not exist.
     */
    put: operations['update_entity_broker_update_put']
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/broker/list': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * List
     * @description Return the matching Entity instances; a zero or negative limit means no limit.
     */
    post: operations['list_entity_broker_list_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/broker/get_by_id/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Get By Id
     * @description Return the Entity with that id, or None when no record exists.
     */
    get: operations['get_by_id_entity_broker_get_by_id__id__get']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/broker/delete/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Delete
     * @description Remove the record and return the deleted Entity, or None when no record exists.
     */
    delete: operations['delete_entity_broker_delete__id__delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/broker/enable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Enable
     * @description Set only is_active to true and return the final Entity, or None when no record exists.
     */
    patch: operations['enable_entity_broker_enable__id__patch']
    trace?: never
  }
  '/entity/broker/disable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Disable
     * @description Set only is_active to false and return the final Entity, or None when no record exists.
     */
    patch: operations['disable_entity_broker_disable__id__patch']
    trace?: never
  }
  '/entity/broker/count': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Count
     * @description Return the number of matching records.
     */
    post: operations['count_entity_broker_count_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/broker/sum': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Sum
     * @description Return the total of a numeric Field, ignoring null values, or zero when nothing matches.
     */
    post: operations['sum_entity_broker_sum_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/broker/min': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Min
     * @description Return the smallest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['min_entity_broker_min_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/broker/max': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Max
     * @description Return the largest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['max_entity_broker_max_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/broker/truncate': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Truncate
     * @description Remove every record of the Entity, keep its Table, and return the deleted count.
     */
    delete: operations['truncate_entity_broker_truncate_delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/asset/add': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Add
     * @description Store one new Entity instance and return the stored Entity, including generated values.
     */
    post: operations['add_entity_asset_add_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/asset/update': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    /**
     * Update
     * @description Replace every mutable Field of the stored record of an Entity instance; None when it does not exist.
     */
    put: operations['update_entity_asset_update_put']
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/asset/list': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * List
     * @description Return the matching Entity instances; a zero or negative limit means no limit.
     */
    post: operations['list_entity_asset_list_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/asset/get_by_id/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Get By Id
     * @description Return the Entity with that id, or None when no record exists.
     */
    get: operations['get_by_id_entity_asset_get_by_id__id__get']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/asset/delete/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Delete
     * @description Remove the record and return the deleted Entity, or None when no record exists.
     */
    delete: operations['delete_entity_asset_delete__id__delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/asset/enable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Enable
     * @description Set only is_active to true and return the final Entity, or None when no record exists.
     */
    patch: operations['enable_entity_asset_enable__id__patch']
    trace?: never
  }
  '/entity/asset/disable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Disable
     * @description Set only is_active to false and return the final Entity, or None when no record exists.
     */
    patch: operations['disable_entity_asset_disable__id__patch']
    trace?: never
  }
  '/entity/asset/count': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Count
     * @description Return the number of matching records.
     */
    post: operations['count_entity_asset_count_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/asset/sum': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Sum
     * @description Return the total of a numeric Field, ignoring null values, or zero when nothing matches.
     */
    post: operations['sum_entity_asset_sum_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/asset/min': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Min
     * @description Return the smallest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['min_entity_asset_min_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/asset/max': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Max
     * @description Return the largest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['max_entity_asset_max_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/asset/truncate': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Truncate
     * @description Remove every record of the Entity, keep its Table, and return the deleted count.
     */
    delete: operations['truncate_entity_asset_truncate_delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/account_group/add': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Add
     * @description Store one new Entity instance and return the stored Entity, including generated values.
     */
    post: operations['add_entity_account_group_add_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/account_group/update': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    /**
     * Update
     * @description Replace every mutable Field of the stored record of an Entity instance; None when it does not exist.
     */
    put: operations['update_entity_account_group_update_put']
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/account_group/list': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * List
     * @description Return the matching Entity instances; a zero or negative limit means no limit.
     */
    post: operations['list_entity_account_group_list_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/account_group/get_by_id/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Get By Id
     * @description Return the Entity with that id, or None when no record exists.
     */
    get: operations['get_by_id_entity_account_group_get_by_id__id__get']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/account_group/delete/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Delete
     * @description Remove the record and return the deleted Entity, or None when no record exists.
     */
    delete: operations['delete_entity_account_group_delete__id__delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/account_group/enable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Enable
     * @description Set only is_active to true and return the final Entity, or None when no record exists.
     */
    patch: operations['enable_entity_account_group_enable__id__patch']
    trace?: never
  }
  '/entity/account_group/disable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Disable
     * @description Set only is_active to false and return the final Entity, or None when no record exists.
     */
    patch: operations['disable_entity_account_group_disable__id__patch']
    trace?: never
  }
  '/entity/account_group/count': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Count
     * @description Return the number of matching records.
     */
    post: operations['count_entity_account_group_count_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/account_group/sum': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Sum
     * @description Return the total of a numeric Field, ignoring null values, or zero when nothing matches.
     */
    post: operations['sum_entity_account_group_sum_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/account_group/min': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Min
     * @description Return the smallest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['min_entity_account_group_min_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/account_group/max': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Max
     * @description Return the largest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['max_entity_account_group_max_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/account_group/truncate': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Truncate
     * @description Remove every record of the Entity, keep its Table, and return the deleted count.
     */
    delete: operations['truncate_entity_account_group_truncate_delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/account/add': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Add
     * @description Store one new Entity instance and return the stored Entity, including generated values.
     */
    post: operations['add_entity_account_add_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/account/update': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    /**
     * Update
     * @description Replace every mutable Field of the stored record of an Entity instance; None when it does not exist.
     */
    put: operations['update_entity_account_update_put']
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/account/list': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * List
     * @description Return the matching Entity instances; a zero or negative limit means no limit.
     */
    post: operations['list_entity_account_list_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/account/get_by_id/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Get By Id
     * @description Return the Entity with that id, or None when no record exists.
     */
    get: operations['get_by_id_entity_account_get_by_id__id__get']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/account/delete/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Delete
     * @description Remove the record and return the deleted Entity, or None when no record exists.
     */
    delete: operations['delete_entity_account_delete__id__delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/account/enable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Enable
     * @description Set only is_active to true and return the final Entity, or None when no record exists.
     */
    patch: operations['enable_entity_account_enable__id__patch']
    trace?: never
  }
  '/entity/account/disable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Disable
     * @description Set only is_active to false and return the final Entity, or None when no record exists.
     */
    patch: operations['disable_entity_account_disable__id__patch']
    trace?: never
  }
  '/entity/account/count': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Count
     * @description Return the number of matching records.
     */
    post: operations['count_entity_account_count_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/account/sum': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Sum
     * @description Return the total of a numeric Field, ignoring null values, or zero when nothing matches.
     */
    post: operations['sum_entity_account_sum_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/account/min': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Min
     * @description Return the smallest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['min_entity_account_min_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/account/max': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Max
     * @description Return the largest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['max_entity_account_max_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/account/truncate': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Truncate
     * @description Remove every record of the Entity, keep its Table, and return the deleted count.
     */
    delete: operations['truncate_entity_account_truncate_delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trailing_group/add': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Add
     * @description Store one new Entity instance and return the stored Entity, including generated values.
     */
    post: operations['add_entity_trailing_group_add_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trailing_group/update': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    /**
     * Update
     * @description Replace every mutable Field of the stored record of an Entity instance; None when it does not exist.
     */
    put: operations['update_entity_trailing_group_update_put']
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trailing_group/list': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * List
     * @description Return the matching Entity instances; a zero or negative limit means no limit.
     */
    post: operations['list_entity_trailing_group_list_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trailing_group/get_by_id/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Get By Id
     * @description Return the Entity with that id, or None when no record exists.
     */
    get: operations['get_by_id_entity_trailing_group_get_by_id__id__get']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trailing_group/delete/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Delete
     * @description Remove the record and return the deleted Entity, or None when no record exists.
     */
    delete: operations['delete_entity_trailing_group_delete__id__delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trailing_group/enable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Enable
     * @description Set only is_active to true and return the final Entity, or None when no record exists.
     */
    patch: operations['enable_entity_trailing_group_enable__id__patch']
    trace?: never
  }
  '/entity/trailing_group/disable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Disable
     * @description Set only is_active to false and return the final Entity, or None when no record exists.
     */
    patch: operations['disable_entity_trailing_group_disable__id__patch']
    trace?: never
  }
  '/entity/trailing_group/count': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Count
     * @description Return the number of matching records.
     */
    post: operations['count_entity_trailing_group_count_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trailing_group/sum': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Sum
     * @description Return the total of a numeric Field, ignoring null values, or zero when nothing matches.
     */
    post: operations['sum_entity_trailing_group_sum_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trailing_group/min': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Min
     * @description Return the smallest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['min_entity_trailing_group_min_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trailing_group/max': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Max
     * @description Return the largest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['max_entity_trailing_group_max_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trailing_group/truncate': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Truncate
     * @description Remove every record of the Entity, keep its Table, and return the deleted count.
     */
    delete: operations['truncate_entity_trailing_group_truncate_delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trailing_rule/add': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Add
     * @description Store one new Entity instance and return the stored Entity, including generated values.
     */
    post: operations['add_entity_trailing_rule_add_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trailing_rule/update': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    /**
     * Update
     * @description Replace every mutable Field of the stored record of an Entity instance; None when it does not exist.
     */
    put: operations['update_entity_trailing_rule_update_put']
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trailing_rule/list': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * List
     * @description Return the matching Entity instances; a zero or negative limit means no limit.
     */
    post: operations['list_entity_trailing_rule_list_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trailing_rule/get_by_id/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Get By Id
     * @description Return the Entity with that id, or None when no record exists.
     */
    get: operations['get_by_id_entity_trailing_rule_get_by_id__id__get']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trailing_rule/delete/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Delete
     * @description Remove the record and return the deleted Entity, or None when no record exists.
     */
    delete: operations['delete_entity_trailing_rule_delete__id__delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trailing_rule/enable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Enable
     * @description Set only is_active to true and return the final Entity, or None when no record exists.
     */
    patch: operations['enable_entity_trailing_rule_enable__id__patch']
    trace?: never
  }
  '/entity/trailing_rule/disable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Disable
     * @description Set only is_active to false and return the final Entity, or None when no record exists.
     */
    patch: operations['disable_entity_trailing_rule_disable__id__patch']
    trace?: never
  }
  '/entity/trailing_rule/count': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Count
     * @description Return the number of matching records.
     */
    post: operations['count_entity_trailing_rule_count_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trailing_rule/sum': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Sum
     * @description Return the total of a numeric Field, ignoring null values, or zero when nothing matches.
     */
    post: operations['sum_entity_trailing_rule_sum_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trailing_rule/min': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Min
     * @description Return the smallest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['min_entity_trailing_rule_min_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trailing_rule/max': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Max
     * @description Return the largest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['max_entity_trailing_rule_max_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/trailing_rule/truncate': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Truncate
     * @description Remove every record of the Entity, keep its Table, and return the deleted count.
     */
    delete: operations['truncate_entity_trailing_rule_truncate_delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/partial_group/add': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Add
     * @description Store one new Entity instance and return the stored Entity, including generated values.
     */
    post: operations['add_entity_partial_group_add_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/partial_group/update': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    /**
     * Update
     * @description Replace every mutable Field of the stored record of an Entity instance; None when it does not exist.
     */
    put: operations['update_entity_partial_group_update_put']
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/partial_group/list': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * List
     * @description Return the matching Entity instances; a zero or negative limit means no limit.
     */
    post: operations['list_entity_partial_group_list_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/partial_group/get_by_id/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Get By Id
     * @description Return the Entity with that id, or None when no record exists.
     */
    get: operations['get_by_id_entity_partial_group_get_by_id__id__get']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/partial_group/delete/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Delete
     * @description Remove the record and return the deleted Entity, or None when no record exists.
     */
    delete: operations['delete_entity_partial_group_delete__id__delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/partial_group/enable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Enable
     * @description Set only is_active to true and return the final Entity, or None when no record exists.
     */
    patch: operations['enable_entity_partial_group_enable__id__patch']
    trace?: never
  }
  '/entity/partial_group/disable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Disable
     * @description Set only is_active to false and return the final Entity, or None when no record exists.
     */
    patch: operations['disable_entity_partial_group_disable__id__patch']
    trace?: never
  }
  '/entity/partial_group/count': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Count
     * @description Return the number of matching records.
     */
    post: operations['count_entity_partial_group_count_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/partial_group/sum': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Sum
     * @description Return the total of a numeric Field, ignoring null values, or zero when nothing matches.
     */
    post: operations['sum_entity_partial_group_sum_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/partial_group/min': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Min
     * @description Return the smallest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['min_entity_partial_group_min_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/partial_group/max': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Max
     * @description Return the largest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['max_entity_partial_group_max_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/partial_group/truncate': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Truncate
     * @description Remove every record of the Entity, keep its Table, and return the deleted count.
     */
    delete: operations['truncate_entity_partial_group_truncate_delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/partial_rule/add': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Add
     * @description Store one new Entity instance and return the stored Entity, including generated values.
     */
    post: operations['add_entity_partial_rule_add_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/partial_rule/update': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    /**
     * Update
     * @description Replace every mutable Field of the stored record of an Entity instance; None when it does not exist.
     */
    put: operations['update_entity_partial_rule_update_put']
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/partial_rule/list': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * List
     * @description Return the matching Entity instances; a zero or negative limit means no limit.
     */
    post: operations['list_entity_partial_rule_list_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/partial_rule/get_by_id/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Get By Id
     * @description Return the Entity with that id, or None when no record exists.
     */
    get: operations['get_by_id_entity_partial_rule_get_by_id__id__get']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/partial_rule/delete/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Delete
     * @description Remove the record and return the deleted Entity, or None when no record exists.
     */
    delete: operations['delete_entity_partial_rule_delete__id__delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/partial_rule/enable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Enable
     * @description Set only is_active to true and return the final Entity, or None when no record exists.
     */
    patch: operations['enable_entity_partial_rule_enable__id__patch']
    trace?: never
  }
  '/entity/partial_rule/disable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Disable
     * @description Set only is_active to false and return the final Entity, or None when no record exists.
     */
    patch: operations['disable_entity_partial_rule_disable__id__patch']
    trace?: never
  }
  '/entity/partial_rule/count': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Count
     * @description Return the number of matching records.
     */
    post: operations['count_entity_partial_rule_count_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/partial_rule/sum': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Sum
     * @description Return the total of a numeric Field, ignoring null values, or zero when nothing matches.
     */
    post: operations['sum_entity_partial_rule_sum_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/partial_rule/min': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Min
     * @description Return the smallest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['min_entity_partial_rule_min_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/partial_rule/max': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Max
     * @description Return the largest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['max_entity_partial_rule_max_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/partial_rule/truncate': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Truncate
     * @description Remove every record of the Entity, keep its Table, and return the deleted count.
     */
    delete: operations['truncate_entity_partial_rule_truncate_delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/action_group/add': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Add
     * @description Store one new Entity instance and return the stored Entity, including generated values.
     */
    post: operations['add_entity_action_group_add_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/action_group/update': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    /**
     * Update
     * @description Replace every mutable Field of the stored record of an Entity instance; None when it does not exist.
     */
    put: operations['update_entity_action_group_update_put']
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/action_group/list': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * List
     * @description Return the matching Entity instances; a zero or negative limit means no limit.
     */
    post: operations['list_entity_action_group_list_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/action_group/get_by_id/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Get By Id
     * @description Return the Entity with that id, or None when no record exists.
     */
    get: operations['get_by_id_entity_action_group_get_by_id__id__get']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/action_group/delete/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Delete
     * @description Remove the record and return the deleted Entity, or None when no record exists.
     */
    delete: operations['delete_entity_action_group_delete__id__delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/action_group/enable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Enable
     * @description Set only is_active to true and return the final Entity, or None when no record exists.
     */
    patch: operations['enable_entity_action_group_enable__id__patch']
    trace?: never
  }
  '/entity/action_group/disable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Disable
     * @description Set only is_active to false and return the final Entity, or None when no record exists.
     */
    patch: operations['disable_entity_action_group_disable__id__patch']
    trace?: never
  }
  '/entity/action_group/count': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Count
     * @description Return the number of matching records.
     */
    post: operations['count_entity_action_group_count_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/action_group/sum': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Sum
     * @description Return the total of a numeric Field, ignoring null values, or zero when nothing matches.
     */
    post: operations['sum_entity_action_group_sum_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/action_group/min': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Min
     * @description Return the smallest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['min_entity_action_group_min_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/action_group/max': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Max
     * @description Return the largest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['max_entity_action_group_max_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/action_group/truncate': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Truncate
     * @description Remove every record of the Entity, keep its Table, and return the deleted count.
     */
    delete: operations['truncate_entity_action_group_truncate_delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/action/add': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Add
     * @description Store one new Entity instance and return the stored Entity, including generated values.
     */
    post: operations['add_entity_action_add_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/action/update': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    /**
     * Update
     * @description Replace every mutable Field of the stored record of an Entity instance; None when it does not exist.
     */
    put: operations['update_entity_action_update_put']
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/action/list': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * List
     * @description Return the matching Entity instances; a zero or negative limit means no limit.
     */
    post: operations['list_entity_action_list_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/action/get_by_id/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Get By Id
     * @description Return the Entity with that id, or None when no record exists.
     */
    get: operations['get_by_id_entity_action_get_by_id__id__get']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/action/delete/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Delete
     * @description Remove the record and return the deleted Entity, or None when no record exists.
     */
    delete: operations['delete_entity_action_delete__id__delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/action/enable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Enable
     * @description Set only is_active to true and return the final Entity, or None when no record exists.
     */
    patch: operations['enable_entity_action_enable__id__patch']
    trace?: never
  }
  '/entity/action/disable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Disable
     * @description Set only is_active to false and return the final Entity, or None when no record exists.
     */
    patch: operations['disable_entity_action_disable__id__patch']
    trace?: never
  }
  '/entity/action/count': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Count
     * @description Return the number of matching records.
     */
    post: operations['count_entity_action_count_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/action/sum': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Sum
     * @description Return the total of a numeric Field, ignoring null values, or zero when nothing matches.
     */
    post: operations['sum_entity_action_sum_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/action/min': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Min
     * @description Return the smallest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['min_entity_action_min_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/action/max': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Max
     * @description Return the largest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['max_entity_action_max_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/action/truncate': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Truncate
     * @description Remove every record of the Entity, keep its Table, and return the deleted count.
     */
    delete: operations['truncate_entity_action_truncate_delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/position/add': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Add
     * @description Store one new Entity instance and return the stored Entity, including generated values.
     */
    post: operations['add_entity_position_add_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/position/update': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    /**
     * Update
     * @description Replace every mutable Field of the stored record of an Entity instance; None when it does not exist.
     */
    put: operations['update_entity_position_update_put']
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/position/list': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * List
     * @description Return the matching Entity instances; a zero or negative limit means no limit.
     */
    post: operations['list_entity_position_list_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/position/get_by_id/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Get By Id
     * @description Return the Entity with that id, or None when no record exists.
     */
    get: operations['get_by_id_entity_position_get_by_id__id__get']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/position/delete/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Delete
     * @description Remove the record and return the deleted Entity, or None when no record exists.
     */
    delete: operations['delete_entity_position_delete__id__delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/position/enable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Enable
     * @description Set only is_active to true and return the final Entity, or None when no record exists.
     */
    patch: operations['enable_entity_position_enable__id__patch']
    trace?: never
  }
  '/entity/position/disable/{id}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    /**
     * Disable
     * @description Set only is_active to false and return the final Entity, or None when no record exists.
     */
    patch: operations['disable_entity_position_disable__id__patch']
    trace?: never
  }
  '/entity/position/count': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Count
     * @description Return the number of matching records.
     */
    post: operations['count_entity_position_count_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/position/sum': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Sum
     * @description Return the total of a numeric Field, ignoring null values, or zero when nothing matches.
     */
    post: operations['sum_entity_position_sum_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/position/min': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Min
     * @description Return the smallest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['min_entity_position_min_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/position/max': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Max
     * @description Return the largest non-null value of a comparable Field, or None when nothing matches.
     */
    post: operations['max_entity_position_max_post']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/entity/position/truncate': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Truncate
     * @description Remove every record of the Entity, keep its Table, and return the deleted count.
     */
    delete: operations['truncate_entity_position_truncate_delete']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
}
export type webhooks = Record<string, never>
export interface components {
  schemas: {
    /** Body_add_entity_account_add_post */
    Body_add_entity_account_add_post: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_add_entity_account_group_add_post */
    Body_add_entity_account_group_add_post: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_add_entity_action_add_post */
    Body_add_entity_action_add_post: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_add_entity_action_group_add_post */
    Body_add_entity_action_group_add_post: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_add_entity_asset_add_post */
    Body_add_entity_asset_add_post: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_add_entity_broker_add_post */
    Body_add_entity_broker_add_post: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_add_entity_currency_add_post */
    Body_add_entity_currency_add_post: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_add_entity_instance_add_post */
    Body_add_entity_instance_add_post: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_add_entity_partial_group_add_post */
    Body_add_entity_partial_group_add_post: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_add_entity_partial_rule_add_post */
    Body_add_entity_partial_rule_add_post: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_add_entity_position_add_post */
    Body_add_entity_position_add_post: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_add_entity_trading_platform_add_post */
    Body_add_entity_trading_platform_add_post: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_add_entity_trailing_group_add_post */
    Body_add_entity_trailing_group_add_post: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_add_entity_trailing_rule_add_post */
    Body_add_entity_trailing_rule_add_post: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_add_entity_user_add_post */
    Body_add_entity_user_add_post: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_count_entity_account_count_post */
    Body_count_entity_account_count_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_count_entity_account_group_count_post */
    Body_count_entity_account_group_count_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_count_entity_action_count_post */
    Body_count_entity_action_count_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_count_entity_action_group_count_post */
    Body_count_entity_action_group_count_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_count_entity_asset_count_post */
    Body_count_entity_asset_count_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_count_entity_broker_count_post */
    Body_count_entity_broker_count_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_count_entity_currency_count_post */
    Body_count_entity_currency_count_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_count_entity_instance_count_post */
    Body_count_entity_instance_count_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_count_entity_partial_group_count_post */
    Body_count_entity_partial_group_count_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_count_entity_partial_rule_count_post */
    Body_count_entity_partial_rule_count_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_count_entity_position_count_post */
    Body_count_entity_position_count_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_count_entity_trading_platform_count_post */
    Body_count_entity_trading_platform_count_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_count_entity_trailing_group_count_post */
    Body_count_entity_trailing_group_count_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_count_entity_trailing_rule_count_post */
    Body_count_entity_trailing_rule_count_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_count_entity_user_count_post */
    Body_count_entity_user_count_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_disable_entity_account_disable__id__patch */
    Body_disable_entity_account_disable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_disable_entity_account_group_disable__id__patch */
    Body_disable_entity_account_group_disable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_disable_entity_action_disable__id__patch */
    Body_disable_entity_action_disable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_disable_entity_action_group_disable__id__patch */
    Body_disable_entity_action_group_disable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_disable_entity_asset_disable__id__patch */
    Body_disable_entity_asset_disable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_disable_entity_broker_disable__id__patch */
    Body_disable_entity_broker_disable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_disable_entity_currency_disable__id__patch */
    Body_disable_entity_currency_disable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_disable_entity_instance_disable__id__patch */
    Body_disable_entity_instance_disable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_disable_entity_partial_group_disable__id__patch */
    Body_disable_entity_partial_group_disable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_disable_entity_partial_rule_disable__id__patch */
    Body_disable_entity_partial_rule_disable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_disable_entity_position_disable__id__patch */
    Body_disable_entity_position_disable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_disable_entity_trading_platform_disable__id__patch */
    Body_disable_entity_trading_platform_disable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_disable_entity_trailing_group_disable__id__patch */
    Body_disable_entity_trailing_group_disable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_disable_entity_trailing_rule_disable__id__patch */
    Body_disable_entity_trailing_rule_disable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_disable_entity_user_disable__id__patch */
    Body_disable_entity_user_disable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_enable_entity_account_enable__id__patch */
    Body_enable_entity_account_enable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_enable_entity_account_group_enable__id__patch */
    Body_enable_entity_account_group_enable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_enable_entity_action_enable__id__patch */
    Body_enable_entity_action_enable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_enable_entity_action_group_enable__id__patch */
    Body_enable_entity_action_group_enable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_enable_entity_asset_enable__id__patch */
    Body_enable_entity_asset_enable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_enable_entity_broker_enable__id__patch */
    Body_enable_entity_broker_enable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_enable_entity_currency_enable__id__patch */
    Body_enable_entity_currency_enable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_enable_entity_instance_enable__id__patch */
    Body_enable_entity_instance_enable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_enable_entity_partial_group_enable__id__patch */
    Body_enable_entity_partial_group_enable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_enable_entity_partial_rule_enable__id__patch */
    Body_enable_entity_partial_rule_enable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_enable_entity_position_enable__id__patch */
    Body_enable_entity_position_enable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_enable_entity_trading_platform_enable__id__patch */
    Body_enable_entity_trading_platform_enable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_enable_entity_trailing_group_enable__id__patch */
    Body_enable_entity_trailing_group_enable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_enable_entity_trailing_rule_enable__id__patch */
    Body_enable_entity_trailing_rule_enable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_enable_entity_user_enable__id__patch */
    Body_enable_entity_user_enable__id__patch: {
      /** Instance */
      instance?: string | null
    }
    /** Body_list_entity_account_group_list_post */
    Body_list_entity_account_group_list_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Orders */
      orders?: components['schemas']['OrderBody'][] | null
      /** Limit */
      limit?: number | null
      /** Instance */
      instance?: string | null
    }
    /** Body_list_entity_account_list_post */
    Body_list_entity_account_list_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Orders */
      orders?: components['schemas']['OrderBody'][] | null
      /** Limit */
      limit?: number | null
      /** Instance */
      instance?: string | null
    }
    /** Body_list_entity_action_group_list_post */
    Body_list_entity_action_group_list_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Orders */
      orders?: components['schemas']['OrderBody'][] | null
      /** Limit */
      limit?: number | null
      /** Instance */
      instance?: string | null
    }
    /** Body_list_entity_action_list_post */
    Body_list_entity_action_list_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Orders */
      orders?: components['schemas']['OrderBody'][] | null
      /** Limit */
      limit?: number | null
      /** Instance */
      instance?: string | null
    }
    /** Body_list_entity_asset_list_post */
    Body_list_entity_asset_list_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Orders */
      orders?: components['schemas']['OrderBody'][] | null
      /** Limit */
      limit?: number | null
      /** Instance */
      instance?: string | null
    }
    /** Body_list_entity_broker_list_post */
    Body_list_entity_broker_list_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Orders */
      orders?: components['schemas']['OrderBody'][] | null
      /** Limit */
      limit?: number | null
      /** Instance */
      instance?: string | null
    }
    /** Body_list_entity_currency_list_post */
    Body_list_entity_currency_list_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Orders */
      orders?: components['schemas']['OrderBody'][] | null
      /** Limit */
      limit?: number | null
      /** Instance */
      instance?: string | null
    }
    /** Body_list_entity_instance_list_post */
    Body_list_entity_instance_list_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Orders */
      orders?: components['schemas']['OrderBody'][] | null
      /** Limit */
      limit?: number | null
      /** Instance */
      instance?: string | null
    }
    /** Body_list_entity_partial_group_list_post */
    Body_list_entity_partial_group_list_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Orders */
      orders?: components['schemas']['OrderBody'][] | null
      /** Limit */
      limit?: number | null
      /** Instance */
      instance?: string | null
    }
    /** Body_list_entity_partial_rule_list_post */
    Body_list_entity_partial_rule_list_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Orders */
      orders?: components['schemas']['OrderBody'][] | null
      /** Limit */
      limit?: number | null
      /** Instance */
      instance?: string | null
    }
    /** Body_list_entity_position_list_post */
    Body_list_entity_position_list_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Orders */
      orders?: components['schemas']['OrderBody'][] | null
      /** Limit */
      limit?: number | null
      /** Instance */
      instance?: string | null
    }
    /** Body_list_entity_trading_platform_list_post */
    Body_list_entity_trading_platform_list_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Orders */
      orders?: components['schemas']['OrderBody'][] | null
      /** Limit */
      limit?: number | null
      /** Instance */
      instance?: string | null
    }
    /** Body_list_entity_trailing_group_list_post */
    Body_list_entity_trailing_group_list_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Orders */
      orders?: components['schemas']['OrderBody'][] | null
      /** Limit */
      limit?: number | null
      /** Instance */
      instance?: string | null
    }
    /** Body_list_entity_trailing_rule_list_post */
    Body_list_entity_trailing_rule_list_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Orders */
      orders?: components['schemas']['OrderBody'][] | null
      /** Limit */
      limit?: number | null
      /** Instance */
      instance?: string | null
    }
    /** Body_list_entity_user_list_post */
    Body_list_entity_user_list_post: {
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Orders */
      orders?: components['schemas']['OrderBody'][] | null
      /** Limit */
      limit?: number | null
      /** Instance */
      instance?: string | null
    }
    /** Body_max_entity_account_group_max_post */
    Body_max_entity_account_group_max_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_max_entity_account_max_post */
    Body_max_entity_account_max_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_max_entity_action_group_max_post */
    Body_max_entity_action_group_max_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_max_entity_action_max_post */
    Body_max_entity_action_max_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_max_entity_asset_max_post */
    Body_max_entity_asset_max_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_max_entity_broker_max_post */
    Body_max_entity_broker_max_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_max_entity_currency_max_post */
    Body_max_entity_currency_max_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_max_entity_instance_max_post */
    Body_max_entity_instance_max_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_max_entity_partial_group_max_post */
    Body_max_entity_partial_group_max_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_max_entity_partial_rule_max_post */
    Body_max_entity_partial_rule_max_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_max_entity_position_max_post */
    Body_max_entity_position_max_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_max_entity_trading_platform_max_post */
    Body_max_entity_trading_platform_max_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_max_entity_trailing_group_max_post */
    Body_max_entity_trailing_group_max_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_max_entity_trailing_rule_max_post */
    Body_max_entity_trailing_rule_max_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_max_entity_user_max_post */
    Body_max_entity_user_max_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_min_entity_account_group_min_post */
    Body_min_entity_account_group_min_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_min_entity_account_min_post */
    Body_min_entity_account_min_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_min_entity_action_group_min_post */
    Body_min_entity_action_group_min_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_min_entity_action_min_post */
    Body_min_entity_action_min_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_min_entity_asset_min_post */
    Body_min_entity_asset_min_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_min_entity_broker_min_post */
    Body_min_entity_broker_min_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_min_entity_currency_min_post */
    Body_min_entity_currency_min_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_min_entity_instance_min_post */
    Body_min_entity_instance_min_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_min_entity_partial_group_min_post */
    Body_min_entity_partial_group_min_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_min_entity_partial_rule_min_post */
    Body_min_entity_partial_rule_min_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_min_entity_position_min_post */
    Body_min_entity_position_min_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_min_entity_trading_platform_min_post */
    Body_min_entity_trading_platform_min_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_min_entity_trailing_group_min_post */
    Body_min_entity_trailing_group_min_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_min_entity_trailing_rule_min_post */
    Body_min_entity_trailing_rule_min_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_min_entity_user_min_post */
    Body_min_entity_user_min_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_sum_entity_account_group_sum_post */
    Body_sum_entity_account_group_sum_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_sum_entity_account_sum_post */
    Body_sum_entity_account_sum_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_sum_entity_action_group_sum_post */
    Body_sum_entity_action_group_sum_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_sum_entity_action_sum_post */
    Body_sum_entity_action_sum_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_sum_entity_asset_sum_post */
    Body_sum_entity_asset_sum_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_sum_entity_broker_sum_post */
    Body_sum_entity_broker_sum_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_sum_entity_currency_sum_post */
    Body_sum_entity_currency_sum_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_sum_entity_instance_sum_post */
    Body_sum_entity_instance_sum_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_sum_entity_partial_group_sum_post */
    Body_sum_entity_partial_group_sum_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_sum_entity_partial_rule_sum_post */
    Body_sum_entity_partial_rule_sum_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_sum_entity_position_sum_post */
    Body_sum_entity_position_sum_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_sum_entity_trading_platform_sum_post */
    Body_sum_entity_trading_platform_sum_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_sum_entity_trailing_group_sum_post */
    Body_sum_entity_trailing_group_sum_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_sum_entity_trailing_rule_sum_post */
    Body_sum_entity_trailing_rule_sum_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_sum_entity_user_sum_post */
    Body_sum_entity_user_sum_post: {
      /** Field */
      field: string
      /** Filters */
      filters?: components['schemas']['FilterBody'][] | null
      /** Combination */
      combination?: string | null
      /** Instance */
      instance?: string | null
    }
    /** Body_update_entity_account_group_update_put */
    Body_update_entity_account_group_update_put: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_update_entity_account_update_put */
    Body_update_entity_account_update_put: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_update_entity_action_group_update_put */
    Body_update_entity_action_group_update_put: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_update_entity_action_update_put */
    Body_update_entity_action_update_put: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_update_entity_asset_update_put */
    Body_update_entity_asset_update_put: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_update_entity_broker_update_put */
    Body_update_entity_broker_update_put: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_update_entity_currency_update_put */
    Body_update_entity_currency_update_put: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_update_entity_instance_update_put */
    Body_update_entity_instance_update_put: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_update_entity_partial_group_update_put */
    Body_update_entity_partial_group_update_put: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_update_entity_partial_rule_update_put */
    Body_update_entity_partial_rule_update_put: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_update_entity_position_update_put */
    Body_update_entity_position_update_put: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_update_entity_trading_platform_update_put */
    Body_update_entity_trading_platform_update_put: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_update_entity_trailing_group_update_put */
    Body_update_entity_trailing_group_update_put: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_update_entity_trailing_rule_update_put */
    Body_update_entity_trailing_rule_update_put: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /** Body_update_entity_user_update_put */
    Body_update_entity_user_update_put: {
      /** Entity */
      entity: {
        [key: string]: unknown
      }
      /** Instance */
      instance?: string | null
    }
    /**
     * FilterBody
     * @description The transport form of a Filter.
     */
    FilterBody: {
      /** Field */
      field: string
      /** Operator */
      operator: string
      /** Value */
      value?: unknown
    }
    /** HTTPValidationError */
    HTTPValidationError: {
      /** Detail */
      detail?: components['schemas']['ValidationError'][]
    }
    /**
     * OrderBody
     * @description The transport form of an Order.
     */
    OrderBody: {
      /** Field */
      field: string
      /**
       * Direction
       * @default ASCENDING
       */
      direction: string
    }
    /** ValidationError */
    ValidationError: {
      /** Location */
      loc: (string | number)[]
      /** Message */
      msg: string
      /** Error Type */
      type: string
      /** Input */
      input?: unknown
      /** Context */
      ctx?: Record<string, never>
    }
  }
  responses: never
  parameters: never
  requestBodies: never
  headers: never
  pathItems: never
}
export type $defs = Record<string, never>
export interface operations {
  add_entity_user_add_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_add_entity_user_add_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  update_entity_user_update_put: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_update_entity_user_update_put']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  list_entity_user_list_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_list_entity_user_list_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  get_by_id_entity_user_get_by_id__id__get: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  delete_entity_user_delete__id__delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  enable_entity_user_enable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_enable_entity_user_enable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  disable_entity_user_disable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_disable_entity_user_disable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  count_entity_user_count_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_count_entity_user_count_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  sum_entity_user_sum_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_sum_entity_user_sum_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  min_entity_user_min_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_min_entity_user_min_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  max_entity_user_max_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_max_entity_user_max_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  truncate_entity_user_truncate_delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  add_entity_trading_platform_add_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_add_entity_trading_platform_add_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  update_entity_trading_platform_update_put: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_update_entity_trading_platform_update_put']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  list_entity_trading_platform_list_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_list_entity_trading_platform_list_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  get_by_id_entity_trading_platform_get_by_id__id__get: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  delete_entity_trading_platform_delete__id__delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  enable_entity_trading_platform_enable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_enable_entity_trading_platform_enable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  disable_entity_trading_platform_disable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_disable_entity_trading_platform_disable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  count_entity_trading_platform_count_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_count_entity_trading_platform_count_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  sum_entity_trading_platform_sum_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_sum_entity_trading_platform_sum_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  min_entity_trading_platform_min_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_min_entity_trading_platform_min_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  max_entity_trading_platform_max_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_max_entity_trading_platform_max_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  truncate_entity_trading_platform_truncate_delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  add_entity_instance_add_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_add_entity_instance_add_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  update_entity_instance_update_put: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_update_entity_instance_update_put']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  list_entity_instance_list_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_list_entity_instance_list_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  get_by_id_entity_instance_get_by_id__id__get: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  delete_entity_instance_delete__id__delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  enable_entity_instance_enable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_enable_entity_instance_enable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  disable_entity_instance_disable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_disable_entity_instance_disable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  count_entity_instance_count_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_count_entity_instance_count_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  sum_entity_instance_sum_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_sum_entity_instance_sum_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  min_entity_instance_min_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_min_entity_instance_min_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  max_entity_instance_max_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_max_entity_instance_max_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  truncate_entity_instance_truncate_delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  add_entity_currency_add_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_add_entity_currency_add_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  update_entity_currency_update_put: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_update_entity_currency_update_put']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  list_entity_currency_list_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_list_entity_currency_list_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  get_by_id_entity_currency_get_by_id__id__get: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  delete_entity_currency_delete__id__delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  enable_entity_currency_enable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_enable_entity_currency_enable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  disable_entity_currency_disable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_disable_entity_currency_disable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  count_entity_currency_count_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_count_entity_currency_count_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  sum_entity_currency_sum_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_sum_entity_currency_sum_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  min_entity_currency_min_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_min_entity_currency_min_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  max_entity_currency_max_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_max_entity_currency_max_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  truncate_entity_currency_truncate_delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  add_entity_broker_add_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_add_entity_broker_add_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  update_entity_broker_update_put: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_update_entity_broker_update_put']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  list_entity_broker_list_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_list_entity_broker_list_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  get_by_id_entity_broker_get_by_id__id__get: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  delete_entity_broker_delete__id__delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  enable_entity_broker_enable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_enable_entity_broker_enable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  disable_entity_broker_disable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_disable_entity_broker_disable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  count_entity_broker_count_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_count_entity_broker_count_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  sum_entity_broker_sum_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_sum_entity_broker_sum_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  min_entity_broker_min_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_min_entity_broker_min_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  max_entity_broker_max_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_max_entity_broker_max_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  truncate_entity_broker_truncate_delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  add_entity_asset_add_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_add_entity_asset_add_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  update_entity_asset_update_put: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_update_entity_asset_update_put']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  list_entity_asset_list_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_list_entity_asset_list_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  get_by_id_entity_asset_get_by_id__id__get: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  delete_entity_asset_delete__id__delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  enable_entity_asset_enable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_enable_entity_asset_enable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  disable_entity_asset_disable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_disable_entity_asset_disable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  count_entity_asset_count_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_count_entity_asset_count_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  sum_entity_asset_sum_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_sum_entity_asset_sum_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  min_entity_asset_min_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_min_entity_asset_min_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  max_entity_asset_max_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_max_entity_asset_max_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  truncate_entity_asset_truncate_delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  add_entity_account_group_add_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_add_entity_account_group_add_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  update_entity_account_group_update_put: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_update_entity_account_group_update_put']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  list_entity_account_group_list_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_list_entity_account_group_list_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  get_by_id_entity_account_group_get_by_id__id__get: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  delete_entity_account_group_delete__id__delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  enable_entity_account_group_enable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_enable_entity_account_group_enable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  disable_entity_account_group_disable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_disable_entity_account_group_disable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  count_entity_account_group_count_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_count_entity_account_group_count_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  sum_entity_account_group_sum_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_sum_entity_account_group_sum_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  min_entity_account_group_min_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_min_entity_account_group_min_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  max_entity_account_group_max_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_max_entity_account_group_max_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  truncate_entity_account_group_truncate_delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  add_entity_account_add_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_add_entity_account_add_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  update_entity_account_update_put: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_update_entity_account_update_put']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  list_entity_account_list_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_list_entity_account_list_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  get_by_id_entity_account_get_by_id__id__get: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  delete_entity_account_delete__id__delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  enable_entity_account_enable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_enable_entity_account_enable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  disable_entity_account_disable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_disable_entity_account_disable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  count_entity_account_count_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_count_entity_account_count_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  sum_entity_account_sum_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_sum_entity_account_sum_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  min_entity_account_min_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_min_entity_account_min_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  max_entity_account_max_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_max_entity_account_max_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  truncate_entity_account_truncate_delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  add_entity_trailing_group_add_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_add_entity_trailing_group_add_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  update_entity_trailing_group_update_put: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_update_entity_trailing_group_update_put']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  list_entity_trailing_group_list_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_list_entity_trailing_group_list_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  get_by_id_entity_trailing_group_get_by_id__id__get: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  delete_entity_trailing_group_delete__id__delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  enable_entity_trailing_group_enable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_enable_entity_trailing_group_enable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  disable_entity_trailing_group_disable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_disable_entity_trailing_group_disable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  count_entity_trailing_group_count_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_count_entity_trailing_group_count_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  sum_entity_trailing_group_sum_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_sum_entity_trailing_group_sum_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  min_entity_trailing_group_min_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_min_entity_trailing_group_min_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  max_entity_trailing_group_max_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_max_entity_trailing_group_max_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  truncate_entity_trailing_group_truncate_delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  add_entity_trailing_rule_add_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_add_entity_trailing_rule_add_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  update_entity_trailing_rule_update_put: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_update_entity_trailing_rule_update_put']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  list_entity_trailing_rule_list_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_list_entity_trailing_rule_list_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  get_by_id_entity_trailing_rule_get_by_id__id__get: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  delete_entity_trailing_rule_delete__id__delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  enable_entity_trailing_rule_enable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_enable_entity_trailing_rule_enable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  disable_entity_trailing_rule_disable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_disable_entity_trailing_rule_disable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  count_entity_trailing_rule_count_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_count_entity_trailing_rule_count_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  sum_entity_trailing_rule_sum_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_sum_entity_trailing_rule_sum_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  min_entity_trailing_rule_min_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_min_entity_trailing_rule_min_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  max_entity_trailing_rule_max_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_max_entity_trailing_rule_max_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  truncate_entity_trailing_rule_truncate_delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  add_entity_partial_group_add_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_add_entity_partial_group_add_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  update_entity_partial_group_update_put: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_update_entity_partial_group_update_put']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  list_entity_partial_group_list_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_list_entity_partial_group_list_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  get_by_id_entity_partial_group_get_by_id__id__get: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  delete_entity_partial_group_delete__id__delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  enable_entity_partial_group_enable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_enable_entity_partial_group_enable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  disable_entity_partial_group_disable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_disable_entity_partial_group_disable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  count_entity_partial_group_count_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_count_entity_partial_group_count_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  sum_entity_partial_group_sum_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_sum_entity_partial_group_sum_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  min_entity_partial_group_min_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_min_entity_partial_group_min_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  max_entity_partial_group_max_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_max_entity_partial_group_max_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  truncate_entity_partial_group_truncate_delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  add_entity_partial_rule_add_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_add_entity_partial_rule_add_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  update_entity_partial_rule_update_put: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_update_entity_partial_rule_update_put']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  list_entity_partial_rule_list_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_list_entity_partial_rule_list_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  get_by_id_entity_partial_rule_get_by_id__id__get: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  delete_entity_partial_rule_delete__id__delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  enable_entity_partial_rule_enable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_enable_entity_partial_rule_enable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  disable_entity_partial_rule_disable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_disable_entity_partial_rule_disable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  count_entity_partial_rule_count_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_count_entity_partial_rule_count_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  sum_entity_partial_rule_sum_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_sum_entity_partial_rule_sum_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  min_entity_partial_rule_min_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_min_entity_partial_rule_min_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  max_entity_partial_rule_max_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_max_entity_partial_rule_max_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  truncate_entity_partial_rule_truncate_delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  add_entity_action_group_add_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_add_entity_action_group_add_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  update_entity_action_group_update_put: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_update_entity_action_group_update_put']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  list_entity_action_group_list_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_list_entity_action_group_list_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  get_by_id_entity_action_group_get_by_id__id__get: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  delete_entity_action_group_delete__id__delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  enable_entity_action_group_enable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_enable_entity_action_group_enable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  disable_entity_action_group_disable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_disable_entity_action_group_disable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  count_entity_action_group_count_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_count_entity_action_group_count_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  sum_entity_action_group_sum_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_sum_entity_action_group_sum_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  min_entity_action_group_min_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_min_entity_action_group_min_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  max_entity_action_group_max_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_max_entity_action_group_max_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  truncate_entity_action_group_truncate_delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  add_entity_action_add_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_add_entity_action_add_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  update_entity_action_update_put: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_update_entity_action_update_put']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  list_entity_action_list_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_list_entity_action_list_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  get_by_id_entity_action_get_by_id__id__get: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  delete_entity_action_delete__id__delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  enable_entity_action_enable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_enable_entity_action_enable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  disable_entity_action_disable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_disable_entity_action_disable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  count_entity_action_count_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_count_entity_action_count_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  sum_entity_action_sum_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_sum_entity_action_sum_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  min_entity_action_min_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_min_entity_action_min_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  max_entity_action_max_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_max_entity_action_max_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  truncate_entity_action_truncate_delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  add_entity_position_add_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_add_entity_position_add_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  update_entity_position_update_put: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_update_entity_position_update_put']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  list_entity_position_list_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_list_entity_position_list_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  get_by_id_entity_position_get_by_id__id__get: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  delete_entity_position_delete__id__delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  enable_entity_position_enable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_enable_entity_position_enable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  disable_entity_position_disable__id__patch: {
    parameters: {
      query?: never
      header?: never
      path: {
        id: number
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_disable_entity_position_disable__id__patch']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  count_entity_position_count_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': components['schemas']['Body_count_entity_position_count_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  sum_entity_position_sum_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_sum_entity_position_sum_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  min_entity_position_min_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_min_entity_position_min_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  max_entity_position_max_post: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': components['schemas']['Body_max_entity_position_max_post']
      }
    }
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
  truncate_entity_position_truncate_delete: {
    parameters: {
      query?: {
        instance?: string | null
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': unknown
        }
      }
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': components['schemas']['HTTPValidationError']
        }
      }
    }
  }
}
