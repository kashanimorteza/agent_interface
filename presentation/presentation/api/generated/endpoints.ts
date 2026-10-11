// Generated from the API description. Regenerate; do not edit.

export const endpoints = {
  entity: {
    user: {
      add: {
        method: 'post',
        path: '/entity/user/add',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      update: {
        method: 'put',
        path: '/entity/user/update',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      list: {
        method: 'post',
        path: '/entity/user/list',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'orders', in: 'body', required: false },
          { name: 'limit', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      get_by_id: {
        method: 'get',
        path: '/entity/user/get_by_id/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      delete: {
        method: 'delete',
        path: '/entity/user/delete/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      enable: {
        method: 'patch',
        path: '/entity/user/enable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      disable: {
        method: 'patch',
        path: '/entity/user/disable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      count: {
        method: 'post',
        path: '/entity/user/count',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      sum: {
        method: 'post',
        path: '/entity/user/sum',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      min: {
        method: 'post',
        path: '/entity/user/min',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      max: {
        method: 'post',
        path: '/entity/user/max',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      truncate: {
        method: 'delete',
        path: '/entity/user/truncate',
        parameters: [{ name: 'instance', in: 'query', required: false }],
      },
    },
    trading_platform: {
      add: {
        method: 'post',
        path: '/entity/trading_platform/add',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      update: {
        method: 'put',
        path: '/entity/trading_platform/update',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      list: {
        method: 'post',
        path: '/entity/trading_platform/list',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'orders', in: 'body', required: false },
          { name: 'limit', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      get_by_id: {
        method: 'get',
        path: '/entity/trading_platform/get_by_id/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      delete: {
        method: 'delete',
        path: '/entity/trading_platform/delete/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      enable: {
        method: 'patch',
        path: '/entity/trading_platform/enable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      disable: {
        method: 'patch',
        path: '/entity/trading_platform/disable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      count: {
        method: 'post',
        path: '/entity/trading_platform/count',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      sum: {
        method: 'post',
        path: '/entity/trading_platform/sum',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      min: {
        method: 'post',
        path: '/entity/trading_platform/min',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      max: {
        method: 'post',
        path: '/entity/trading_platform/max',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      truncate: {
        method: 'delete',
        path: '/entity/trading_platform/truncate',
        parameters: [{ name: 'instance', in: 'query', required: false }],
      },
    },
    instance: {
      add: {
        method: 'post',
        path: '/entity/instance/add',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      update: {
        method: 'put',
        path: '/entity/instance/update',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      list: {
        method: 'post',
        path: '/entity/instance/list',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'orders', in: 'body', required: false },
          { name: 'limit', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      get_by_id: {
        method: 'get',
        path: '/entity/instance/get_by_id/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      delete: {
        method: 'delete',
        path: '/entity/instance/delete/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      enable: {
        method: 'patch',
        path: '/entity/instance/enable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      disable: {
        method: 'patch',
        path: '/entity/instance/disable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      count: {
        method: 'post',
        path: '/entity/instance/count',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      sum: {
        method: 'post',
        path: '/entity/instance/sum',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      min: {
        method: 'post',
        path: '/entity/instance/min',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      max: {
        method: 'post',
        path: '/entity/instance/max',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      truncate: {
        method: 'delete',
        path: '/entity/instance/truncate',
        parameters: [{ name: 'instance', in: 'query', required: false }],
      },
    },
    currency: {
      add: {
        method: 'post',
        path: '/entity/currency/add',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      update: {
        method: 'put',
        path: '/entity/currency/update',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      list: {
        method: 'post',
        path: '/entity/currency/list',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'orders', in: 'body', required: false },
          { name: 'limit', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      get_by_id: {
        method: 'get',
        path: '/entity/currency/get_by_id/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      delete: {
        method: 'delete',
        path: '/entity/currency/delete/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      enable: {
        method: 'patch',
        path: '/entity/currency/enable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      disable: {
        method: 'patch',
        path: '/entity/currency/disable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      count: {
        method: 'post',
        path: '/entity/currency/count',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      sum: {
        method: 'post',
        path: '/entity/currency/sum',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      min: {
        method: 'post',
        path: '/entity/currency/min',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      max: {
        method: 'post',
        path: '/entity/currency/max',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      truncate: {
        method: 'delete',
        path: '/entity/currency/truncate',
        parameters: [{ name: 'instance', in: 'query', required: false }],
      },
    },
    broker: {
      add: {
        method: 'post',
        path: '/entity/broker/add',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      update: {
        method: 'put',
        path: '/entity/broker/update',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      list: {
        method: 'post',
        path: '/entity/broker/list',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'orders', in: 'body', required: false },
          { name: 'limit', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      get_by_id: {
        method: 'get',
        path: '/entity/broker/get_by_id/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      delete: {
        method: 'delete',
        path: '/entity/broker/delete/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      enable: {
        method: 'patch',
        path: '/entity/broker/enable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      disable: {
        method: 'patch',
        path: '/entity/broker/disable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      count: {
        method: 'post',
        path: '/entity/broker/count',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      sum: {
        method: 'post',
        path: '/entity/broker/sum',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      min: {
        method: 'post',
        path: '/entity/broker/min',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      max: {
        method: 'post',
        path: '/entity/broker/max',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      truncate: {
        method: 'delete',
        path: '/entity/broker/truncate',
        parameters: [{ name: 'instance', in: 'query', required: false }],
      },
    },
    asset: {
      add: {
        method: 'post',
        path: '/entity/asset/add',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      update: {
        method: 'put',
        path: '/entity/asset/update',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      list: {
        method: 'post',
        path: '/entity/asset/list',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'orders', in: 'body', required: false },
          { name: 'limit', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      get_by_id: {
        method: 'get',
        path: '/entity/asset/get_by_id/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      delete: {
        method: 'delete',
        path: '/entity/asset/delete/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      enable: {
        method: 'patch',
        path: '/entity/asset/enable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      disable: {
        method: 'patch',
        path: '/entity/asset/disable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      count: {
        method: 'post',
        path: '/entity/asset/count',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      sum: {
        method: 'post',
        path: '/entity/asset/sum',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      min: {
        method: 'post',
        path: '/entity/asset/min',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      max: {
        method: 'post',
        path: '/entity/asset/max',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      truncate: {
        method: 'delete',
        path: '/entity/asset/truncate',
        parameters: [{ name: 'instance', in: 'query', required: false }],
      },
    },
    account_group: {
      add: {
        method: 'post',
        path: '/entity/account_group/add',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      update: {
        method: 'put',
        path: '/entity/account_group/update',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      list: {
        method: 'post',
        path: '/entity/account_group/list',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'orders', in: 'body', required: false },
          { name: 'limit', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      get_by_id: {
        method: 'get',
        path: '/entity/account_group/get_by_id/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      delete: {
        method: 'delete',
        path: '/entity/account_group/delete/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      enable: {
        method: 'patch',
        path: '/entity/account_group/enable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      disable: {
        method: 'patch',
        path: '/entity/account_group/disable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      count: {
        method: 'post',
        path: '/entity/account_group/count',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      sum: {
        method: 'post',
        path: '/entity/account_group/sum',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      min: {
        method: 'post',
        path: '/entity/account_group/min',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      max: {
        method: 'post',
        path: '/entity/account_group/max',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      truncate: {
        method: 'delete',
        path: '/entity/account_group/truncate',
        parameters: [{ name: 'instance', in: 'query', required: false }],
      },
    },
    account: {
      add: {
        method: 'post',
        path: '/entity/account/add',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      update: {
        method: 'put',
        path: '/entity/account/update',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      list: {
        method: 'post',
        path: '/entity/account/list',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'orders', in: 'body', required: false },
          { name: 'limit', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      get_by_id: {
        method: 'get',
        path: '/entity/account/get_by_id/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      delete: {
        method: 'delete',
        path: '/entity/account/delete/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      enable: {
        method: 'patch',
        path: '/entity/account/enable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      disable: {
        method: 'patch',
        path: '/entity/account/disable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      count: {
        method: 'post',
        path: '/entity/account/count',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      sum: {
        method: 'post',
        path: '/entity/account/sum',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      min: {
        method: 'post',
        path: '/entity/account/min',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      max: {
        method: 'post',
        path: '/entity/account/max',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      truncate: {
        method: 'delete',
        path: '/entity/account/truncate',
        parameters: [{ name: 'instance', in: 'query', required: false }],
      },
    },
    trailing_group: {
      add: {
        method: 'post',
        path: '/entity/trailing_group/add',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      update: {
        method: 'put',
        path: '/entity/trailing_group/update',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      list: {
        method: 'post',
        path: '/entity/trailing_group/list',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'orders', in: 'body', required: false },
          { name: 'limit', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      get_by_id: {
        method: 'get',
        path: '/entity/trailing_group/get_by_id/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      delete: {
        method: 'delete',
        path: '/entity/trailing_group/delete/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      enable: {
        method: 'patch',
        path: '/entity/trailing_group/enable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      disable: {
        method: 'patch',
        path: '/entity/trailing_group/disable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      count: {
        method: 'post',
        path: '/entity/trailing_group/count',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      sum: {
        method: 'post',
        path: '/entity/trailing_group/sum',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      min: {
        method: 'post',
        path: '/entity/trailing_group/min',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      max: {
        method: 'post',
        path: '/entity/trailing_group/max',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      truncate: {
        method: 'delete',
        path: '/entity/trailing_group/truncate',
        parameters: [{ name: 'instance', in: 'query', required: false }],
      },
    },
    trailing_rule: {
      add: {
        method: 'post',
        path: '/entity/trailing_rule/add',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      update: {
        method: 'put',
        path: '/entity/trailing_rule/update',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      list: {
        method: 'post',
        path: '/entity/trailing_rule/list',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'orders', in: 'body', required: false },
          { name: 'limit', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      get_by_id: {
        method: 'get',
        path: '/entity/trailing_rule/get_by_id/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      delete: {
        method: 'delete',
        path: '/entity/trailing_rule/delete/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      enable: {
        method: 'patch',
        path: '/entity/trailing_rule/enable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      disable: {
        method: 'patch',
        path: '/entity/trailing_rule/disable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      count: {
        method: 'post',
        path: '/entity/trailing_rule/count',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      sum: {
        method: 'post',
        path: '/entity/trailing_rule/sum',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      min: {
        method: 'post',
        path: '/entity/trailing_rule/min',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      max: {
        method: 'post',
        path: '/entity/trailing_rule/max',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      truncate: {
        method: 'delete',
        path: '/entity/trailing_rule/truncate',
        parameters: [{ name: 'instance', in: 'query', required: false }],
      },
    },
    partial_group: {
      add: {
        method: 'post',
        path: '/entity/partial_group/add',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      update: {
        method: 'put',
        path: '/entity/partial_group/update',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      list: {
        method: 'post',
        path: '/entity/partial_group/list',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'orders', in: 'body', required: false },
          { name: 'limit', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      get_by_id: {
        method: 'get',
        path: '/entity/partial_group/get_by_id/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      delete: {
        method: 'delete',
        path: '/entity/partial_group/delete/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      enable: {
        method: 'patch',
        path: '/entity/partial_group/enable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      disable: {
        method: 'patch',
        path: '/entity/partial_group/disable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      count: {
        method: 'post',
        path: '/entity/partial_group/count',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      sum: {
        method: 'post',
        path: '/entity/partial_group/sum',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      min: {
        method: 'post',
        path: '/entity/partial_group/min',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      max: {
        method: 'post',
        path: '/entity/partial_group/max',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      truncate: {
        method: 'delete',
        path: '/entity/partial_group/truncate',
        parameters: [{ name: 'instance', in: 'query', required: false }],
      },
    },
    partial_rule: {
      add: {
        method: 'post',
        path: '/entity/partial_rule/add',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      update: {
        method: 'put',
        path: '/entity/partial_rule/update',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      list: {
        method: 'post',
        path: '/entity/partial_rule/list',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'orders', in: 'body', required: false },
          { name: 'limit', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      get_by_id: {
        method: 'get',
        path: '/entity/partial_rule/get_by_id/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      delete: {
        method: 'delete',
        path: '/entity/partial_rule/delete/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      enable: {
        method: 'patch',
        path: '/entity/partial_rule/enable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      disable: {
        method: 'patch',
        path: '/entity/partial_rule/disable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      count: {
        method: 'post',
        path: '/entity/partial_rule/count',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      sum: {
        method: 'post',
        path: '/entity/partial_rule/sum',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      min: {
        method: 'post',
        path: '/entity/partial_rule/min',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      max: {
        method: 'post',
        path: '/entity/partial_rule/max',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      truncate: {
        method: 'delete',
        path: '/entity/partial_rule/truncate',
        parameters: [{ name: 'instance', in: 'query', required: false }],
      },
    },
    action_group: {
      add: {
        method: 'post',
        path: '/entity/action_group/add',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      update: {
        method: 'put',
        path: '/entity/action_group/update',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      list: {
        method: 'post',
        path: '/entity/action_group/list',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'orders', in: 'body', required: false },
          { name: 'limit', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      get_by_id: {
        method: 'get',
        path: '/entity/action_group/get_by_id/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      delete: {
        method: 'delete',
        path: '/entity/action_group/delete/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      enable: {
        method: 'patch',
        path: '/entity/action_group/enable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      disable: {
        method: 'patch',
        path: '/entity/action_group/disable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      count: {
        method: 'post',
        path: '/entity/action_group/count',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      sum: {
        method: 'post',
        path: '/entity/action_group/sum',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      min: {
        method: 'post',
        path: '/entity/action_group/min',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      max: {
        method: 'post',
        path: '/entity/action_group/max',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      truncate: {
        method: 'delete',
        path: '/entity/action_group/truncate',
        parameters: [{ name: 'instance', in: 'query', required: false }],
      },
    },
    action: {
      add: {
        method: 'post',
        path: '/entity/action/add',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      update: {
        method: 'put',
        path: '/entity/action/update',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      list: {
        method: 'post',
        path: '/entity/action/list',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'orders', in: 'body', required: false },
          { name: 'limit', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      get_by_id: {
        method: 'get',
        path: '/entity/action/get_by_id/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      delete: {
        method: 'delete',
        path: '/entity/action/delete/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      enable: {
        method: 'patch',
        path: '/entity/action/enable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      disable: {
        method: 'patch',
        path: '/entity/action/disable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      count: {
        method: 'post',
        path: '/entity/action/count',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      sum: {
        method: 'post',
        path: '/entity/action/sum',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      min: {
        method: 'post',
        path: '/entity/action/min',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      max: {
        method: 'post',
        path: '/entity/action/max',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      truncate: {
        method: 'delete',
        path: '/entity/action/truncate',
        parameters: [{ name: 'instance', in: 'query', required: false }],
      },
    },
    position: {
      add: {
        method: 'post',
        path: '/entity/position/add',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      update: {
        method: 'put',
        path: '/entity/position/update',
        parameters: [
          { name: 'entity', in: 'body', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      list: {
        method: 'post',
        path: '/entity/position/list',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'orders', in: 'body', required: false },
          { name: 'limit', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      get_by_id: {
        method: 'get',
        path: '/entity/position/get_by_id/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      delete: {
        method: 'delete',
        path: '/entity/position/delete/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'query', required: false },
        ],
      },
      enable: {
        method: 'patch',
        path: '/entity/position/enable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      disable: {
        method: 'patch',
        path: '/entity/position/disable/{id}',
        parameters: [
          { name: 'id', in: 'path', required: true },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      count: {
        method: 'post',
        path: '/entity/position/count',
        parameters: [
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      sum: {
        method: 'post',
        path: '/entity/position/sum',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      min: {
        method: 'post',
        path: '/entity/position/min',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      max: {
        method: 'post',
        path: '/entity/position/max',
        parameters: [
          { name: 'field', in: 'body', required: true },
          { name: 'filters', in: 'body', required: false },
          { name: 'combination', in: 'body', required: false },
          { name: 'instance', in: 'body', required: false },
        ],
      },
      truncate: {
        method: 'delete',
        path: '/entity/position/truncate',
        parameters: [{ name: 'instance', in: 'query', required: false }],
      },
    },
  },
} as const

export type Endpoints = typeof endpoints
