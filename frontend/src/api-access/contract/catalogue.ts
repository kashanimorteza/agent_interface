// Derived from the contract's own description — do not edit by hand.
//
// Regenerate with `npm run contract:pull`; `npm run contract:check` says
// whether the contract has moved on since this was taken.
//
// Contract: Trading Assistant 0.1.0

export interface FieldDescription {
  readonly name: string;
  readonly required: boolean;
  readonly type: "text" | "integer" | "number" | "boolean" | "datetime";
  readonly nullable: boolean;
  readonly maxLength: number | null;
  readonly writeOnly: boolean;
  readonly changeable: boolean;
}

export interface ReturnedField {
  readonly name: string;
  readonly required: boolean;
  readonly type: "text" | "integer" | "number" | "boolean" | "datetime";
  readonly nullable: boolean;
  readonly maxLength: number | null;
}

export interface ResourceDescription {
  readonly name: string;
  readonly path: string;
  readonly title: string;
  readonly identifier: string;
  readonly operations: {
    readonly list: boolean;
    readonly create: boolean;
    readonly read: boolean;
    readonly change: boolean;
    readonly remove: boolean;
    readonly status: boolean;
  };
  readonly fields: readonly FieldDescription[];
  readonly returned: readonly ReturnedField[];
}

export const RESOURCES: readonly ResourceDescription[] = [
  {
    "name": "AccountGroup",
    "path": "/account-groups",
    "title": "Account Group",
    "operations": {
      "list": true,
      "create": true,
      "read": true,
      "change": true,
      "remove": true,
      "status": true
    },
    "fields": [
      {
        "name": "name",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      }
    ],
    "returned": [
      {
        "name": "id",
        "required": false,
        "type": "integer",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "name",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null
      }
    ],
    "identifier": "id"
  },
  {
    "name": "Account",
    "path": "/accounts",
    "title": "Account",
    "operations": {
      "list": true,
      "create": true,
      "read": true,
      "change": true,
      "remove": true,
      "status": true
    },
    "fields": [
      {
        "name": "name",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "group_id",
        "required": true,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "broker_id",
        "required": true,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "base_currency_id",
        "required": true,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "username",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "password",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": true,
        "changeable": true
      },
      {
        "name": "leverage",
        "required": true,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "balance",
        "required": false,
        "type": "number",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "account_type",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      }
    ],
    "returned": [
      {
        "name": "id",
        "required": false,
        "type": "integer",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "name",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "group_id",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "broker_id",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "base_currency_id",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "username",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "leverage",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "balance",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "account_type",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null
      }
    ],
    "identifier": "id"
  },
  {
    "name": "ActionGroup",
    "path": "/action-groups",
    "title": "Action Group",
    "operations": {
      "list": true,
      "create": true,
      "read": true,
      "change": true,
      "remove": true,
      "status": true
    },
    "fields": [
      {
        "name": "name",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      }
    ],
    "returned": [
      {
        "name": "id",
        "required": false,
        "type": "integer",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "name",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null
      }
    ],
    "identifier": "id"
  },
  {
    "name": "Action",
    "path": "/actions",
    "title": "Action",
    "operations": {
      "list": true,
      "create": true,
      "read": true,
      "change": true,
      "remove": true,
      "status": true
    },
    "fields": [
      {
        "name": "name",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "action_group_id",
        "required": true,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "asset_id",
        "required": true,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "account_id",
        "required": true,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "partial_group_id",
        "required": true,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "trailing_group_id",
        "required": true,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "risk_by_reward",
        "required": true,
        "type": "number",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "take_profit",
        "required": true,
        "type": "number",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "stop_loss",
        "required": true,
        "type": "number",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      }
    ],
    "returned": [
      {
        "name": "id",
        "required": false,
        "type": "integer",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "name",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "action_group_id",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "asset_id",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "account_id",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "partial_group_id",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "trailing_group_id",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "risk_by_reward",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "take_profit",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "stop_loss",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null
      }
    ],
    "identifier": "id"
  },
  {
    "name": "Asset",
    "path": "/assets",
    "title": "Asset",
    "operations": {
      "list": true,
      "create": true,
      "read": true,
      "change": true,
      "remove": true,
      "status": true
    },
    "fields": [
      {
        "name": "name",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "symbol",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "category",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "point_size",
        "required": false,
        "type": "number",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "digits",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      }
    ],
    "returned": [
      {
        "name": "id",
        "required": false,
        "type": "integer",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "name",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "symbol",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "category",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "point_size",
        "required": false,
        "type": "number",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "digits",
        "required": false,
        "type": "integer",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null
      }
    ],
    "identifier": "id"
  },
  {
    "name": "Broker",
    "path": "/brokers",
    "title": "Broker",
    "operations": {
      "list": true,
      "create": true,
      "read": true,
      "change": true,
      "remove": true,
      "status": true
    },
    "fields": [
      {
        "name": "name",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "user_id",
        "required": true,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "trading_platform_id",
        "required": true,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      }
    ],
    "returned": [
      {
        "name": "id",
        "required": false,
        "type": "integer",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "name",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "user_id",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "trading_platform_id",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null
      }
    ],
    "identifier": "id"
  },
  {
    "name": "Currency",
    "path": "/currencies",
    "title": "Currency",
    "operations": {
      "list": true,
      "create": true,
      "read": true,
      "change": true,
      "remove": true,
      "status": true
    },
    "fields": [
      {
        "name": "name",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "code",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "symbol",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "country",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "decimal_digits",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      }
    ],
    "returned": [
      {
        "name": "id",
        "required": false,
        "type": "integer",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "name",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "code",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "symbol",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "country",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "decimal_digits",
        "required": false,
        "type": "integer",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null
      }
    ],
    "identifier": "id"
  },
  {
    "name": "PartialGroup",
    "path": "/partial-groups",
    "title": "Partial Group",
    "operations": {
      "list": true,
      "create": true,
      "read": true,
      "change": true,
      "remove": true,
      "status": true
    },
    "fields": [
      {
        "name": "name",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      }
    ],
    "returned": [
      {
        "name": "id",
        "required": false,
        "type": "integer",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "name",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null
      }
    ],
    "identifier": "id"
  },
  {
    "name": "PartialRule",
    "path": "/partial-rules",
    "title": "Partial Rule",
    "operations": {
      "list": true,
      "create": true,
      "read": true,
      "change": true,
      "remove": true,
      "status": true
    },
    "fields": [
      {
        "name": "name",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "partial_group_id",
        "required": true,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "profit_percentage",
        "required": true,
        "type": "number",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "close_percentage",
        "required": true,
        "type": "number",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      }
    ],
    "returned": [
      {
        "name": "id",
        "required": false,
        "type": "integer",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "name",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "partial_group_id",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "profit_percentage",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "close_percentage",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null
      }
    ],
    "identifier": "id"
  },
  {
    "name": "Position",
    "path": "/positions",
    "title": "Position",
    "operations": {
      "list": true,
      "create": true,
      "read": true,
      "change": true,
      "remove": true,
      "status": true
    },
    "fields": [
      {
        "name": "name",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "trading_platform_id",
        "required": true,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "broker_id",
        "required": true,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "account_id",
        "required": true,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "trailing_group_id",
        "required": true,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "partial_group_id",
        "required": true,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "action_group_id",
        "required": true,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "action_id",
        "required": true,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "date",
        "required": true,
        "type": "datetime",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "volume",
        "required": true,
        "type": "number",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "profit",
        "required": false,
        "type": "number",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "is_executed",
        "required": false,
        "type": "boolean",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "order_type",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "base_tp",
        "required": true,
        "type": "number",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "base_sl",
        "required": true,
        "type": "number",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "real_tp",
        "required": true,
        "type": "number",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "real_sl",
        "required": true,
        "type": "number",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      }
    ],
    "returned": [
      {
        "name": "id",
        "required": false,
        "type": "integer",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "name",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "trading_platform_id",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "broker_id",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "account_id",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "trailing_group_id",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "partial_group_id",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "action_group_id",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "action_id",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "date",
        "required": false,
        "type": "datetime",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "volume",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "profit",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "is_executed",
        "required": false,
        "type": "boolean",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "order_type",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "base_tp",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "base_sl",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "real_tp",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "real_sl",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null
      }
    ],
    "identifier": "id"
  },
  {
    "name": "TradingPlatform",
    "path": "/trading-platforms",
    "title": "Trading Platform",
    "operations": {
      "list": true,
      "create": true,
      "read": true,
      "change": true,
      "remove": true,
      "status": true
    },
    "fields": [
      {
        "name": "name",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "code",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      }
    ],
    "returned": [
      {
        "name": "id",
        "required": false,
        "type": "integer",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "name",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "code",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null
      }
    ],
    "identifier": "id"
  },
  {
    "name": "TrailingGroup",
    "path": "/trailing-groups",
    "title": "Trailing Group",
    "operations": {
      "list": true,
      "create": true,
      "read": true,
      "change": true,
      "remove": true,
      "status": true
    },
    "fields": [
      {
        "name": "name",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      }
    ],
    "returned": [
      {
        "name": "id",
        "required": false,
        "type": "integer",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "name",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null
      }
    ],
    "identifier": "id"
  },
  {
    "name": "TrailingRule",
    "path": "/trailing-rules",
    "title": "Trailing Rule",
    "operations": {
      "list": true,
      "create": true,
      "read": true,
      "change": true,
      "remove": true,
      "status": true
    },
    "fields": [
      {
        "name": "name",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "trailing_group_id",
        "required": true,
        "type": "integer",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "trigger_percentage",
        "required": true,
        "type": "number",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "take_profit_adjustment",
        "required": false,
        "type": "number",
        "nullable": true,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "stop_loss_adjustment",
        "required": false,
        "type": "number",
        "nullable": true,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      }
    ],
    "returned": [
      {
        "name": "id",
        "required": false,
        "type": "integer",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "name",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "trailing_group_id",
        "required": false,
        "type": "integer",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "trigger_percentage",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "take_profit_adjustment",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "stop_loss_adjustment",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null
      }
    ],
    "identifier": "id"
  },
  {
    "name": "User",
    "path": "/users",
    "title": "User",
    "operations": {
      "list": true,
      "create": true,
      "read": true,
      "change": true,
      "remove": true,
      "status": true
    },
    "fields": [
      {
        "name": "name",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "username",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "password",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": true,
        "changeable": true
      },
      {
        "name": "api_key",
        "required": true,
        "type": "text",
        "nullable": false,
        "maxLength": null,
        "writeOnly": true,
        "changeable": true
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": false,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null,
        "writeOnly": false,
        "changeable": true
      }
    ],
    "returned": [
      {
        "name": "id",
        "required": false,
        "type": "integer",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "name",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "username",
        "required": false,
        "type": "text",
        "nullable": false,
        "maxLength": null
      },
      {
        "name": "status",
        "required": false,
        "type": "boolean",
        "nullable": true,
        "maxLength": null
      },
      {
        "name": "description",
        "required": false,
        "type": "text",
        "nullable": true,
        "maxLength": null
      }
    ],
    "identifier": "id"
  }
] as const;

export function resourceAt(path: string): ResourceDescription | undefined {
  return RESOURCES.find((resource) => resource.path === `/${path}`);
}
