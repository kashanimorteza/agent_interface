// Generated from the contract's own description — do not edit by hand.
export interface paths {
    "/health": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Whether the layer is answering */
        get: operations["health_health_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/users/": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List User records */
        get: operations["list_records_users__get"];
        put?: never;
        /** Create one User */
        post: operations["create_record_users__post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/users/{identifier}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get one User */
        get: operations["get_record_users__identifier__get"];
        put?: never;
        post?: never;
        /** Remove one User */
        delete: operations["remove_record_users__identifier__delete"];
        options?: never;
        head?: never;
        /** Change one User */
        patch: operations["change_record_users__identifier__patch"];
        trace?: never;
    };
    "/users/{identifier}/status": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Enable or disable one User */
        post: operations["change_status_users__identifier__status_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/currencies/": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List Currency records */
        get: operations["list_records_currencies__get"];
        put?: never;
        /** Create one Currency */
        post: operations["create_record_currencies__post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/currencies/{identifier}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get one Currency */
        get: operations["get_record_currencies__identifier__get"];
        put?: never;
        post?: never;
        /** Remove one Currency */
        delete: operations["remove_record_currencies__identifier__delete"];
        options?: never;
        head?: never;
        /** Change one Currency */
        patch: operations["change_record_currencies__identifier__patch"];
        trace?: never;
    };
    "/currencies/{identifier}/status": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Enable or disable one Currency */
        post: operations["change_status_currencies__identifier__status_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/trading-platforms/": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List TradingPlatform records */
        get: operations["list_records_trading_platforms__get"];
        put?: never;
        /** Create one TradingPlatform */
        post: operations["create_record_trading_platforms__post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/trading-platforms/{identifier}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get one TradingPlatform */
        get: operations["get_record_trading_platforms__identifier__get"];
        put?: never;
        post?: never;
        /** Remove one TradingPlatform */
        delete: operations["remove_record_trading_platforms__identifier__delete"];
        options?: never;
        head?: never;
        /** Change one TradingPlatform */
        patch: operations["change_record_trading_platforms__identifier__patch"];
        trace?: never;
    };
    "/trading-platforms/{identifier}/status": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Enable or disable one TradingPlatform */
        post: operations["change_status_trading_platforms__identifier__status_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/brokers/": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List Broker records */
        get: operations["list_records_brokers__get"];
        put?: never;
        /** Create one Broker */
        post: operations["create_record_brokers__post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/brokers/{identifier}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get one Broker */
        get: operations["get_record_brokers__identifier__get"];
        put?: never;
        post?: never;
        /** Remove one Broker */
        delete: operations["remove_record_brokers__identifier__delete"];
        options?: never;
        head?: never;
        /** Change one Broker */
        patch: operations["change_record_brokers__identifier__patch"];
        trace?: never;
    };
    "/brokers/{identifier}/status": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Enable or disable one Broker */
        post: operations["change_status_brokers__identifier__status_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/account-groups/": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List AccountGroup records */
        get: operations["list_records_account_groups__get"];
        put?: never;
        /** Create one AccountGroup */
        post: operations["create_record_account_groups__post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/account-groups/{identifier}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get one AccountGroup */
        get: operations["get_record_account_groups__identifier__get"];
        put?: never;
        post?: never;
        /** Remove one AccountGroup */
        delete: operations["remove_record_account_groups__identifier__delete"];
        options?: never;
        head?: never;
        /** Change one AccountGroup */
        patch: operations["change_record_account_groups__identifier__patch"];
        trace?: never;
    };
    "/account-groups/{identifier}/status": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Enable or disable one AccountGroup */
        post: operations["change_status_account_groups__identifier__status_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/accounts/": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List Account records */
        get: operations["list_records_accounts__get"];
        put?: never;
        /** Create one Account */
        post: operations["create_record_accounts__post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/accounts/{identifier}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get one Account */
        get: operations["get_record_accounts__identifier__get"];
        put?: never;
        post?: never;
        /** Remove one Account */
        delete: operations["remove_record_accounts__identifier__delete"];
        options?: never;
        head?: never;
        /** Change one Account */
        patch: operations["change_record_accounts__identifier__patch"];
        trace?: never;
    };
    "/accounts/{identifier}/status": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Enable or disable one Account */
        post: operations["change_status_accounts__identifier__status_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/assets/": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List Asset records */
        get: operations["list_records_assets__get"];
        put?: never;
        /** Create one Asset */
        post: operations["create_record_assets__post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/assets/{identifier}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get one Asset */
        get: operations["get_record_assets__identifier__get"];
        put?: never;
        post?: never;
        /** Remove one Asset */
        delete: operations["remove_record_assets__identifier__delete"];
        options?: never;
        head?: never;
        /** Change one Asset */
        patch: operations["change_record_assets__identifier__patch"];
        trace?: never;
    };
    "/assets/{identifier}/status": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Enable or disable one Asset */
        post: operations["change_status_assets__identifier__status_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/trailing-groups/": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List TrailingGroup records */
        get: operations["list_records_trailing_groups__get"];
        put?: never;
        /** Create one TrailingGroup */
        post: operations["create_record_trailing_groups__post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/trailing-groups/{identifier}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get one TrailingGroup */
        get: operations["get_record_trailing_groups__identifier__get"];
        put?: never;
        post?: never;
        /** Remove one TrailingGroup */
        delete: operations["remove_record_trailing_groups__identifier__delete"];
        options?: never;
        head?: never;
        /** Change one TrailingGroup */
        patch: operations["change_record_trailing_groups__identifier__patch"];
        trace?: never;
    };
    "/trailing-groups/{identifier}/status": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Enable or disable one TrailingGroup */
        post: operations["change_status_trailing_groups__identifier__status_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/trailing-rules/": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List TrailingRule records */
        get: operations["list_records_trailing_rules__get"];
        put?: never;
        /** Create one TrailingRule */
        post: operations["create_record_trailing_rules__post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/trailing-rules/{identifier}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get one TrailingRule */
        get: operations["get_record_trailing_rules__identifier__get"];
        put?: never;
        post?: never;
        /** Remove one TrailingRule */
        delete: operations["remove_record_trailing_rules__identifier__delete"];
        options?: never;
        head?: never;
        /** Change one TrailingRule */
        patch: operations["change_record_trailing_rules__identifier__patch"];
        trace?: never;
    };
    "/trailing-rules/{identifier}/status": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Enable or disable one TrailingRule */
        post: operations["change_status_trailing_rules__identifier__status_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/partial-groups/": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List PartialGroup records */
        get: operations["list_records_partial_groups__get"];
        put?: never;
        /** Create one PartialGroup */
        post: operations["create_record_partial_groups__post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/partial-groups/{identifier}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get one PartialGroup */
        get: operations["get_record_partial_groups__identifier__get"];
        put?: never;
        post?: never;
        /** Remove one PartialGroup */
        delete: operations["remove_record_partial_groups__identifier__delete"];
        options?: never;
        head?: never;
        /** Change one PartialGroup */
        patch: operations["change_record_partial_groups__identifier__patch"];
        trace?: never;
    };
    "/partial-groups/{identifier}/status": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Enable or disable one PartialGroup */
        post: operations["change_status_partial_groups__identifier__status_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/partial-rules/": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List PartialRule records */
        get: operations["list_records_partial_rules__get"];
        put?: never;
        /** Create one PartialRule */
        post: operations["create_record_partial_rules__post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/partial-rules/{identifier}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get one PartialRule */
        get: operations["get_record_partial_rules__identifier__get"];
        put?: never;
        post?: never;
        /** Remove one PartialRule */
        delete: operations["remove_record_partial_rules__identifier__delete"];
        options?: never;
        head?: never;
        /** Change one PartialRule */
        patch: operations["change_record_partial_rules__identifier__patch"];
        trace?: never;
    };
    "/partial-rules/{identifier}/status": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Enable or disable one PartialRule */
        post: operations["change_status_partial_rules__identifier__status_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/action-groups/": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List ActionGroup records */
        get: operations["list_records_action_groups__get"];
        put?: never;
        /** Create one ActionGroup */
        post: operations["create_record_action_groups__post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/action-groups/{identifier}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get one ActionGroup */
        get: operations["get_record_action_groups__identifier__get"];
        put?: never;
        post?: never;
        /** Remove one ActionGroup */
        delete: operations["remove_record_action_groups__identifier__delete"];
        options?: never;
        head?: never;
        /** Change one ActionGroup */
        patch: operations["change_record_action_groups__identifier__patch"];
        trace?: never;
    };
    "/action-groups/{identifier}/status": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Enable or disable one ActionGroup */
        post: operations["change_status_action_groups__identifier__status_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/actions/": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List Action records */
        get: operations["list_records_actions__get"];
        put?: never;
        /** Create one Action */
        post: operations["create_record_actions__post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/actions/{identifier}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get one Action */
        get: operations["get_record_actions__identifier__get"];
        put?: never;
        post?: never;
        /** Remove one Action */
        delete: operations["remove_record_actions__identifier__delete"];
        options?: never;
        head?: never;
        /** Change one Action */
        patch: operations["change_record_actions__identifier__patch"];
        trace?: never;
    };
    "/actions/{identifier}/status": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Enable or disable one Action */
        post: operations["change_status_actions__identifier__status_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/positions/": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List Position records */
        get: operations["list_records_positions__get"];
        put?: never;
        /** Create one Position */
        post: operations["create_record_positions__post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/positions/{identifier}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get one Position */
        get: operations["get_record_positions__identifier__get"];
        put?: never;
        post?: never;
        /** Remove one Position */
        delete: operations["remove_record_positions__identifier__delete"];
        options?: never;
        head?: never;
        /** Change one Position */
        patch: operations["change_record_positions__identifier__patch"];
        trace?: never;
    };
    "/positions/{identifier}/status": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Enable or disable one Position */
        post: operations["change_status_positions__identifier__status_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
}
export type webhooks = Record<string, never>;
export interface components {
    schemas: {
        /** Account */
        Account: {
            /** Id */
            id?: number | null;
            /** Name */
            name?: string;
            /** Group Id */
            group_id?: number;
            /** Broker Id */
            broker_id?: number;
            /** Base Currency Id */
            base_currency_id?: number;
            /** Username */
            username?: string;
            /** Leverage */
            leverage?: number;
            /** Balance */
            balance?: string | null;
            /** Account Type */
            account_type?: string;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** Account changes */
        AccountChange: {
            /** Name */
            name?: string | null;
            /** Group Id */
            group_id?: number | null;
            /** Broker Id */
            broker_id?: number | null;
            /** Base Currency Id */
            base_currency_id?: number | null;
            /** Username */
            username?: string | null;
            /** Password */
            password?: string | null;
            /** Leverage */
            leverage?: number | null;
            /** Balance */
            balance?: number | string | null;
            /** Account Type */
            account_type?: string | null;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** AccountGroup */
        AccountGroup: {
            /** Id */
            id?: number | null;
            /** Name */
            name?: string;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** AccountGroup changes */
        AccountGroupChange: {
            /** Name */
            name?: string | null;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** AccountGroup to create */
        AccountGroupInput: {
            /** Name */
            name: string;
            /**
             * Status
             * @default true
             */
            status: boolean;
            /** Description */
            description?: string | null;
        };
        /** Account to create */
        AccountInput: {
            /** Name */
            name: string;
            /** Group Id */
            group_id: number;
            /** Broker Id */
            broker_id: number;
            /** Base Currency Id */
            base_currency_id: number;
            /** Username */
            username: string;
            /** Password */
            password: string;
            /** Leverage */
            leverage: number;
            /**
             * Balance
             * @default 0
             */
            balance: number | string;
            /** Account Type */
            account_type: string;
            /**
             * Status
             * @default true
             */
            status: boolean;
            /** Description */
            description?: string | null;
        };
        /** Action */
        Action: {
            /** Id */
            id?: number | null;
            /** Name */
            name?: string;
            /** Action Group Id */
            action_group_id?: number;
            /** Asset Id */
            asset_id?: number;
            /** Account Id */
            account_id?: number;
            /** Partial Group Id */
            partial_group_id?: number;
            /** Trailing Group Id */
            trailing_group_id?: number;
            /** Risk By Reward */
            risk_by_reward?: string;
            /** Take Profit */
            take_profit?: string;
            /** Stop Loss */
            stop_loss?: string;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** Action changes */
        ActionChange: {
            /** Name */
            name?: string | null;
            /** Action Group Id */
            action_group_id?: number | null;
            /** Asset Id */
            asset_id?: number | null;
            /** Account Id */
            account_id?: number | null;
            /** Partial Group Id */
            partial_group_id?: number | null;
            /** Trailing Group Id */
            trailing_group_id?: number | null;
            /** Risk By Reward */
            risk_by_reward?: number | string | null;
            /** Take Profit */
            take_profit?: number | string | null;
            /** Stop Loss */
            stop_loss?: number | string | null;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** ActionGroup */
        ActionGroup: {
            /** Id */
            id?: number | null;
            /** Name */
            name?: string;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** ActionGroup changes */
        ActionGroupChange: {
            /** Name */
            name?: string | null;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** ActionGroup to create */
        ActionGroupInput: {
            /** Name */
            name: string;
            /**
             * Status
             * @default true
             */
            status: boolean;
            /** Description */
            description?: string | null;
        };
        /** Action to create */
        ActionInput: {
            /** Name */
            name: string;
            /** Action Group Id */
            action_group_id: number;
            /** Asset Id */
            asset_id: number;
            /** Account Id */
            account_id: number;
            /** Partial Group Id */
            partial_group_id: number;
            /** Trailing Group Id */
            trailing_group_id: number;
            /** Risk By Reward */
            risk_by_reward: number | string;
            /** Take Profit */
            take_profit: number | string;
            /** Stop Loss */
            stop_loss: number | string;
            /**
             * Status
             * @default true
             */
            status: boolean;
            /** Description */
            description?: string | null;
        };
        /** Asset */
        Asset: {
            /** Id */
            id?: number | null;
            /** Name */
            name?: string;
            /** Symbol */
            symbol?: string;
            /** Category */
            category?: string;
            /** Point Size */
            point_size?: number | null;
            /** Digits */
            digits?: number | null;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** Asset changes */
        AssetChange: {
            /** Name */
            name?: string | null;
            /** Symbol */
            symbol?: string | null;
            /** Category */
            category?: string | null;
            /** Point Size */
            point_size?: number | null;
            /** Digits */
            digits?: number | null;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** Asset to create */
        AssetInput: {
            /** Name */
            name: string;
            /** Symbol */
            symbol: string;
            /** Category */
            category: string;
            /**
             * Point Size
             * @default 0
             */
            point_size: number;
            /**
             * Digits
             * @default 0
             */
            digits: number;
            /**
             * Status
             * @default true
             */
            status: boolean;
            /** Description */
            description?: string | null;
        };
        /** Broker */
        Broker: {
            /** Id */
            id?: number | null;
            /** Name */
            name?: string;
            /** User Id */
            user_id?: number;
            /** Trading Platform Id */
            trading_platform_id?: number;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** Broker changes */
        BrokerChange: {
            /** Name */
            name?: string | null;
            /** User Id */
            user_id?: number | null;
            /** Trading Platform Id */
            trading_platform_id?: number | null;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** Broker to create */
        BrokerInput: {
            /** Name */
            name: string;
            /** User Id */
            user_id: number;
            /** Trading Platform Id */
            trading_platform_id: number;
            /**
             * Status
             * @default true
             */
            status: boolean;
            /** Description */
            description?: string | null;
        };
        /** Currency */
        Currency: {
            /** Id */
            id?: number | null;
            /** Name */
            name?: string;
            /** Code */
            code?: string;
            /** Symbol */
            symbol?: string | null;
            /** Country */
            country?: string | null;
            /** Decimal Digits */
            decimal_digits?: number | null;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** Currency changes */
        CurrencyChange: {
            /** Name */
            name?: string | null;
            /** Code */
            code?: string | null;
            /** Symbol */
            symbol?: string | null;
            /** Country */
            country?: string | null;
            /** Decimal Digits */
            decimal_digits?: number | null;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** Currency to create */
        CurrencyInput: {
            /** Name */
            name: string;
            /** Code */
            code: string;
            /** Symbol */
            symbol?: string | null;
            /** Country */
            country?: string | null;
            /**
             * Decimal Digits
             * @default 2
             */
            decimal_digits: number;
            /**
             * Status
             * @default true
             */
            status: boolean;
            /** Description */
            description?: string | null;
        };
        /** HTTPValidationError */
        HTTPValidationError: {
            /** Detail */
            detail?: components["schemas"]["ValidationError"][];
        };
        /** PartialGroup */
        PartialGroup: {
            /** Id */
            id?: number | null;
            /** Name */
            name?: string;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** PartialGroup changes */
        PartialGroupChange: {
            /** Name */
            name?: string | null;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** PartialGroup to create */
        PartialGroupInput: {
            /** Name */
            name: string;
            /**
             * Status
             * @default true
             */
            status: boolean;
            /** Description */
            description?: string | null;
        };
        /** PartialRule */
        PartialRule: {
            /** Id */
            id?: number | null;
            /** Name */
            name?: string;
            /** Partial Group Id */
            partial_group_id?: number;
            /** Profit Percentage */
            profit_percentage?: string;
            /** Close Percentage */
            close_percentage?: string;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** PartialRule changes */
        PartialRuleChange: {
            /** Name */
            name?: string | null;
            /** Partial Group Id */
            partial_group_id?: number | null;
            /** Profit Percentage */
            profit_percentage?: number | string | null;
            /** Close Percentage */
            close_percentage?: number | string | null;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** PartialRule to create */
        PartialRuleInput: {
            /** Name */
            name: string;
            /** Partial Group Id */
            partial_group_id: number;
            /** Profit Percentage */
            profit_percentage: number | string;
            /** Close Percentage */
            close_percentage: number | string;
            /**
             * Status
             * @default true
             */
            status: boolean;
            /** Description */
            description?: string | null;
        };
        /** Position */
        Position: {
            /** Id */
            id?: number | null;
            /** Name */
            name?: string;
            /** Trading Platform Id */
            trading_platform_id?: number;
            /** Broker Id */
            broker_id?: number;
            /** Account Id */
            account_id?: number;
            /** Trailing Group Id */
            trailing_group_id?: number;
            /** Partial Group Id */
            partial_group_id?: number;
            /** Action Group Id */
            action_group_id?: number;
            /** Action Id */
            action_id?: number;
            /**
             * Date
             * Format: date-time
             */
            date?: string;
            /** Volume */
            volume?: string;
            /** Profit */
            profit?: string | null;
            /** Is Executed */
            is_executed?: boolean | null;
            /** Order Type */
            order_type?: string;
            /** Base Tp */
            base_tp?: string;
            /** Base Sl */
            base_sl?: string;
            /** Real Tp */
            real_tp?: string;
            /** Real Sl */
            real_sl?: string;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** Position changes */
        PositionChange: {
            /** Name */
            name?: string | null;
            /** Trading Platform Id */
            trading_platform_id?: number | null;
            /** Broker Id */
            broker_id?: number | null;
            /** Account Id */
            account_id?: number | null;
            /** Trailing Group Id */
            trailing_group_id?: number | null;
            /** Partial Group Id */
            partial_group_id?: number | null;
            /** Action Group Id */
            action_group_id?: number | null;
            /** Action Id */
            action_id?: number | null;
            /** Date */
            date?: string | null;
            /** Volume */
            volume?: number | string | null;
            /** Profit */
            profit?: number | string | null;
            /** Is Executed */
            is_executed?: boolean | null;
            /** Order Type */
            order_type?: string | null;
            /** Base Tp */
            base_tp?: number | string | null;
            /** Base Sl */
            base_sl?: number | string | null;
            /** Real Tp */
            real_tp?: number | string | null;
            /** Real Sl */
            real_sl?: number | string | null;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** Position to create */
        PositionInput: {
            /** Name */
            name: string;
            /** Trading Platform Id */
            trading_platform_id: number;
            /** Broker Id */
            broker_id: number;
            /** Account Id */
            account_id: number;
            /** Trailing Group Id */
            trailing_group_id: number;
            /** Partial Group Id */
            partial_group_id: number;
            /** Action Group Id */
            action_group_id: number;
            /** Action Id */
            action_id: number;
            /**
             * Date
             * Format: date-time
             */
            date: string;
            /** Volume */
            volume: number | string;
            /**
             * Profit
             * @default 0
             */
            profit: number | string;
            /**
             * Is Executed
             * @default false
             */
            is_executed: boolean;
            /** Order Type */
            order_type: string;
            /** Base Tp */
            base_tp: number | string;
            /** Base Sl */
            base_sl: number | string;
            /** Real Tp */
            real_tp: number | string;
            /** Real Sl */
            real_sl: number | string;
            /**
             * Status
             * @default true
             */
            status: boolean;
            /** Description */
            description?: string | null;
        };
        /**
         * StatusChange
         * @description Which of the two actions to apply to a record's active state.
         */
        StatusChange: {
            /** Action */
            action: string;
        };
        /** TradingPlatform */
        TradingPlatform: {
            /** Id */
            id?: number | null;
            /** Name */
            name?: string;
            /** Code */
            code?: string;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** TradingPlatform changes */
        TradingPlatformChange: {
            /** Name */
            name?: string | null;
            /** Code */
            code?: string | null;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** TradingPlatform to create */
        TradingPlatformInput: {
            /** Name */
            name: string;
            /** Code */
            code: string;
            /**
             * Status
             * @default true
             */
            status: boolean;
            /** Description */
            description?: string | null;
        };
        /** TrailingGroup */
        TrailingGroup: {
            /** Id */
            id?: number | null;
            /** Name */
            name?: string;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** TrailingGroup changes */
        TrailingGroupChange: {
            /** Name */
            name?: string | null;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** TrailingGroup to create */
        TrailingGroupInput: {
            /** Name */
            name: string;
            /**
             * Status
             * @default true
             */
            status: boolean;
            /** Description */
            description?: string | null;
        };
        /** TrailingRule */
        TrailingRule: {
            /** Id */
            id?: number | null;
            /** Name */
            name?: string;
            /** Trailing Group Id */
            trailing_group_id?: number;
            /** Trigger Percentage */
            trigger_percentage?: string;
            /** Take Profit Adjustment */
            take_profit_adjustment?: string | null;
            /** Stop Loss Adjustment */
            stop_loss_adjustment?: string | null;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** TrailingRule changes */
        TrailingRuleChange: {
            /** Name */
            name?: string | null;
            /** Trailing Group Id */
            trailing_group_id?: number | null;
            /** Trigger Percentage */
            trigger_percentage?: number | string | null;
            /** Take Profit Adjustment */
            take_profit_adjustment?: number | string | null;
            /** Stop Loss Adjustment */
            stop_loss_adjustment?: number | string | null;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** TrailingRule to create */
        TrailingRuleInput: {
            /** Name */
            name: string;
            /** Trailing Group Id */
            trailing_group_id: number;
            /** Trigger Percentage */
            trigger_percentage: number | string;
            /** Take Profit Adjustment */
            take_profit_adjustment?: number | string | null;
            /** Stop Loss Adjustment */
            stop_loss_adjustment?: number | string | null;
            /**
             * Status
             * @default true
             */
            status: boolean;
            /** Description */
            description?: string | null;
        };
        /** User */
        User: {
            /** Id */
            id?: number | null;
            /** Name */
            name?: string;
            /** Username */
            username?: string;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** User changes */
        UserChange: {
            /** Name */
            name?: string | null;
            /** Username */
            username?: string | null;
            /** Password */
            password?: string | null;
            /** Api Key */
            api_key?: string | null;
            /** Status */
            status?: boolean | null;
            /** Description */
            description?: string | null;
        };
        /** User to create */
        UserInput: {
            /** Name */
            name: string;
            /** Username */
            username: string;
            /** Password */
            password: string;
            /** Api Key */
            api_key: string;
            /**
             * Status
             * @default true
             */
            status: boolean;
            /** Description */
            description?: string | null;
        };
        /** ValidationError */
        ValidationError: {
            /** Location */
            loc: (string | number)[];
            /** Message */
            msg: string;
            /** Error Type */
            type: string;
            /** Input */
            input?: unknown;
            /** Context */
            ctx?: Record<string, never>;
        };
    };
    responses: never;
    parameters: never;
    requestBodies: never;
    headers: never;
    pathItems: never;
}
export type $defs = Record<string, never>;
export interface operations {
    health_health_get: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": {
                        [key: string]: string;
                    };
                };
            };
        };
    };
    list_records_users__get: {
        parameters: {
            query?: {
                /** @description How many to return. */
                limit?: number | null;
                /** @description How many to skip. */
                offset?: number | null;
                /** @description A field to order by. */
                order_by?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["User"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_record_users__post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["UserInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["User"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_record_users__identifier__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one User. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["User"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    remove_record_users__identifier__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one User. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_record_users__identifier__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one User. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["UserChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["User"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_status_users__identifier__status_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one User. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["StatusChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["User"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_records_currencies__get: {
        parameters: {
            query?: {
                /** @description How many to return. */
                limit?: number | null;
                /** @description How many to skip. */
                offset?: number | null;
                /** @description A field to order by. */
                order_by?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Currency"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_record_currencies__post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["CurrencyInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Currency"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_record_currencies__identifier__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Currency. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Currency"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    remove_record_currencies__identifier__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Currency. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_record_currencies__identifier__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Currency. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["CurrencyChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Currency"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_status_currencies__identifier__status_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Currency. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["StatusChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Currency"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_records_trading_platforms__get: {
        parameters: {
            query?: {
                /** @description How many to return. */
                limit?: number | null;
                /** @description How many to skip. */
                offset?: number | null;
                /** @description A field to order by. */
                order_by?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["TradingPlatform"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_record_trading_platforms__post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["TradingPlatformInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["TradingPlatform"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_record_trading_platforms__identifier__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one TradingPlatform. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["TradingPlatform"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    remove_record_trading_platforms__identifier__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one TradingPlatform. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_record_trading_platforms__identifier__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one TradingPlatform. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["TradingPlatformChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["TradingPlatform"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_status_trading_platforms__identifier__status_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one TradingPlatform. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["StatusChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["TradingPlatform"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_records_brokers__get: {
        parameters: {
            query?: {
                /** @description How many to return. */
                limit?: number | null;
                /** @description How many to skip. */
                offset?: number | null;
                /** @description A field to order by. */
                order_by?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Broker"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_record_brokers__post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["BrokerInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Broker"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_record_brokers__identifier__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Broker. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Broker"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    remove_record_brokers__identifier__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Broker. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_record_brokers__identifier__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Broker. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["BrokerChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Broker"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_status_brokers__identifier__status_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Broker. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["StatusChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Broker"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_records_account_groups__get: {
        parameters: {
            query?: {
                /** @description How many to return. */
                limit?: number | null;
                /** @description How many to skip. */
                offset?: number | null;
                /** @description A field to order by. */
                order_by?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AccountGroup"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_record_account_groups__post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["AccountGroupInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AccountGroup"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_record_account_groups__identifier__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one AccountGroup. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AccountGroup"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    remove_record_account_groups__identifier__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one AccountGroup. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_record_account_groups__identifier__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one AccountGroup. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["AccountGroupChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AccountGroup"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_status_account_groups__identifier__status_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one AccountGroup. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["StatusChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AccountGroup"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_records_accounts__get: {
        parameters: {
            query?: {
                /** @description How many to return. */
                limit?: number | null;
                /** @description How many to skip. */
                offset?: number | null;
                /** @description A field to order by. */
                order_by?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Account"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_record_accounts__post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["AccountInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Account"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_record_accounts__identifier__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Account. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Account"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    remove_record_accounts__identifier__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Account. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_record_accounts__identifier__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Account. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["AccountChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Account"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_status_accounts__identifier__status_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Account. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["StatusChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Account"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_records_assets__get: {
        parameters: {
            query?: {
                /** @description How many to return. */
                limit?: number | null;
                /** @description How many to skip. */
                offset?: number | null;
                /** @description A field to order by. */
                order_by?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Asset"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_record_assets__post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["AssetInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Asset"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_record_assets__identifier__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Asset. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Asset"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    remove_record_assets__identifier__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Asset. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_record_assets__identifier__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Asset. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["AssetChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Asset"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_status_assets__identifier__status_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Asset. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["StatusChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Asset"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_records_trailing_groups__get: {
        parameters: {
            query?: {
                /** @description How many to return. */
                limit?: number | null;
                /** @description How many to skip. */
                offset?: number | null;
                /** @description A field to order by. */
                order_by?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["TrailingGroup"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_record_trailing_groups__post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["TrailingGroupInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["TrailingGroup"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_record_trailing_groups__identifier__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one TrailingGroup. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["TrailingGroup"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    remove_record_trailing_groups__identifier__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one TrailingGroup. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_record_trailing_groups__identifier__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one TrailingGroup. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["TrailingGroupChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["TrailingGroup"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_status_trailing_groups__identifier__status_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one TrailingGroup. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["StatusChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["TrailingGroup"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_records_trailing_rules__get: {
        parameters: {
            query?: {
                /** @description How many to return. */
                limit?: number | null;
                /** @description How many to skip. */
                offset?: number | null;
                /** @description A field to order by. */
                order_by?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["TrailingRule"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_record_trailing_rules__post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["TrailingRuleInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["TrailingRule"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_record_trailing_rules__identifier__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one TrailingRule. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["TrailingRule"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    remove_record_trailing_rules__identifier__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one TrailingRule. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_record_trailing_rules__identifier__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one TrailingRule. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["TrailingRuleChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["TrailingRule"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_status_trailing_rules__identifier__status_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one TrailingRule. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["StatusChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["TrailingRule"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_records_partial_groups__get: {
        parameters: {
            query?: {
                /** @description How many to return. */
                limit?: number | null;
                /** @description How many to skip. */
                offset?: number | null;
                /** @description A field to order by. */
                order_by?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["PartialGroup"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_record_partial_groups__post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["PartialGroupInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["PartialGroup"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_record_partial_groups__identifier__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one PartialGroup. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["PartialGroup"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    remove_record_partial_groups__identifier__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one PartialGroup. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_record_partial_groups__identifier__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one PartialGroup. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["PartialGroupChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["PartialGroup"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_status_partial_groups__identifier__status_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one PartialGroup. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["StatusChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["PartialGroup"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_records_partial_rules__get: {
        parameters: {
            query?: {
                /** @description How many to return. */
                limit?: number | null;
                /** @description How many to skip. */
                offset?: number | null;
                /** @description A field to order by. */
                order_by?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["PartialRule"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_record_partial_rules__post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["PartialRuleInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["PartialRule"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_record_partial_rules__identifier__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one PartialRule. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["PartialRule"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    remove_record_partial_rules__identifier__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one PartialRule. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_record_partial_rules__identifier__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one PartialRule. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["PartialRuleChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["PartialRule"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_status_partial_rules__identifier__status_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one PartialRule. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["StatusChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["PartialRule"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_records_action_groups__get: {
        parameters: {
            query?: {
                /** @description How many to return. */
                limit?: number | null;
                /** @description How many to skip. */
                offset?: number | null;
                /** @description A field to order by. */
                order_by?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ActionGroup"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_record_action_groups__post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ActionGroupInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ActionGroup"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_record_action_groups__identifier__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one ActionGroup. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ActionGroup"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    remove_record_action_groups__identifier__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one ActionGroup. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_record_action_groups__identifier__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one ActionGroup. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ActionGroupChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ActionGroup"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_status_action_groups__identifier__status_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one ActionGroup. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["StatusChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ActionGroup"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_records_actions__get: {
        parameters: {
            query?: {
                /** @description How many to return. */
                limit?: number | null;
                /** @description How many to skip. */
                offset?: number | null;
                /** @description A field to order by. */
                order_by?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Action"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_record_actions__post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ActionInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Action"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_record_actions__identifier__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Action. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Action"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    remove_record_actions__identifier__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Action. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_record_actions__identifier__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Action. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ActionChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Action"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_status_actions__identifier__status_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Action. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["StatusChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Action"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_records_positions__get: {
        parameters: {
            query?: {
                /** @description How many to return. */
                limit?: number | null;
                /** @description How many to skip. */
                offset?: number | null;
                /** @description A field to order by. */
                order_by?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Position"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_record_positions__post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["PositionInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Position"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_record_positions__identifier__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Position. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Position"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    remove_record_positions__identifier__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Position. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_record_positions__identifier__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Position. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["PositionChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Position"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_status_positions__identifier__status_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                /** @description Identifies one Position. */
                identifier: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["StatusChange"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Position"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
}
