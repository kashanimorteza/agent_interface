(()=>{"use strict";(globalThis["TURBOPACK"] || (globalThis["TURBOPACK"] = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/presentation/api/calls.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "createApiClient",
    ()=>createApiClient
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$errors$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/api/errors.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$generated$2f$endpoints$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/api/generated/endpoints.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$translation$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/api/translation.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$transport$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/api/transport.ts [app-client] (ecmascript)");
;
;
;
;
function createApiClient(address) {
    const table = __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$generated$2f$endpoints$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["endpoints"];
    const client = {};
    for (const [group, adapters] of Object.entries(table)){
        const byAdapter = {};
        client[group] = byAdapter;
        for (const [adapter, operations] of Object.entries(adapters)){
            const byName = {};
            byAdapter[adapter] = byName;
            for (const [name, endpoint] of Object.entries(operations)){
                byName[name] = (args = {})=>(0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$errors$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["outcome"])(()=>(0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$transport$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["send"])(address, endpoint, (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$translation$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["argumentsToWire"])(args)));
            }
        }
    }
    return client;
}
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/api/errors.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "interpret",
    ()=>interpret,
    "outcome",
    ()=>outcome
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$transport$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/api/transport.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$values$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/api/values.ts [app-client] (ecmascript)");
;
;
function text(value) {
    return typeof value === 'string' ? value : null;
}
function problemOf(response) {
    const { body, contentType } = response;
    if (contentType === null || !contentType.includes('application/problem+json')) return null;
    if (body === null || typeof body !== 'object') return null;
    const members = body;
    if (typeof members.type !== 'string') return null;
    return {
        type: members.type,
        status: typeof members.status === 'number' ? members.status : response.status,
        title: text(members.title),
        detail: text(members.detail)
    };
}
function interpret(response) {
    if (response.ok) return {
        ok: true,
        value: response.body
    };
    const problem = problemOf(response);
    if (problem !== null) return {
        ok: false,
        failure: {
            kind: 'problem',
            problem
        }
    };
    return {
        ok: false,
        failure: {
            kind: 'unrecognized',
            status: response.status,
            body: response.body
        }
    };
}
async function outcome(request) {
    try {
        return interpret(await request());
    } catch (error) {
        if (error instanceof __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$transport$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["TransportFailure"]) {
            return {
                ok: false,
                failure: {
                    kind: 'unreachable',
                    message: error.message
                }
            };
        }
        if (error instanceof __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$values$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["TranslationError"]) {
            return {
                ok: false,
                failure: {
                    kind: 'untranslatable',
                    message: error.message
                }
            };
        }
        throw error;
    }
}
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/api/generated/endpoints.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

// Generated from the API description. Regenerate; do not edit.
__turbopack_context__.s([
    "endpoints",
    ()=>endpoints
]);
const endpoints = {
    entity: {
        user: {
            add: {
                method: 'post',
                path: '/entity/user/add',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            update: {
                method: 'put',
                path: '/entity/user/update',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            list: {
                method: 'post',
                path: '/entity/user/list',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'orders',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'limit',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            get_by_id: {
                method: 'get',
                path: '/entity/user/get_by_id/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            delete: {
                method: 'delete',
                path: '/entity/user/delete/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            enable: {
                method: 'patch',
                path: '/entity/user/enable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            disable: {
                method: 'patch',
                path: '/entity/user/disable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            count: {
                method: 'post',
                path: '/entity/user/count',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            sum: {
                method: 'post',
                path: '/entity/user/sum',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            min: {
                method: 'post',
                path: '/entity/user/min',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            max: {
                method: 'post',
                path: '/entity/user/max',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            truncate: {
                method: 'delete',
                path: '/entity/user/truncate',
                parameters: [
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            }
        },
        trading_platform: {
            add: {
                method: 'post',
                path: '/entity/trading_platform/add',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            update: {
                method: 'put',
                path: '/entity/trading_platform/update',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            list: {
                method: 'post',
                path: '/entity/trading_platform/list',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'orders',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'limit',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            get_by_id: {
                method: 'get',
                path: '/entity/trading_platform/get_by_id/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            delete: {
                method: 'delete',
                path: '/entity/trading_platform/delete/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            enable: {
                method: 'patch',
                path: '/entity/trading_platform/enable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            disable: {
                method: 'patch',
                path: '/entity/trading_platform/disable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            count: {
                method: 'post',
                path: '/entity/trading_platform/count',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            sum: {
                method: 'post',
                path: '/entity/trading_platform/sum',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            min: {
                method: 'post',
                path: '/entity/trading_platform/min',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            max: {
                method: 'post',
                path: '/entity/trading_platform/max',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            truncate: {
                method: 'delete',
                path: '/entity/trading_platform/truncate',
                parameters: [
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            }
        },
        instance: {
            add: {
                method: 'post',
                path: '/entity/instance/add',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            update: {
                method: 'put',
                path: '/entity/instance/update',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            list: {
                method: 'post',
                path: '/entity/instance/list',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'orders',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'limit',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            get_by_id: {
                method: 'get',
                path: '/entity/instance/get_by_id/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            delete: {
                method: 'delete',
                path: '/entity/instance/delete/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            enable: {
                method: 'patch',
                path: '/entity/instance/enable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            disable: {
                method: 'patch',
                path: '/entity/instance/disable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            count: {
                method: 'post',
                path: '/entity/instance/count',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            sum: {
                method: 'post',
                path: '/entity/instance/sum',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            min: {
                method: 'post',
                path: '/entity/instance/min',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            max: {
                method: 'post',
                path: '/entity/instance/max',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            truncate: {
                method: 'delete',
                path: '/entity/instance/truncate',
                parameters: [
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            }
        },
        currency: {
            add: {
                method: 'post',
                path: '/entity/currency/add',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            update: {
                method: 'put',
                path: '/entity/currency/update',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            list: {
                method: 'post',
                path: '/entity/currency/list',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'orders',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'limit',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            get_by_id: {
                method: 'get',
                path: '/entity/currency/get_by_id/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            delete: {
                method: 'delete',
                path: '/entity/currency/delete/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            enable: {
                method: 'patch',
                path: '/entity/currency/enable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            disable: {
                method: 'patch',
                path: '/entity/currency/disable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            count: {
                method: 'post',
                path: '/entity/currency/count',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            sum: {
                method: 'post',
                path: '/entity/currency/sum',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            min: {
                method: 'post',
                path: '/entity/currency/min',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            max: {
                method: 'post',
                path: '/entity/currency/max',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            truncate: {
                method: 'delete',
                path: '/entity/currency/truncate',
                parameters: [
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            }
        },
        broker: {
            add: {
                method: 'post',
                path: '/entity/broker/add',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            update: {
                method: 'put',
                path: '/entity/broker/update',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            list: {
                method: 'post',
                path: '/entity/broker/list',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'orders',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'limit',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            get_by_id: {
                method: 'get',
                path: '/entity/broker/get_by_id/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            delete: {
                method: 'delete',
                path: '/entity/broker/delete/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            enable: {
                method: 'patch',
                path: '/entity/broker/enable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            disable: {
                method: 'patch',
                path: '/entity/broker/disable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            count: {
                method: 'post',
                path: '/entity/broker/count',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            sum: {
                method: 'post',
                path: '/entity/broker/sum',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            min: {
                method: 'post',
                path: '/entity/broker/min',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            max: {
                method: 'post',
                path: '/entity/broker/max',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            truncate: {
                method: 'delete',
                path: '/entity/broker/truncate',
                parameters: [
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            }
        },
        asset: {
            add: {
                method: 'post',
                path: '/entity/asset/add',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            update: {
                method: 'put',
                path: '/entity/asset/update',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            list: {
                method: 'post',
                path: '/entity/asset/list',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'orders',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'limit',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            get_by_id: {
                method: 'get',
                path: '/entity/asset/get_by_id/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            delete: {
                method: 'delete',
                path: '/entity/asset/delete/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            enable: {
                method: 'patch',
                path: '/entity/asset/enable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            disable: {
                method: 'patch',
                path: '/entity/asset/disable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            count: {
                method: 'post',
                path: '/entity/asset/count',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            sum: {
                method: 'post',
                path: '/entity/asset/sum',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            min: {
                method: 'post',
                path: '/entity/asset/min',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            max: {
                method: 'post',
                path: '/entity/asset/max',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            truncate: {
                method: 'delete',
                path: '/entity/asset/truncate',
                parameters: [
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            }
        },
        account_group: {
            add: {
                method: 'post',
                path: '/entity/account_group/add',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            update: {
                method: 'put',
                path: '/entity/account_group/update',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            list: {
                method: 'post',
                path: '/entity/account_group/list',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'orders',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'limit',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            get_by_id: {
                method: 'get',
                path: '/entity/account_group/get_by_id/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            delete: {
                method: 'delete',
                path: '/entity/account_group/delete/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            enable: {
                method: 'patch',
                path: '/entity/account_group/enable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            disable: {
                method: 'patch',
                path: '/entity/account_group/disable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            count: {
                method: 'post',
                path: '/entity/account_group/count',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            sum: {
                method: 'post',
                path: '/entity/account_group/sum',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            min: {
                method: 'post',
                path: '/entity/account_group/min',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            max: {
                method: 'post',
                path: '/entity/account_group/max',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            truncate: {
                method: 'delete',
                path: '/entity/account_group/truncate',
                parameters: [
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            }
        },
        account: {
            add: {
                method: 'post',
                path: '/entity/account/add',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            update: {
                method: 'put',
                path: '/entity/account/update',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            list: {
                method: 'post',
                path: '/entity/account/list',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'orders',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'limit',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            get_by_id: {
                method: 'get',
                path: '/entity/account/get_by_id/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            delete: {
                method: 'delete',
                path: '/entity/account/delete/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            enable: {
                method: 'patch',
                path: '/entity/account/enable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            disable: {
                method: 'patch',
                path: '/entity/account/disable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            count: {
                method: 'post',
                path: '/entity/account/count',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            sum: {
                method: 'post',
                path: '/entity/account/sum',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            min: {
                method: 'post',
                path: '/entity/account/min',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            max: {
                method: 'post',
                path: '/entity/account/max',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            truncate: {
                method: 'delete',
                path: '/entity/account/truncate',
                parameters: [
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            }
        },
        trailing_group: {
            add: {
                method: 'post',
                path: '/entity/trailing_group/add',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            update: {
                method: 'put',
                path: '/entity/trailing_group/update',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            list: {
                method: 'post',
                path: '/entity/trailing_group/list',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'orders',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'limit',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            get_by_id: {
                method: 'get',
                path: '/entity/trailing_group/get_by_id/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            delete: {
                method: 'delete',
                path: '/entity/trailing_group/delete/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            enable: {
                method: 'patch',
                path: '/entity/trailing_group/enable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            disable: {
                method: 'patch',
                path: '/entity/trailing_group/disable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            count: {
                method: 'post',
                path: '/entity/trailing_group/count',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            sum: {
                method: 'post',
                path: '/entity/trailing_group/sum',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            min: {
                method: 'post',
                path: '/entity/trailing_group/min',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            max: {
                method: 'post',
                path: '/entity/trailing_group/max',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            truncate: {
                method: 'delete',
                path: '/entity/trailing_group/truncate',
                parameters: [
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            }
        },
        trailing_rule: {
            add: {
                method: 'post',
                path: '/entity/trailing_rule/add',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            update: {
                method: 'put',
                path: '/entity/trailing_rule/update',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            list: {
                method: 'post',
                path: '/entity/trailing_rule/list',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'orders',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'limit',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            get_by_id: {
                method: 'get',
                path: '/entity/trailing_rule/get_by_id/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            delete: {
                method: 'delete',
                path: '/entity/trailing_rule/delete/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            enable: {
                method: 'patch',
                path: '/entity/trailing_rule/enable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            disable: {
                method: 'patch',
                path: '/entity/trailing_rule/disable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            count: {
                method: 'post',
                path: '/entity/trailing_rule/count',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            sum: {
                method: 'post',
                path: '/entity/trailing_rule/sum',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            min: {
                method: 'post',
                path: '/entity/trailing_rule/min',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            max: {
                method: 'post',
                path: '/entity/trailing_rule/max',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            truncate: {
                method: 'delete',
                path: '/entity/trailing_rule/truncate',
                parameters: [
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            }
        },
        partial_group: {
            add: {
                method: 'post',
                path: '/entity/partial_group/add',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            update: {
                method: 'put',
                path: '/entity/partial_group/update',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            list: {
                method: 'post',
                path: '/entity/partial_group/list',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'orders',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'limit',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            get_by_id: {
                method: 'get',
                path: '/entity/partial_group/get_by_id/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            delete: {
                method: 'delete',
                path: '/entity/partial_group/delete/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            enable: {
                method: 'patch',
                path: '/entity/partial_group/enable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            disable: {
                method: 'patch',
                path: '/entity/partial_group/disable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            count: {
                method: 'post',
                path: '/entity/partial_group/count',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            sum: {
                method: 'post',
                path: '/entity/partial_group/sum',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            min: {
                method: 'post',
                path: '/entity/partial_group/min',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            max: {
                method: 'post',
                path: '/entity/partial_group/max',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            truncate: {
                method: 'delete',
                path: '/entity/partial_group/truncate',
                parameters: [
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            }
        },
        partial_rule: {
            add: {
                method: 'post',
                path: '/entity/partial_rule/add',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            update: {
                method: 'put',
                path: '/entity/partial_rule/update',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            list: {
                method: 'post',
                path: '/entity/partial_rule/list',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'orders',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'limit',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            get_by_id: {
                method: 'get',
                path: '/entity/partial_rule/get_by_id/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            delete: {
                method: 'delete',
                path: '/entity/partial_rule/delete/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            enable: {
                method: 'patch',
                path: '/entity/partial_rule/enable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            disable: {
                method: 'patch',
                path: '/entity/partial_rule/disable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            count: {
                method: 'post',
                path: '/entity/partial_rule/count',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            sum: {
                method: 'post',
                path: '/entity/partial_rule/sum',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            min: {
                method: 'post',
                path: '/entity/partial_rule/min',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            max: {
                method: 'post',
                path: '/entity/partial_rule/max',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            truncate: {
                method: 'delete',
                path: '/entity/partial_rule/truncate',
                parameters: [
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            }
        },
        action_group: {
            add: {
                method: 'post',
                path: '/entity/action_group/add',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            update: {
                method: 'put',
                path: '/entity/action_group/update',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            list: {
                method: 'post',
                path: '/entity/action_group/list',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'orders',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'limit',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            get_by_id: {
                method: 'get',
                path: '/entity/action_group/get_by_id/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            delete: {
                method: 'delete',
                path: '/entity/action_group/delete/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            enable: {
                method: 'patch',
                path: '/entity/action_group/enable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            disable: {
                method: 'patch',
                path: '/entity/action_group/disable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            count: {
                method: 'post',
                path: '/entity/action_group/count',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            sum: {
                method: 'post',
                path: '/entity/action_group/sum',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            min: {
                method: 'post',
                path: '/entity/action_group/min',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            max: {
                method: 'post',
                path: '/entity/action_group/max',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            truncate: {
                method: 'delete',
                path: '/entity/action_group/truncate',
                parameters: [
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            }
        },
        action: {
            add: {
                method: 'post',
                path: '/entity/action/add',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            update: {
                method: 'put',
                path: '/entity/action/update',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            list: {
                method: 'post',
                path: '/entity/action/list',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'orders',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'limit',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            get_by_id: {
                method: 'get',
                path: '/entity/action/get_by_id/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            delete: {
                method: 'delete',
                path: '/entity/action/delete/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            enable: {
                method: 'patch',
                path: '/entity/action/enable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            disable: {
                method: 'patch',
                path: '/entity/action/disable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            count: {
                method: 'post',
                path: '/entity/action/count',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            sum: {
                method: 'post',
                path: '/entity/action/sum',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            min: {
                method: 'post',
                path: '/entity/action/min',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            max: {
                method: 'post',
                path: '/entity/action/max',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            truncate: {
                method: 'delete',
                path: '/entity/action/truncate',
                parameters: [
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            }
        },
        position: {
            add: {
                method: 'post',
                path: '/entity/position/add',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            update: {
                method: 'put',
                path: '/entity/position/update',
                parameters: [
                    {
                        name: 'entity',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            list: {
                method: 'post',
                path: '/entity/position/list',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'orders',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'limit',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            get_by_id: {
                method: 'get',
                path: '/entity/position/get_by_id/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            delete: {
                method: 'delete',
                path: '/entity/position/delete/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            },
            enable: {
                method: 'patch',
                path: '/entity/position/enable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            disable: {
                method: 'patch',
                path: '/entity/position/disable/{id}',
                parameters: [
                    {
                        name: 'id',
                        in: 'path',
                        required: true
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            count: {
                method: 'post',
                path: '/entity/position/count',
                parameters: [
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            sum: {
                method: 'post',
                path: '/entity/position/sum',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            min: {
                method: 'post',
                path: '/entity/position/min',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            max: {
                method: 'post',
                path: '/entity/position/max',
                parameters: [
                    {
                        name: 'field',
                        in: 'body',
                        required: true
                    },
                    {
                        name: 'filters',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'combination',
                        in: 'body',
                        required: false
                    },
                    {
                        name: 'instance',
                        in: 'body',
                        required: false
                    }
                ]
            },
            truncate: {
                method: 'delete',
                path: '/entity/position/truncate',
                parameters: [
                    {
                        name: 'instance',
                        in: 'query',
                        required: false
                    }
                ]
            }
        }
    }
};
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/api/provider.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "ApiAccessProvider",
    ()=>ApiAccessProvider,
    "useApiAccess",
    ()=>useApiAccess
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$calls$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/api/calls.ts [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature(), _s1 = __turbopack_context__.k.signature();
'use client';
;
;
const Context = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["createContext"])(null);
_c = Context;
function ApiAccessProvider({ baseUrl, problem, children }) {
    _s();
    const access = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useMemo"])({
        "ApiAccessProvider.useMemo[access]": ()=>baseUrl === undefined ? {
                status: 'misconfigured',
                problem: problem ?? 'The API address is not set.'
            } : {
                status: 'ready',
                client: (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$calls$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["createApiClient"])({
                    baseUrl
                })
            }
    }["ApiAccessProvider.useMemo[access]"], [
        baseUrl,
        problem
    ]);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(Context, {
        value: access,
        children: children
    }, void 0, false, {
        fileName: "[project]/presentation/api/provider.tsx",
        lineNumber: 36,
        columnNumber: 10
    }, this);
}
_s(ApiAccessProvider, "iuPqfdTVeu97+kqvBhU7oIMkrag=");
_c1 = ApiAccessProvider;
function useApiAccess() {
    _s1();
    const access = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useContext"])(Context);
    if (access === null) {
        throw new Error('API Access is used outside its provider.');
    }
    return access;
}
_s1(useApiAccess, "PBjrDbTE5r+zReDoXfSik64a/lE=");
var _c, _c1;
__turbopack_context__.k.register(_c, "Context");
__turbopack_context__.k.register(_c1, "ApiAccessProvider");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/api/translation.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "argumentsToWire",
    ()=>argumentsToWire,
    "filterToWire",
    ()=>filterToWire,
    "orderToWire",
    ()=>orderToWire,
    "parameterToWire",
    ()=>parameterToWire
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$values$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/api/values.ts [app-client] (ecmascript)");
;
function jsonValue(value) {
    if (value === null) return null;
    if (typeof value === 'string' || typeof value === 'boolean') return value;
    if (typeof value === 'number' && Number.isFinite(value)) return value;
    throw new __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$values$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["TranslationError"]('A value cannot travel as JSON.');
}
function name(value, what) {
    if (typeof value !== 'string' || value === '') {
        throw new __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$values$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["TranslationError"](`A ${what} must be a non-empty name.`);
    }
    return value;
}
function filterToWire(condition) {
    const wire = {
        field: name(condition.field, 'Filter Field'),
        operator: name(condition.operator, 'Filter operator')
    };
    const { value } = condition;
    if (value !== undefined) {
        wire.value = Array.isArray(value) ? value.map(jsonValue) : jsonValue(value);
    }
    return wire;
}
function orderToWire(term) {
    const wire = {
        field: name(term.field, 'Order Field')
    };
    if (term.direction !== undefined) wire.direction = name(term.direction, 'Order direction');
    return wire;
}
function integer(value, what) {
    if (typeof value !== 'number' || !Number.isSafeInteger(value)) {
        throw new __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$values$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["TranslationError"](`A ${what} must be an integer.`);
    }
    return value;
}
function recordToJson(record) {
    if (record === null || typeof record !== 'object' || Array.isArray(record)) {
        throw new __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$values$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["TranslationError"]('A record must be an object.');
    }
    const wire = {};
    for (const [field, value] of Object.entries(record))wire[field] = jsonValue(value);
    return wire;
}
function parameterToWire(parameter, value) {
    switch(parameter){
        case 'entity':
            return recordToJson(value);
        case 'filters':
            if (!Array.isArray(value)) throw new __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$values$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["TranslationError"]('Filters must be a list.');
            return value.map((condition)=>filterToWire(condition));
        case 'orders':
            if (!Array.isArray(value)) throw new __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$values$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["TranslationError"]('Orders must be a list.');
            return value.map((term)=>orderToWire(term));
        case 'combination':
        case 'field':
        case 'instance':
            return name(value, parameter);
        case 'limit':
        case 'id':
            return integer(value, parameter);
        default:
            throw new __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$values$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["TranslationError"](`The Parameter ${parameter} has no published transport form.`);
    }
}
function argumentsToWire(args) {
    const wire = {};
    for (const [parameter, value] of Object.entries(args)){
        if (value === undefined) continue;
        wire[parameter] = value === null ? null : parameterToWire(parameter, value);
    }
    return wire;
}
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/api/transport.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "TransportFailure",
    ()=>TransportFailure,
    "send",
    ()=>send
]);
class TransportFailure extends Error {
    name = 'TransportFailure';
}
function present(value) {
    return value !== undefined;
}
function pathOf(endpoint, args) {
    return endpoint.path.replace(/\{([^}]+)\}/g, (_, name)=>{
        const value = args[name];
        if (!present(value) || value === null) {
            throw new TypeError(`The path parameter ${name} is required.`);
        }
        return encodeURIComponent(String(value));
    });
}
function queryOf(endpoint, args) {
    const query = new URLSearchParams();
    for (const parameter of endpoint.parameters){
        const value = args[parameter.name];
        if (parameter.in === 'query' && present(value) && value !== null) {
            query.append(parameter.name, String(value));
        }
    }
    const text = query.toString();
    return text === '' ? '' : `?${text}`;
}
function bodyOf(endpoint, args) {
    const members = endpoint.parameters.filter((parameter)=>parameter.in === 'body');
    if (members.length === 0) return undefined;
    const body = {};
    for (const parameter of members){
        if (present(args[parameter.name])) body[parameter.name] = args[parameter.name];
    }
    return JSON.stringify(body);
}
async function parse(response) {
    const text = await response.text();
    if (text === '') return null;
    try {
        return JSON.parse(text);
    } catch  {
        return text;
    }
}
async function send(address, endpoint, args) {
    const url = `${address.baseUrl}${pathOf(endpoint, args)}${queryOf(endpoint, args)}`;
    const body = bodyOf(endpoint, args);
    let response;
    try {
        response = await fetch(url, {
            method: endpoint.method.toUpperCase(),
            headers: body === undefined ? undefined : {
                'Content-Type': 'application/json'
            },
            body
        });
    } catch  {
        throw new TransportFailure('The API could not be reached.');
    }
    return {
        status: response.status,
        ok: response.ok,
        contentType: response.headers.get('content-type'),
        body: await parse(response)
    };
}
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/api/values.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/** The value kinds the API publishes a transport form for. */ __turbopack_context__.s([
    "TranslationError",
    ()=>TranslationError,
    "recordFromWire",
    ()=>recordFromWire,
    "recordToWire",
    ()=>recordToWire,
    "valueFromWire",
    ()=>valueFromWire,
    "valueToWire",
    ()=>valueToWire
]);
class TranslationError extends Error {
    name = 'TranslationError';
}
const DECIMAL = /^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$/;
const DATETIME = /^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:?\d{2})$/;
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
function refuse(kind) {
    throw new TranslationError(`A value is not in the form of a ${kind}.`);
}
/**
 * Checks that a value has the form of its kind and returns it unchanged. The
 * same form holds on both sides of the API, so one check serves both
 * directions. A message names the kind, never the value.
 */ function conform(kind, value) {
    if (value === null) return null;
    switch(kind){
        case 'string':
            return typeof value === 'string' ? value : refuse(kind);
        case 'integer':
            return typeof value === 'number' && Number.isSafeInteger(value) ? value : refuse(kind);
        case 'float':
            return typeof value === 'number' && Number.isFinite(value) ? value : refuse(kind);
        case 'boolean':
            return typeof value === 'boolean' ? value : refuse(kind);
        case 'decimal':
            return typeof value === 'string' && DECIMAL.test(value) ? value : refuse(kind);
        case 'datetime':
            return typeof value === 'string' && DATETIME.test(value) ? value : refuse(kind);
        case 'uuid':
            return typeof value === 'string' && UUID.test(value) ? value : refuse(kind);
    }
}
function valueToWire(kind, value) {
    return conform(kind, value);
}
function valueFromWire(kind, wire) {
    return conform(kind, wire);
}
function translateRecord(kinds, record, convert) {
    const result = {};
    for (const [name, value] of Object.entries(record)){
        const kind = kinds[name];
        if (kind === undefined) {
            throw new TranslationError(`A Field is not described: ${name}.`);
        }
        result[name] = convert(kind, value);
    }
    return result;
}
function recordToWire(kinds, record) {
    return translateRecord(kinds, record, conform);
}
function recordFromWire(kinds, wire) {
    if (wire === null || typeof wire !== 'object' || Array.isArray(wire)) {
        throw new TranslationError('A record is not an object.');
    }
    return translateRecord(kinds, wire, conform);
}
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
]);})()

//# sourceMappingURL=presentation_api_1zla_xet7z4qx._.js.map