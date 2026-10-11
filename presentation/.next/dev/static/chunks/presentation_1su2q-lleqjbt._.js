(globalThis["TURBOPACK"] || (globalThis["TURBOPACK"] = [])).push([typeof document === "object" ? document.currentScript : undefined,
(()=>{"use strict";return[
"[project]/presentation/api/address.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "API_ADDRESS_VARIABLE",
    ()=>API_ADDRESS_VARIABLE,
    "ApiAddressError",
    ()=>ApiAddressError,
    "readApiAddress",
    ()=>readApiAddress
]);
const API_ADDRESS_VARIABLE = 'PRESENTATION_API_URL';
class ApiAddressError extends Error {
    name = 'ApiAddressError';
}
function readApiAddress(environment) {
    const raw = environment[API_ADDRESS_VARIABLE];
    if (raw === undefined || raw.trim() === '') {
        throw new ApiAddressError(`The API address is not set. Set ${API_ADDRESS_VARIABLE} to the complete Base URL of the running API, including its URL Key.`);
    }
    let url;
    try {
        url = new URL(raw.trim());
    } catch  {
        throw new ApiAddressError(`The API address in ${API_ADDRESS_VARIABLE} is not a valid URL. Set it to the complete Base URL of the running API, such as http://host:port/key.`);
    }
    if (url.protocol !== 'http:' && url.protocol !== 'https:') {
        throw new ApiAddressError(`The API address in ${API_ADDRESS_VARIABLE} must use http or https.`);
    }
    if (url.search !== '' || url.hash !== '' || url.username !== '' || url.password !== '') {
        throw new ApiAddressError(`The API address in ${API_ADDRESS_VARIABLE} must be a plain Base URL without credentials, query or fragment.`);
    }
    return {
        baseUrl: url.origin + url.pathname.replace(/\/+$/, '')
    };
}
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/api/generated/vocabulary.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

// Generated from the API documentation. Regenerate; do not edit.
__turbopack_context__.s([
    "queryVocabulary",
    ()=>queryVocabulary
]);
const queryVocabulary = {
    operators: [
        {
            name: 'EQUALS',
            value: 'one'
        },
        {
            name: 'NOT_EQUALS',
            value: 'one'
        },
        {
            name: 'GREATER_THAN',
            value: 'one'
        },
        {
            name: 'GREATER_OR_EQUAL',
            value: 'one'
        },
        {
            name: 'LESS_THAN',
            value: 'one'
        },
        {
            name: 'LESS_OR_EQUAL',
            value: 'one'
        },
        {
            name: 'IN',
            value: 'many'
        },
        {
            name: 'CONTAINS',
            value: 'one'
        },
        {
            name: 'STARTS_WITH',
            value: 'one'
        },
        {
            name: 'ENDS_WITH',
            value: 'one'
        },
        {
            name: 'IS_NULL',
            value: 'none'
        },
        {
            name: 'IS_NOT_NULL',
            value: 'none'
        }
    ],
    combinations: [
        'AND',
        'OR'
    ],
    directions: [
        'ASCENDING',
        'DESCENDING'
    ]
};
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/api/index.ts [app-client] (ecmascript) <locals>", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([]);
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$address$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/api/address.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$calls$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/api/calls.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$provider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/api/provider.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$setting$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/api/setting.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$vocabulary$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/api/vocabulary.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$values$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/api/values.ts [app-client] (ecmascript)");
;
;
;
;
;
;
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/api/setting.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "loadApiSetting",
    ()=>loadApiSetting
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$address$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/api/address.ts [app-client] (ecmascript)");
;
function loadApiSetting() {
    try {
        return {
            address: (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$address$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["readApiAddress"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].env)
        };
    } catch (error) {
        if (error instanceof __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$address$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["ApiAddressError"]) return {
            problem: error.message
        };
        throw error;
    }
}
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/api/vocabulary.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "queryVocabulary",
    ()=>queryVocabulary
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$generated$2f$vocabulary$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/api/generated/vocabulary.ts [app-client] (ecmascript)");
;
const queryVocabulary = __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$generated$2f$vocabulary$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["queryVocabulary"];
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/interaction/aggregate.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "changeOperation",
    ()=>changeOperation,
    "firstRequest",
    ()=>firstRequest,
    "operationsOf",
    ()=>operationsOf,
    "useAggregate",
    ()=>useAggregate
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$index$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$locals$3e$__ = __turbopack_context__.i("[project]/presentation/api/index.ts [app-client] (ecmascript) <locals>");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$vocabulary$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/api/vocabulary.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$filter$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/interaction/filter.ts [app-client] (ecmascript)");
var _s = __turbopack_context__.k.signature();
;
;
;
function firstRequest(operations) {
    const operation = operations[0];
    if (operation === undefined) return null;
    return {
        operation: operation.name,
        field: operation.fields?.[0]?.name ?? null,
        filters: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$filter$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["noFilters"]
    };
}
function changeOperation(request, operation) {
    const field = operation.fields === undefined ? null : operation.fields.find((f)=>f.name === request.field)?.name ?? operation.fields[0]?.name ?? null;
    return {
        operation: operation.name,
        field,
        filters: operation.takesFilters ? request.filters : __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$filter$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["noFilters"]
    };
}
const NUMERIC = new Set([
    'integer',
    'float',
    'decimal'
]);
function operationsOf(calls, fields) {
    const visible = fields.filter((field)=>field.sensitive !== true);
    const operations = [];
    if (calls.count !== undefined) {
        operations.push({
            name: 'count',
            takesFilters: true
        });
    }
    if (calls.sum !== undefined) {
        operations.push({
            name: 'sum',
            fields: visible.filter((field)=>NUMERIC.has(field.kind)),
            takesFilters: true
        });
    }
    for (const name of [
        'min',
        'max'
    ]){
        if (calls[name] !== undefined) {
            operations.push({
                name,
                fields: visible.filter((field)=>field.kind !== 'boolean'),
                takesFilters: true
            });
        }
    }
    return operations;
}
function singleValue(value) {
    return value === null || typeof value === 'number' || typeof value === 'string' || typeof value === 'boolean' ? value : undefined;
}
/** Starts the request of one operation; nothing starts for an operation the Adapter lacks or one that needs a Field and has none. */ function ask(calls, operation, field, query) {
    if (operation === 'count') return calls.count?.(query);
    if (field === null) return undefined;
    const call = operation === 'sum' ? calls.sum : operation === 'min' ? calls.min : operation === 'max' ? calls.max : undefined;
    return call?.({
        ...query,
        field
    });
}
function useAggregate(calls, fields) {
    _s();
    const operations = operationsOf(calls, fields);
    const [request, setRequest] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])({
        "useAggregate.useState": ()=>firstRequest(operations)
    }["useAggregate.useState"]);
    const [problems, setProblems] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([]);
    const [state, setState] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])({
        status: 'idle'
    });
    const sending = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRef"])(false);
    const run = async ()=>{
        const operation = operations.find((o)=>o.name === request?.operation);
        if (request === null || operation === undefined || sending.current) return;
        const outcome = (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$filter$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["filterOf"])(request.filters, fields, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$vocabulary$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["queryVocabulary"].operators);
        if (!outcome.ok) {
            setProblems(outcome.problems);
            return;
        }
        const query = {
            ...outcome.conditions.length > 0 && {
                filters: outcome.conditions
            },
            ...outcome.combination !== undefined && {
                combination: outcome.combination
            }
        };
        const pending = ask(calls, operation.name, request.field, query);
        if (pending === undefined) return;
        setProblems([]);
        sending.current = true;
        setState({
            status: 'loading'
        });
        const result = await pending.finally(()=>{
            sending.current = false;
        });
        if (!result.ok) {
            setState({
                status: 'failed',
                failure: result.failure
            });
            return;
        }
        const value = singleValue(result.value);
        setState(value === undefined ? {
            status: 'failed',
            failure: {
                kind: 'untranslatable',
                message: 'The result is not a single value.'
            }
        } : {
            status: 'ready',
            value
        });
    };
    return {
        operations,
        request,
        setRequest,
        problems,
        state,
        run: ()=>void run()
    };
}
_s(useAggregate, "ZQLF4guPCDbbPY89FTNpXEm3yzE=");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/interaction/async.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "useLoaded",
    ()=>useLoaded
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var _s = __turbopack_context__.k.signature();
;
function useLoaded(key, load) {
    _s();
    const latest = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRef"])(load);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "useLoaded.useEffect": ()=>{
            latest.current = load;
        }
    }["useLoaded.useEffect"]);
    const [settled, setSettled] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "useLoaded.useEffect": ()=>{
            if (key === null) return;
            let current = true;
            void latest.current().then({
                "useLoaded.useEffect": (value)=>{
                    if (current) setSettled({
                        key,
                        value
                    });
                }
            }["useLoaded.useEffect"]);
            return ({
                "useLoaded.useEffect": ()=>{
                    current = false;
                }
            })["useLoaded.useEffect"];
        }
    }["useLoaded.useEffect"], [
        key
    ]);
    if (key === null) return {
        status: 'idle'
    };
    if (settled !== null && settled.key === key) {
        return {
            status: 'ready',
            value: settled.value
        };
    }
    return {
        status: 'loading'
    };
}
_s(useLoaded, "Q3J5pH53H8E48VTEQeQOUkbuOUU=");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/interaction/fields.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "fieldText",
    ()=>fieldText,
    "isEnterable",
    ()=>isEnterable,
    "parseFieldText",
    ()=>parseFieldText
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$index$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$locals$3e$__ = __turbopack_context__.i("[project]/presentation/api/index.ts [app-client] (ecmascript) <locals>");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$values$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/api/values.ts [app-client] (ecmascript)");
;
function isEnterable(field) {
    return field.immutable !== true && field.generated !== true;
}
const INTEGER = /^[+-]?\d+$/;
function parsed(kind, candidate, text) {
    try {
        return {
            state: 'value',
            value: (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$values$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["valueFromWire"])(kind, candidate)
        };
    } catch  {
        return {
            state: 'invalid',
            text
        };
    }
}
function parseFieldText(kind, text) {
    const trimmed = text.trim();
    switch(kind){
        case 'string':
            return {
                state: 'value',
                value: text
            };
        case 'integer':
            return INTEGER.test(trimmed) ? parsed(kind, Number(trimmed), text) : trimmed === '' ? {
                state: 'empty'
            } : {
                state: 'invalid',
                text
            };
        case 'float':
            return trimmed === '' ? {
                state: 'empty'
            } : parsed(kind, Number(trimmed), text);
        case 'boolean':
            return trimmed === 'true' || trimmed === 'false' ? {
                state: 'value',
                value: trimmed === 'true'
            } : trimmed === '' ? {
                state: 'empty'
            } : {
                state: 'invalid',
                text
            };
        case 'decimal':
        case 'datetime':
        case 'uuid':
            return trimmed === '' ? {
                state: 'empty'
            } : parsed(kind, trimmed, text);
    }
}
function fieldText(value) {
    return value === undefined || value === null ? '' : String(value);
}
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/interaction/filter.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "applicableOperators",
    ()=>applicableOperators,
    "changeField",
    ()=>changeField,
    "changeOperator",
    ()=>changeOperator,
    "filterOf",
    ()=>filterOf,
    "newCondition",
    ()=>newCondition,
    "noFilters",
    ()=>noFilters
]);
const noFilters = {
    conditions: [],
    combination: null
};
function applicableOperators(operators, field) {
    return operators.filter((operator)=>operator.kinds === undefined || operator.kinds.includes(field.kind));
}
function valuesFor(operator) {
    return operator === undefined || operator.value === 'none' ? [] : [
        {
            state: 'empty'
        }
    ];
}
function newCondition(fields, operators) {
    const field = fields[0];
    if (field === undefined) return null;
    const operator = applicableOperators(operators, field)[0];
    if (operator === undefined) return null;
    return {
        field: field.name,
        operator: operator.name,
        values: valuesFor(operator)
    };
}
function changeField(condition, field, operators) {
    const applicable = applicableOperators(operators, field);
    const operator = applicable.find((candidate)=>candidate.name === condition.operator) ?? applicable[0];
    return {
        field: field.name,
        operator: operator?.name ?? '',
        values: valuesFor(operator)
    };
}
function changeOperator(condition, operator, previous) {
    return {
        ...condition,
        operator: operator.name,
        values: previous?.value === operator.value ? condition.values : valuesFor(operator)
    };
}
function valueOf(entry) {
    return entry !== undefined && entry.state === 'value' && entry.value !== null ? entry : null;
}
function filterOf(draft, fields, operators) {
    const problems = [];
    const conditions = [];
    for (const condition of draft.conditions){
        const field = fields.find((candidate)=>candidate.name === condition.field);
        const operator = operators.find((candidate)=>candidate.name === condition.operator);
        if (field === undefined || operator === undefined) {
            problems.push('Choose a Field and an operator.');
            continue;
        }
        if (operator.value === 'none') {
            problems.push(null);
            conditions.push({
                field: field.name,
                operator: operator.name
            });
            continue;
        }
        const entries = condition.values.map(valueOf);
        if (entries.length === 0 || operator.value === 'one' && entries.length !== 1 || entries.some((entry)=>entry === null)) {
            problems.push('Enter a value.');
            continue;
        }
        problems.push(null);
        const values = entries.map((entry)=>entry.value);
        conditions.push({
            field: field.name,
            operator: operator.name,
            value: operator.value === 'many' ? values : values[0]
        });
    }
    if (problems.some((problem)=>problem !== null)) {
        return {
            ok: false,
            problems
        };
    }
    return {
        ok: true,
        conditions,
        combination: conditions.length > 1 ? draft.combination ?? undefined : undefined
    };
}
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/interaction/order.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "limitOf",
    ()=>limitOf,
    "orderTermsOf",
    ()=>orderTermsOf,
    "unordered",
    ()=>unordered
]);
const unordered = {
    order: null,
    limit: {
        state: 'empty'
    }
};
function orderTermsOf(choice) {
    return choice === null ? [] : [
        {
            field: choice.field,
            direction: choice.direction
        }
    ];
}
function limitOf(entry) {
    if (entry.state === 'value' && typeof entry.value === 'number') {
        return entry.value;
    }
    return entry.state === 'empty' || entry.state === 'absent' ? undefined : null;
}
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/preview/demo.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Demo",
    ()=>Demo
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
// TEMPORARY preview page, requested by the user to see the Theme and the built Components.
// It is not part of the Plan: delete this directory and restore app/page.tsx to remove it.
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$index$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$locals$3e$__ = __turbopack_context__.i("[project]/presentation/api/index.ts [app-client] (ecmascript) <locals>");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$provider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/api/provider.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$async$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/interaction/async.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$filter$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/interaction/filter.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$order$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/interaction/order.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$aggregate$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/interaction/aggregate.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$aggregate$2d$panel$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/aggregate-panel.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/button.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$confirmation$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/confirmation.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/feedback.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$input$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/field-input.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$filter$2d$editor$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/filter-editor.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$order$2d$controls$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/order-controls.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$page$2d$frame$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/page-frame.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$record$2d$form$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/record-form.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$record$2d$table$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/record-table.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$preview$2f$demo$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/presentation/preview/demo.module.css [app-client] (css module)");
;
var _s = __turbopack_context__.k.signature(), _s1 = __turbopack_context__.k.signature(), _s2 = __turbopack_context__.k.signature();
'use client';
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
// The preview lists these by hand; the real Sections take them from the API contract.
const OPERATORS = [
    {
        name: 'EQUALS',
        value: 'one'
    },
    {
        name: 'NOT_EQUALS',
        value: 'one'
    },
    {
        name: 'GREATER_THAN',
        value: 'one',
        kinds: [
            'integer',
            'float',
            'decimal',
            'datetime'
        ]
    },
    {
        name: 'IN',
        value: 'many'
    },
    {
        name: 'CONTAINS',
        value: 'one',
        kinds: [
            'string'
        ]
    },
    {
        name: 'IS_NULL',
        value: 'none'
    }
];
const SAMPLE_FIELDS = [
    {
        name: 'code',
        kind: 'string',
        required: true
    },
    {
        name: 'decimal_digits',
        kind: 'integer',
        required: true,
        default: 2
    },
    {
        name: 'balance',
        kind: 'decimal',
        required: true
    },
    {
        name: 'opened_at',
        kind: 'datetime',
        required: false
    },
    {
        name: 'is_active',
        kind: 'boolean',
        required: true,
        default: true
    },
    {
        name: 'description',
        kind: 'string',
        required: false
    }
];
const AGGREGATES = [
    {
        name: 'count',
        takesFilters: true
    },
    {
        name: 'sum',
        fields: SAMPLE_FIELDS.filter((f)=>f.kind === 'decimal' || f.kind === 'integer'),
        takesFilters: true
    }
];
const SWATCHES = [
    'surface',
    'surface-raised',
    'surface-sunken',
    'border',
    'accent',
    'accent-subtle',
    'danger',
    'success',
    'warning',
    'text',
    'text-muted'
];
function kindOf(value) {
    if (typeof value === 'boolean') return 'boolean';
    if (typeof value === 'number') return Number.isInteger(value) ? 'integer' : 'float';
    return 'string';
}
function Block({ id, title, children }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
        id: id,
        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$preview$2f$demo$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].block,
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$preview$2f$demo$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].title,
                children: title
            }, void 0, false, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 91,
                columnNumber: 7
            }, this),
            children
        ]
    }, void 0, true, {
        fileName: "[project]/presentation/preview/demo.tsx",
        lineNumber: 90,
        columnNumber: 5
    }, this);
}
_c = Block;
function Connection() {
    _s();
    const access = (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$provider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useApiAccess"])();
    const client = access.status === 'ready' ? access.client : null;
    const counts = (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$async$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useLoaded"])(client === null ? null : 'counts', {
        "Connection.useLoaded[counts]": async ()=>{
            const entries = Object.entries(client.entity);
            return Promise.all(entries.map({
                "Connection.useLoaded[counts]": async ([adapter, calls])=>[
                        adapter,
                        await calls.count()
                    ]
            }["Connection.useLoaded[counts]"]));
        }
    }["Connection.useLoaded[counts]"]);
    if (access.status === 'misconfigured') {
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["ErrorNotice"], {
            failure: {
                kind: 'untranslatable',
                message: access.problem
            }
        }, void 0, false, {
            fileName: "[project]/presentation/preview/demo.tsx",
            lineNumber: 115,
            columnNumber: 7
        }, this);
    }
    if (counts.status !== 'ready') return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Loading"], {
        label: "Asking the API how many records each Entity has"
    }, void 0, false, {
        fileName: "[project]/presentation/preview/demo.tsx",
        lineNumber: 121,
        columnNumber: 12
    }, this);
    const rows = counts.value.map(([adapter, result])=>({
            entity: adapter,
            records: result.ok ? result.value : null
        }));
    const failed = counts.value.find(([, r])=>!r.ok);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$preview$2f$demo$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].stack,
        children: [
            failed === undefined ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Success"], {
                children: [
                    "The API answered for all ",
                    rows.length,
                    " Entities."
                ]
            }, void 0, true, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 130,
                columnNumber: 9
            }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["ErrorNotice"], {
                failure: {
                    kind: 'unreachable',
                    message: 'The API did not answer for every Entity. Check the API address setting and that the API is running.'
                }
            }, void 0, false, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 132,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$record$2d$table$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["RecordTable"], {
                caption: "Records per Entity",
                fields: [
                    {
                        name: 'entity',
                        kind: 'string',
                        required: true
                    },
                    {
                        name: 'records',
                        kind: 'integer',
                        required: true
                    }
                ],
                records: rows
            }, void 0, false, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 140,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/presentation/preview/demo.tsx",
        lineNumber: 128,
        columnNumber: 5
    }, this);
}
_s(Connection, "t6TmOK99QWn0n7d3mmj04zADrrI=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$provider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useApiAccess"],
        __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$async$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useLoaded"]
    ];
});
_c1 = Connection;
function Currencies() {
    _s1();
    const access = (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$provider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useApiAccess"])();
    const list = (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$async$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useLoaded"])(access.status === 'ready' ? 'currency' : null, {
        "Currencies.useLoaded[list]": ()=>access.status === 'ready' ? access.client.entity.currency.list({
                limit: 10
            }) : Promise.reject()
    }["Currencies.useLoaded[list]"]);
    if (list.status !== 'ready') return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Loading"], {}, void 0, false, {
        fileName: "[project]/presentation/preview/demo.tsx",
        lineNumber: 159,
        columnNumber: 39
    }, this);
    if (!list.value.ok) return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["ErrorNotice"], {
        failure: list.value.failure
    }, void 0, false, {
        fileName: "[project]/presentation/preview/demo.tsx",
        lineNumber: 160,
        columnNumber: 30
    }, this);
    const records = list.value.value;
    const sample = records[0] ?? {};
    const fields = Object.entries(sample).map(([name, value])=>({
            name,
            kind: kindOf(value),
            required: false
        }));
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$record$2d$table$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["RecordTable"], {
        caption: "Currencies",
        fields: fields,
        records: records,
        emptyTitle: "No currencies",
        rowActions: (record)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
                children: [
                    "Open ",
                    String(record.code)
                ]
            }, void 0, true, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 176,
                columnNumber: 31
            }, this)
    }, void 0, false, {
        fileName: "[project]/presentation/preview/demo.tsx",
        lineNumber: 171,
        columnNumber: 5
    }, this);
}
_s1(Currencies, "zgb2RNTAnk4xaq0huANPhWuhLT0=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$api$2f$provider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useApiAccess"],
        __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$async$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useLoaded"]
    ];
});
_c2 = Currencies;
function Gallery() {
    _s2();
    const [filters, setFilters] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$filter$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["noFilters"]);
    const [order, setOrder] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$order$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["unordered"]);
    const [entry, setEntry] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])({
        state: 'empty'
    });
    const [asking, setAsking] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [request, setRequest] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])((0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$aggregate$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["firstRequest"])(AGGREGATES));
    const [submitted, setSubmitted] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])('');
    const [result, setResult] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(undefined);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$preview$2f$demo$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].stack,
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                children: "Feedback"
            }, void 0, false, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 191,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$preview$2f$demo$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].row,
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Loading"], {}, void 0, false, {
                        fileName: "[project]/presentation/preview/demo.tsx",
                        lineNumber: 193,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Success"], {
                        children: "Saved."
                    }, void 0, false, {
                        fileName: "[project]/presentation/preview/demo.tsx",
                        lineNumber: 194,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Empty"], {
                        title: "No records yet",
                        children: "Add the first record to get started."
                    }, void 0, false, {
                        fileName: "[project]/presentation/preview/demo.tsx",
                        lineNumber: 195,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["ErrorNotice"], {
                        failure: {
                            kind: 'problem',
                            problem: {
                                type: 'InvalidInputError',
                                status: 422,
                                title: 'Unprocessable Content',
                                detail: "'nope' is not a Field of Account"
                            }
                        }
                    }, void 0, false, {
                        fileName: "[project]/presentation/preview/demo.tsx",
                        lineNumber: 198,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 192,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                children: "Inputs"
            }, void 0, false, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 210,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$preview$2f$demo$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].row,
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$input$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["FieldInput"], {
                        field: {
                            name: 'unit_price',
                            kind: 'decimal',
                            required: true
                        },
                        entry: entry,
                        onChange: setEntry
                    }, void 0, false, {
                        fileName: "[project]/presentation/preview/demo.tsx",
                        lineNumber: 212,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$input$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["FieldInput"], {
                        field: {
                            name: 'note',
                            kind: 'string',
                            required: false
                        },
                        entry: {
                            state: 'empty'
                        },
                        onChange: ()=>{}
                    }, void 0, false, {
                        fileName: "[project]/presentation/preview/demo.tsx",
                        lineNumber: 217,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 211,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                children: "Filters, order and limit"
            }, void 0, false, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 223,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$filter$2d$editor$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["FilterEditor"], {
                fields: SAMPLE_FIELDS,
                operators: OPERATORS,
                combinations: [
                    'AND',
                    'OR'
                ],
                draft: filters,
                onChange: setFilters
            }, void 0, false, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 224,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$order$2d$controls$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["OrderControls"], {
                fields: SAMPLE_FIELDS,
                directions: [
                    'ASCENDING',
                    'DESCENDING'
                ],
                value: order,
                onChange: setOrder
            }, void 0, false, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 231,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                children: "Aggregates"
            }, void 0, false, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 237,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$aggregate$2d$panel$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["AggregatePanel"], {
                operations: AGGREGATES,
                filterFields: SAMPLE_FIELDS,
                filterOperators: OPERATORS,
                combinations: [
                    'AND',
                    'OR'
                ],
                value: request,
                onChange: setRequest,
                onRun: (r)=>setResult(r.operation === 'count' ? 42 : '1234.50'),
                result: result
            }, void 0, false, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 238,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                children: "Form"
            }, void 0, false, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 248,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$record$2d$form$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["RecordForm"], {
                fields: SAMPLE_FIELDS,
                submitLabel: "Add record",
                onSubmit: (entries)=>setSubmitted(Object.entries(entries).map(([k, v])=>`${k}: ${v.state}`).join(', '))
            }, void 0, false, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 249,
                columnNumber: 7
            }, this),
            submitted !== '' && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Success"], {
                children: submitted
            }, void 0, false, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 260,
                columnNumber: 28
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                children: "Confirmation"
            }, void 0, false, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 261,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
                        variant: "danger",
                        onClick: ()=>setAsking(true),
                        children: "Delete something"
                    }, void 0, false, {
                        fileName: "[project]/presentation/preview/demo.tsx",
                        lineNumber: 263,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$confirmation$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Confirmation"], {
                        open: asking,
                        question: "Delete the User with id 4?",
                        confirmLabel: "Delete user",
                        onConfirm: ()=>setAsking(false),
                        onCancel: ()=>setAsking(false)
                    }, void 0, false, {
                        fileName: "[project]/presentation/preview/demo.tsx",
                        lineNumber: 266,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 262,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/presentation/preview/demo.tsx",
        lineNumber: 190,
        columnNumber: 5
    }, this);
}
_s2(Gallery, "g5TwNHpJeJb6+hrYQoq3FX3rWFM=");
_c3 = Gallery;
function Demo() {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$page$2d$frame$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["PageFrame"], {
        applicationTitle: "Trading Assistant",
        heading: "Preview",
        navigation: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("ul", {
            className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$preview$2f$demo$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].nav,
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("a", {
                        href: "#connection",
                        children: "API connection"
                    }, void 0, false, {
                        fileName: "[project]/presentation/preview/demo.tsx",
                        lineNumber: 286,
                        columnNumber: 13
                    }, this)
                }, void 0, false, {
                    fileName: "[project]/presentation/preview/demo.tsx",
                    lineNumber: 285,
                    columnNumber: 11
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("a", {
                        href: "#data",
                        children: "Live data"
                    }, void 0, false, {
                        fileName: "[project]/presentation/preview/demo.tsx",
                        lineNumber: 289,
                        columnNumber: 13
                    }, this)
                }, void 0, false, {
                    fileName: "[project]/presentation/preview/demo.tsx",
                    lineNumber: 288,
                    columnNumber: 11
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("a", {
                        href: "#theme",
                        children: "Theme"
                    }, void 0, false, {
                        fileName: "[project]/presentation/preview/demo.tsx",
                        lineNumber: 292,
                        columnNumber: 13
                    }, this)
                }, void 0, false, {
                    fileName: "[project]/presentation/preview/demo.tsx",
                    lineNumber: 291,
                    columnNumber: 11
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("a", {
                        href: "#components",
                        children: "Components"
                    }, void 0, false, {
                        fileName: "[project]/presentation/preview/demo.tsx",
                        lineNumber: 295,
                        columnNumber: 13
                    }, this)
                }, void 0, false, {
                    fileName: "[project]/presentation/preview/demo.tsx",
                    lineNumber: 294,
                    columnNumber: 11
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/presentation/preview/demo.tsx",
            lineNumber: 284,
            columnNumber: 9
        }, this),
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$preview$2f$demo$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].note,
                children: "A temporary preview of the Theme and the built Components. The real pages (one Section per Entity) are not built yet."
            }, void 0, false, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 300,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(Block, {
                id: "connection",
                title: "API connection",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(Connection, {}, void 0, false, {
                    fileName: "[project]/presentation/preview/demo.tsx",
                    lineNumber: 305,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 304,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(Block, {
                id: "data",
                title: "Live data",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(Currencies, {}, void 0, false, {
                    fileName: "[project]/presentation/preview/demo.tsx",
                    lineNumber: 308,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 307,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(Block, {
                id: "theme",
                title: "Theme",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$preview$2f$demo$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].swatches,
                        children: SWATCHES.map((name)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$preview$2f$demo$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].swatch,
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$preview$2f$demo$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].chip,
                                        style: {
                                            background: `var(--color-${name})`
                                        }
                                    }, void 0, false, {
                                        fileName: "[project]/presentation/preview/demo.tsx",
                                        lineNumber: 314,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                                        children: name
                                    }, void 0, false, {
                                        fileName: "[project]/presentation/preview/demo.tsx",
                                        lineNumber: 318,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, name, true, {
                                fileName: "[project]/presentation/preview/demo.tsx",
                                lineNumber: 313,
                                columnNumber: 13
                            }, this))
                    }, void 0, false, {
                        fileName: "[project]/presentation/preview/demo.tsx",
                        lineNumber: 311,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        dir: "auto",
                        children: "نمونهٔ متن راست‌به‌چپ: جهت متن به‌صورت خودکار از محتوا تشخیص داده می‌شود."
                    }, void 0, false, {
                        fileName: "[project]/presentation/preview/demo.tsx",
                        lineNumber: 322,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 310,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(Block, {
                id: "components",
                title: "Components",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(Gallery, {}, void 0, false, {
                    fileName: "[project]/presentation/preview/demo.tsx",
                    lineNumber: 328,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/presentation/preview/demo.tsx",
                lineNumber: 327,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/presentation/preview/demo.tsx",
        lineNumber: 280,
        columnNumber: 5
    }, this);
}
_c4 = Demo;
var _c, _c1, _c2, _c3, _c4;
__turbopack_context__.k.register(_c, "Block");
__turbopack_context__.k.register(_c1, "Connection");
__turbopack_context__.k.register(_c2, "Currencies");
__turbopack_context__.k.register(_c3, "Gallery");
__turbopack_context__.k.register(_c4, "Demo");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/theme/theme.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/** Marks an element whose text direction follows its own content. */ __turbopack_context__.s([
    "autoDirection",
    ()=>autoDirection
]);
const autoDirection = {
    dir: 'auto'
};
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/view/aggregate-panel.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "AggregatePanel",
    ()=>AggregatePanel
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$aggregate$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/interaction/aggregate.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/theme/theme.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/button.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$filter$2d$editor$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/filter-editor.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$label$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/field-label.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$aggregate$2d$panel$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/presentation/view/aggregate-panel.module.css [app-client] (css module)");
'use client';
;
;
;
;
;
;
;
function shown(result) {
    if (result === null) return 'No value';
    if (typeof result === 'boolean') return result ? 'Yes' : 'No';
    return String(result);
}
function AggregatePanel({ operations, filterFields, filterOperators, combinations, value, onChange, onRun, result, problems, busy = false }) {
    const operation = operations.find((o)=>o.name === value.operation);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$aggregate$2d$panel$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].panel,
        "aria-label": "Count and aggregates",
        ...__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["autoDirection"],
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$aggregate$2d$panel$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].choices,
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$aggregate$2d$panel$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].part,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                children: "Operation"
                            }, void 0, false, {
                                fileName: "[project]/presentation/view/aggregate-panel.tsx",
                                lineNumber: 65,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$aggregate$2d$panel$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].select,
                                value: value.operation,
                                onChange: (event)=>{
                                    const chosen = operations.find((o)=>o.name === event.target.value);
                                    if (chosen !== undefined) onChange((0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$aggregate$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["changeOperation"])(value, chosen));
                                },
                                children: operations.map((o)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                        value: o.name,
                                        children: o.name
                                    }, o.name, false, {
                                        fileName: "[project]/presentation/view/aggregate-panel.tsx",
                                        lineNumber: 77,
                                        columnNumber: 15
                                    }, this))
                            }, void 0, false, {
                                fileName: "[project]/presentation/view/aggregate-panel.tsx",
                                lineNumber: 66,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/presentation/view/aggregate-panel.tsx",
                        lineNumber: 64,
                        columnNumber: 9
                    }, this),
                    operation?.fields !== undefined && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$aggregate$2d$panel$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].part,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                children: "Field"
                            }, void 0, false, {
                                fileName: "[project]/presentation/view/aggregate-panel.tsx",
                                lineNumber: 85,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$aggregate$2d$panel$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].select,
                                value: value.field ?? '',
                                onChange: (event)=>onChange({
                                        ...value,
                                        field: event.target.value
                                    }),
                                children: operation.fields.map((f)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                        value: f.name,
                                        children: (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$label$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["fieldLabel"])(f)
                                    }, f.name, false, {
                                        fileName: "[project]/presentation/view/aggregate-panel.tsx",
                                        lineNumber: 94,
                                        columnNumber: 17
                                    }, this))
                            }, void 0, false, {
                                fileName: "[project]/presentation/view/aggregate-panel.tsx",
                                lineNumber: 86,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/presentation/view/aggregate-panel.tsx",
                        lineNumber: 84,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/presentation/view/aggregate-panel.tsx",
                lineNumber: 63,
                columnNumber: 7
            }, this),
            operation?.takesFilters === true && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$filter$2d$editor$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["FilterEditor"], {
                fields: filterFields,
                operators: filterOperators,
                combinations: combinations,
                draft: value.filters,
                onChange: (filters)=>onChange({
                        ...value,
                        filters
                    }),
                problems: problems
            }, void 0, false, {
                fileName: "[project]/presentation/view/aggregate-panel.tsx",
                lineNumber: 103,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$aggregate$2d$panel$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].run,
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
                        variant: "primary",
                        disabled: busy || operation === undefined,
                        onClick: ()=>onRun(value),
                        children: "Calculate"
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/aggregate-panel.tsx",
                        lineNumber: 113,
                        columnNumber: 9
                    }, this),
                    result !== undefined && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("output", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$aggregate$2d$panel$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].result,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$aggregate$2d$panel$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].resultLabel,
                                children: "Result"
                            }, void 0, false, {
                                fileName: "[project]/presentation/view/aggregate-panel.tsx",
                                lineNumber: 122,
                                columnNumber: 13
                            }, this),
                            ' ',
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                children: shown(result)
                            }, void 0, false, {
                                fileName: "[project]/presentation/view/aggregate-panel.tsx",
                                lineNumber: 123,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/presentation/view/aggregate-panel.tsx",
                        lineNumber: 121,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/presentation/view/aggregate-panel.tsx",
                lineNumber: 112,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/presentation/view/aggregate-panel.tsx",
        lineNumber: 58,
        columnNumber: 5
    }, this);
}
_c = AggregatePanel;
var _c;
__turbopack_context__.k.register(_c, "AggregatePanel");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/view/button.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Button",
    ()=>Button
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$button$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/presentation/view/button.module.css [app-client] (css module)");
;
;
function Button({ variant = 'secondary', className, type = 'button', ...rest }) {
    const classes = [
        __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$button$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].button,
        __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$button$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"][variant],
        className
    ].filter(Boolean).join(' ');
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
        ...rest,
        type: type,
        className: classes
    }, void 0, false, {
        fileName: "[project]/presentation/view/button.tsx",
        lineNumber: 18,
        columnNumber: 10
    }, this);
}
_c = Button;
var _c;
__turbopack_context__.k.register(_c, "Button");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/view/concealed.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Concealed",
    ()=>Concealed
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$concealed$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/presentation/view/concealed.module.css [app-client] (css module)");
;
;
function Concealed() {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$concealed$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].concealed,
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                "aria-hidden": "true",
                children: "••••••"
            }, void 0, false, {
                fileName: "[project]/presentation/view/concealed.tsx",
                lineNumber: 7,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$concealed$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].visuallyHidden,
                children: "Hidden"
            }, void 0, false, {
                fileName: "[project]/presentation/view/concealed.tsx",
                lineNumber: 8,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/presentation/view/concealed.tsx",
        lineNumber: 6,
        columnNumber: 5
    }, this);
}
_c = Concealed;
var _c;
__turbopack_context__.k.register(_c, "Concealed");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/view/confirmation.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Confirmation",
    ()=>Confirmation
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/theme/theme.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/button.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$confirmation$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/presentation/view/confirmation.module.css [app-client] (css module)");
;
var _s = __turbopack_context__.k.signature();
'use client';
;
;
;
;
function Confirmation({ open, question, confirmLabel, cancelLabel = 'Cancel', busy = false, onConfirm, onCancel }) {
    _s();
    const dialog = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRef"])(null);
    const questionId = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useId"])();
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "Confirmation.useEffect": ()=>{
            const element = dialog.current;
            if (element === null) return;
            if (open && !element.open) element.showModal();
            if (!open && element.open) element.close();
        }
    }["Confirmation.useEffect"], [
        open
    ]);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("dialog", {
        ref: dialog,
        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$confirmation$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].dialog,
        "aria-labelledby": questionId,
        onCancel: (event)=>{
            event.preventDefault();
            onCancel();
        },
        onClick: (event)=>{
            if (event.target === dialog.current) onCancel();
        },
        ...__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["autoDirection"],
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$confirmation$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].content,
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                    id: questionId,
                    className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$confirmation$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].question,
                    children: question
                }, void 0, false, {
                    fileName: "[project]/presentation/view/confirmation.tsx",
                    lineNumber: 52,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$confirmation$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].actions,
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
                            onClick: onCancel,
                            disabled: busy,
                            children: cancelLabel
                        }, void 0, false, {
                            fileName: "[project]/presentation/view/confirmation.tsx",
                            lineNumber: 56,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
                            variant: "danger",
                            onClick: onConfirm,
                            disabled: busy,
                            children: confirmLabel
                        }, void 0, false, {
                            fileName: "[project]/presentation/view/confirmation.tsx",
                            lineNumber: 59,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/presentation/view/confirmation.tsx",
                    lineNumber: 55,
                    columnNumber: 9
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/presentation/view/confirmation.tsx",
            lineNumber: 51,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/presentation/view/confirmation.tsx",
        lineNumber: 38,
        columnNumber: 5
    }, this);
}
_s(Confirmation, "PDYQ0cDToXkvFb34Em49RzagP5U=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useId"]
    ];
});
_c = Confirmation;
var _c;
__turbopack_context__.k.register(_c, "Confirmation");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/view/feedback.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Empty",
    ()=>Empty,
    "ErrorNotice",
    ()=>ErrorNotice,
    "Loading",
    ()=>Loading,
    "Success",
    ()=>Success
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/theme/theme.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/presentation/view/feedback.module.css [app-client] (css module)");
;
;
;
function Loading({ label = 'Loading' }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].loading,
        role: "status",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].spinner,
                "aria-hidden": "true"
            }, void 0, false, {
                fileName: "[project]/presentation/view/feedback.tsx",
                lineNumber: 9,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                children: label
            }, void 0, false, {
                fileName: "[project]/presentation/view/feedback.tsx",
                lineNumber: 10,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/presentation/view/feedback.tsx",
        lineNumber: 8,
        columnNumber: 5
    }, this);
}
_c = Loading;
function Empty({ title, children }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].empty,
        ...__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["autoDirection"],
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].emptyTitle,
                children: title
            }, void 0, false, {
                fileName: "[project]/presentation/view/feedback.tsx",
                lineNumber: 24,
                columnNumber: 7
            }, this),
            children
        ]
    }, void 0, true, {
        fileName: "[project]/presentation/view/feedback.tsx",
        lineNumber: 23,
        columnNumber: 5
    }, this);
}
_c1 = Empty;
function Success({ children }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].success,
        role: "status",
        ...__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["autoDirection"],
        children: children
    }, void 0, false, {
        fileName: "[project]/presentation/view/feedback.tsx",
        lineNumber: 32,
        columnNumber: 5
    }, this);
}
_c2 = Success;
function bodyText(body) {
    return typeof body === 'string' ? body : JSON.stringify(body);
}
function ErrorNotice({ failure }) {
    if (failure.kind === 'problem') {
        const { type, status, title, detail } = failure.problem;
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].error,
            role: "alert",
            ...__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["autoDirection"],
            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("dl", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].details,
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("dt", {
                        children: "Type"
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/feedback.tsx",
                        lineNumber: 49,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("dd", {
                        children: type
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/feedback.tsx",
                        lineNumber: 50,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("dt", {
                        children: "Status"
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/feedback.tsx",
                        lineNumber: 51,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("dd", {
                        children: status
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/feedback.tsx",
                        lineNumber: 52,
                        columnNumber: 11
                    }, this),
                    title !== null && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("dt", {
                                children: "Title"
                            }, void 0, false, {
                                fileName: "[project]/presentation/view/feedback.tsx",
                                lineNumber: 55,
                                columnNumber: 15
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("dd", {
                                children: title
                            }, void 0, false, {
                                fileName: "[project]/presentation/view/feedback.tsx",
                                lineNumber: 56,
                                columnNumber: 15
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/presentation/view/feedback.tsx",
                        lineNumber: 54,
                        columnNumber: 13
                    }, this),
                    detail !== null && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("dt", {
                                children: "Detail"
                            }, void 0, false, {
                                fileName: "[project]/presentation/view/feedback.tsx",
                                lineNumber: 61,
                                columnNumber: 15
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("dd", {
                                children: detail
                            }, void 0, false, {
                                fileName: "[project]/presentation/view/feedback.tsx",
                                lineNumber: 62,
                                columnNumber: 15
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/presentation/view/feedback.tsx",
                        lineNumber: 60,
                        columnNumber: 13
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/presentation/view/feedback.tsx",
                lineNumber: 48,
                columnNumber: 9
            }, this)
        }, void 0, false, {
            fileName: "[project]/presentation/view/feedback.tsx",
            lineNumber: 47,
            columnNumber: 7
        }, this);
    }
    if (failure.kind === 'unrecognized') {
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].error,
            role: "alert",
            ...__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["autoDirection"],
            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("dl", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].details,
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("dt", {
                        children: "Status"
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/feedback.tsx",
                        lineNumber: 73,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("dd", {
                        children: failure.status
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/feedback.tsx",
                        lineNumber: 74,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("dt", {
                        children: "Response"
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/feedback.tsx",
                        lineNumber: 75,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("dd", {
                        children: bodyText(failure.body)
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/feedback.tsx",
                        lineNumber: 76,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/presentation/view/feedback.tsx",
                lineNumber: 72,
                columnNumber: 9
            }, this)
        }, void 0, false, {
            fileName: "[project]/presentation/view/feedback.tsx",
            lineNumber: 71,
            columnNumber: 7
        }, this);
    }
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].error,
        role: "alert",
        ...__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["autoDirection"],
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
            className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].message,
            children: failure.message
        }, void 0, false, {
            fileName: "[project]/presentation/view/feedback.tsx",
            lineNumber: 83,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/presentation/view/feedback.tsx",
        lineNumber: 82,
        columnNumber: 5
    }, this);
}
_c3 = ErrorNotice;
var _c, _c1, _c2, _c3;
__turbopack_context__.k.register(_c, "Loading");
__turbopack_context__.k.register(_c1, "Empty");
__turbopack_context__.k.register(_c2, "Success");
__turbopack_context__.k.register(_c3, "ErrorNotice");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/view/field-input.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "FieldInput",
    ()=>FieldInput
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$fields$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/interaction/fields.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/theme/theme.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$label$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/field-label.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$input$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/presentation/view/field-input.module.css [app-client] (css module)");
;
var _s = __turbopack_context__.k.signature();
'use client';
;
;
;
;
;
const FORM = {
    string: 'text',
    integer: 'a whole number',
    float: 'a number',
    decimal: 'a decimal number',
    boolean: 'Yes or No',
    datetime: 'a date and time with an offset, such as 2026-01-02T03:04:05+00:00',
    uuid: 'a UUID'
};
const MODE = {
    integer: 'numeric',
    float: 'decimal',
    decimal: 'decimal'
};
function same(a, b) {
    if (a.state !== b.state) return false;
    if (a.state === 'value' && b.state === 'value') return a.value === b.value;
    if (a.state === 'invalid' && b.state === 'invalid') return a.text === b.text;
    return true;
}
function textOf(entry) {
    if (entry.state === 'value') return (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$fields$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["fieldText"])(entry.value);
    if (entry.state === 'invalid') return entry.text;
    return '';
}
function FieldInput({ field, entry, onChange, hideLabel = false, label: given, absentLabel = 'No value', problem, placeholder, disabled = false }) {
    _s();
    const id = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useId"])();
    const hint = `${id}-hint`;
    const absent = entry.state === 'absent';
    // What the user typed is kept as typed while it still means the entry the owner holds.
    const [typed, setTyped] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const shown = typed !== null && same((0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$fields$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["parseFieldText"])(field.kind, typed), entry) ? typed : textOf(entry);
    const label = given ?? (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$label$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["fieldLabel"])(field);
    const message = entry.state === 'invalid' ? `Enter ${FORM[field.kind]}.` : problem;
    const describedBy = message === undefined ? undefined : hint;
    const common = {
        id,
        disabled: disabled || absent,
        'aria-required': field.required,
        'aria-invalid': message !== undefined,
        'aria-describedby': describedBy,
        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$input$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].control,
        ...__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["autoDirection"]
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$input$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].field,
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                htmlFor: id,
                className: hideLabel ? __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$input$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].visuallyHidden : __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$input$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].label,
                children: [
                    label,
                    field.required && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$input$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].required,
                        children: " (required)"
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/field-input.tsx",
                        lineNumber: 101,
                        columnNumber: 28
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/presentation/view/field-input.tsx",
                lineNumber: 96,
                columnNumber: 7
            }, this),
            field.kind === 'boolean' && field.sensitive !== true ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                ...common,
                value: entry.state === 'value' ? String(entry.value) : '',
                onChange: (event)=>onChange((0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$fields$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["parseFieldText"])('boolean', event.target.value)),
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                        value: "",
                        children: "Choose"
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/field-input.tsx",
                        lineNumber: 111,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                        value: "true",
                        children: "Yes"
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/field-input.tsx",
                        lineNumber: 112,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                        value: "false",
                        children: "No"
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/field-input.tsx",
                        lineNumber: 113,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/presentation/view/field-input.tsx",
                lineNumber: 104,
                columnNumber: 9
            }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                ...common,
                type: field.sensitive === true ? 'password' : 'text',
                inputMode: MODE[field.kind],
                autoComplete: field.sensitive === true ? 'new-password' : 'off',
                value: shown,
                placeholder: placeholder ?? (field.default === undefined || field.sensitive === true ? undefined : (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$fields$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["fieldText"])(field.default)),
                onChange: (event)=>{
                    setTyped(event.target.value);
                    onChange((0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$fields$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["parseFieldText"])(field.kind, event.target.value));
                }
            }, void 0, false, {
                fileName: "[project]/presentation/view/field-input.tsx",
                lineNumber: 116,
                columnNumber: 9
            }, this),
            !field.required && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$input$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].absent,
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                        type: "checkbox",
                        checked: absent,
                        disabled: disabled,
                        onChange: (event)=>onChange(event.target.checked ? {
                                state: 'absent'
                            } : {
                                state: 'empty'
                            })
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/field-input.tsx",
                        lineNumber: 136,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        children: absentLabel
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/field-input.tsx",
                        lineNumber: 146,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/presentation/view/field-input.tsx",
                lineNumber: 135,
                columnNumber: 9
            }, this),
            message !== undefined && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                id: hint,
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$input$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].problem,
                role: "alert",
                children: message
            }, void 0, false, {
                fileName: "[project]/presentation/view/field-input.tsx",
                lineNumber: 150,
                columnNumber: 9
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/presentation/view/field-input.tsx",
        lineNumber: 95,
        columnNumber: 5
    }, this);
}
_s(FieldInput, "EAIf+DDWau+zz4Rw0OOOdVGaA2k=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useId"]
    ];
});
_c = FieldInput;
var _c;
__turbopack_context__.k.register(_c, "FieldInput");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/view/field-label.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "fieldLabel",
    ()=>fieldLabel
]);
function fieldLabel(field) {
    if (field.description !== undefined && field.description !== '') {
        return field.description;
    }
    const words = field.name.replace(/_/g, ' ').trim();
    return words === '' ? field.name : words.charAt(0).toUpperCase() + words.slice(1);
}
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/view/field-value.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "valueText",
    ()=>valueText
]);
function valueText(value) {
    return typeof value === 'boolean' ? value ? 'Yes' : 'No' : String(value);
}
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/view/filter-editor.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "FilterEditor",
    ()=>FilterEditor
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$filter$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/interaction/filter.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/theme/theme.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/button.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$input$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/field-input.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$label$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/field-label.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$filter$2d$editor$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/presentation/view/filter-editor.module.css [app-client] (css module)");
'use client';
;
;
;
;
;
;
;
function FilterEditor({ fields, operators, combinations, draft, onChange, problems = [] }) {
    const replace = (index, next)=>onChange({
            ...draft,
            conditions: draft.conditions.map((c, i)=>i === index ? next : c)
        });
    const add = ()=>{
        const condition = (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$filter$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["newCondition"])(fields, operators);
        if (condition === null) return;
        const conditions = [
            ...draft.conditions,
            condition
        ];
        onChange({
            conditions,
            combination: conditions.length > 1 ? draft.combination ?? combinations[0] ?? null : null
        });
    };
    const remove = (index)=>{
        const conditions = draft.conditions.filter((_, i)=>i !== index);
        onChange({
            conditions,
            combination: conditions.length > 1 ? draft.combination : null
        });
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("fieldset", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$filter$2d$editor$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].editor,
        ...__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["autoDirection"],
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("legend", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$filter$2d$editor$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].legend,
                children: "Filters"
            }, void 0, false, {
                fileName: "[project]/presentation/view/filter-editor.tsx",
                lineNumber: 68,
                columnNumber: 7
            }, this),
            draft.conditions.length === 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$filter$2d$editor$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].none,
                children: "No filters. Every record matches."
            }, void 0, false, {
                fileName: "[project]/presentation/view/filter-editor.tsx",
                lineNumber: 70,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("ul", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$filter$2d$editor$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].list,
                children: draft.conditions.map((condition, index)=>{
                    const field = fields.find((f)=>f.name === condition.field);
                    const choices = field === undefined ? [] : (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$filter$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["applicableOperators"])(operators, field);
                    const operator = operators.find((o)=>o.name === condition.operator);
                    const problem = problems[index] ?? null;
                    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$filter$2d$editor$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].condition,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$filter$2d$editor$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].part,
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: "Field"
                                    }, void 0, false, {
                                        fileName: "[project]/presentation/view/filter-editor.tsx",
                                        lineNumber: 82,
                                        columnNumber: 17
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$filter$2d$editor$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].select,
                                        value: condition.field,
                                        onChange: (event)=>{
                                            const chosen = fields.find((f)=>f.name === event.target.value);
                                            if (chosen !== undefined) {
                                                replace(index, (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$filter$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["changeField"])(condition, chosen, operators));
                                            }
                                        },
                                        children: fields.map((f)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                value: f.name,
                                                children: (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$label$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["fieldLabel"])(f)
                                            }, f.name, false, {
                                                fileName: "[project]/presentation/view/filter-editor.tsx",
                                                lineNumber: 96,
                                                columnNumber: 21
                                            }, this))
                                    }, void 0, false, {
                                        fileName: "[project]/presentation/view/filter-editor.tsx",
                                        lineNumber: 83,
                                        columnNumber: 17
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/presentation/view/filter-editor.tsx",
                                lineNumber: 81,
                                columnNumber: 15
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$filter$2d$editor$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].part,
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: "Operator"
                                    }, void 0, false, {
                                        fileName: "[project]/presentation/view/filter-editor.tsx",
                                        lineNumber: 103,
                                        columnNumber: 17
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$filter$2d$editor$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].select,
                                        value: condition.operator,
                                        onChange: (event)=>{
                                            const chosen = choices.find((o)=>o.name === event.target.value);
                                            if (chosen !== undefined) {
                                                replace(index, (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$filter$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["changeOperator"])(condition, chosen, operator));
                                            }
                                        },
                                        children: choices.map((o)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                value: o.name,
                                                children: o.name
                                            }, o.name, false, {
                                                fileName: "[project]/presentation/view/filter-editor.tsx",
                                                lineNumber: 120,
                                                columnNumber: 21
                                            }, this))
                                    }, void 0, false, {
                                        fileName: "[project]/presentation/view/filter-editor.tsx",
                                        lineNumber: 104,
                                        columnNumber: 17
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/presentation/view/filter-editor.tsx",
                                lineNumber: 102,
                                columnNumber: 15
                            }, this),
                            field !== undefined && operator !== undefined && operator.value !== 'none' && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$filter$2d$editor$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].values,
                                children: [
                                    condition.values.map((entry, valueIndex)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$filter$2d$editor$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].value,
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$input$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["FieldInput"], {
                                                    field: {
                                                        name: 'value',
                                                        kind: field.kind,
                                                        required: true,
                                                        sensitive: field.sensitive === true
                                                    },
                                                    entry: entry,
                                                    hideLabel: true,
                                                    onChange: (next)=>replace(index, {
                                                            ...condition,
                                                            values: condition.values.map((v, i)=>i === valueIndex ? next : v)
                                                        })
                                                }, void 0, false, {
                                                    fileName: "[project]/presentation/view/filter-editor.tsx",
                                                    lineNumber: 132,
                                                    columnNumber: 25
                                                }, this),
                                                operator.value === 'many' && condition.values.length > 1 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
                                                    onClick: ()=>replace(index, {
                                                            ...condition,
                                                            values: condition.values.filter((_, i)=>i !== valueIndex)
                                                        }),
                                                    children: "Remove value"
                                                }, void 0, false, {
                                                    fileName: "[project]/presentation/view/filter-editor.tsx",
                                                    lineNumber: 152,
                                                    columnNumber: 29
                                                }, this)
                                            ]
                                        }, valueIndex, true, {
                                            fileName: "[project]/presentation/view/filter-editor.tsx",
                                            lineNumber: 131,
                                            columnNumber: 23
                                        }, this)),
                                    operator.value === 'many' && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
                                        onClick: ()=>replace(index, {
                                                ...condition,
                                                values: [
                                                    ...condition.values,
                                                    {
                                                        state: 'empty'
                                                    }
                                                ]
                                            }),
                                        children: "Add value"
                                    }, void 0, false, {
                                        fileName: "[project]/presentation/view/filter-editor.tsx",
                                        lineNumber: 168,
                                        columnNumber: 23
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/presentation/view/filter-editor.tsx",
                                lineNumber: 129,
                                columnNumber: 19
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
                                onClick: ()=>remove(index),
                                children: "Remove filter"
                            }, void 0, false, {
                                fileName: "[project]/presentation/view/filter-editor.tsx",
                                lineNumber: 181,
                                columnNumber: 15
                            }, this),
                            problem !== null && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$filter$2d$editor$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].problem,
                                role: "alert",
                                children: problem
                            }, void 0, false, {
                                fileName: "[project]/presentation/view/filter-editor.tsx",
                                lineNumber: 183,
                                columnNumber: 17
                            }, this)
                        ]
                    }, index, true, {
                        fileName: "[project]/presentation/view/filter-editor.tsx",
                        lineNumber: 80,
                        columnNumber: 13
                    }, this);
                })
            }, void 0, false, {
                fileName: "[project]/presentation/view/filter-editor.tsx",
                lineNumber: 72,
                columnNumber: 7
            }, this),
            draft.conditions.length > 1 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$filter$2d$editor$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].part,
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        children: "Combine filters with"
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/filter-editor.tsx",
                        lineNumber: 193,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$filter$2d$editor$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].select,
                        value: draft.combination ?? '',
                        onChange: (event)=>onChange({
                                ...draft,
                                combination: event.target.value
                            }),
                        children: combinations.map((name)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                value: name,
                                children: name
                            }, name, false, {
                                fileName: "[project]/presentation/view/filter-editor.tsx",
                                lineNumber: 202,
                                columnNumber: 15
                            }, this))
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/filter-editor.tsx",
                        lineNumber: 194,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/presentation/view/filter-editor.tsx",
                lineNumber: 192,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
                    onClick: add,
                    disabled: fields.length === 0,
                    children: "Add filter"
                }, void 0, false, {
                    fileName: "[project]/presentation/view/filter-editor.tsx",
                    lineNumber: 210,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/presentation/view/filter-editor.tsx",
                lineNumber: 209,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/presentation/view/filter-editor.tsx",
        lineNumber: 67,
        columnNumber: 5
    }, this);
}
_c = FilterEditor;
var _c;
__turbopack_context__.k.register(_c, "FilterEditor");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/view/order-controls.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "OrderControls",
    ()=>OrderControls
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/theme/theme.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$input$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/field-input.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$label$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/field-label.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$order$2d$controls$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/presentation/view/order-controls.module.css [app-client] (css module)");
'use client';
;
;
;
;
;
function OrderControls({ fields, directions, value, onChange }) {
    const { order, limit } = value;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("fieldset", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$order$2d$controls$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].controls,
        ...__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["autoDirection"],
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("legend", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$order$2d$controls$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].legend,
                children: "Order and limit"
            }, void 0, false, {
                fileName: "[project]/presentation/view/order-controls.tsx",
                lineNumber: 24,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$order$2d$controls$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].part,
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        children: "Order by"
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/order-controls.tsx",
                        lineNumber: 26,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$order$2d$controls$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].select,
                        value: order?.field ?? '',
                        onChange: (event)=>{
                            const field = event.target.value;
                            onChange({
                                ...value,
                                order: field === '' ? null : {
                                    field,
                                    direction: order?.direction ?? directions[0] ?? ''
                                }
                            });
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                value: "",
                                children: "No order"
                            }, void 0, false, {
                                fileName: "[project]/presentation/view/order-controls.tsx",
                                lineNumber: 44,
                                columnNumber: 11
                            }, this),
                            fields.map((f)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                    value: f.name,
                                    children: (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$label$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["fieldLabel"])(f)
                                }, f.name, false, {
                                    fileName: "[project]/presentation/view/order-controls.tsx",
                                    lineNumber: 46,
                                    columnNumber: 13
                                }, this))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/presentation/view/order-controls.tsx",
                        lineNumber: 27,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/presentation/view/order-controls.tsx",
                lineNumber: 25,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$order$2d$controls$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].part,
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        children: "Direction"
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/order-controls.tsx",
                        lineNumber: 53,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$order$2d$controls$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].select,
                        value: order?.direction ?? '',
                        disabled: order === null,
                        onChange: (event)=>{
                            if (order !== null) {
                                onChange({
                                    ...value,
                                    order: {
                                        ...order,
                                        direction: event.target.value
                                    }
                                });
                            }
                        },
                        children: [
                            order === null && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                value: ""
                            }, void 0, false, {
                                fileName: "[project]/presentation/view/order-controls.tsx",
                                lineNumber: 67,
                                columnNumber: 30
                            }, this),
                            directions.map((name)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                    value: name,
                                    children: name
                                }, name, false, {
                                    fileName: "[project]/presentation/view/order-controls.tsx",
                                    lineNumber: 69,
                                    columnNumber: 13
                                }, this))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/presentation/view/order-controls.tsx",
                        lineNumber: 54,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/presentation/view/order-controls.tsx",
                lineNumber: 52,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$order$2d$controls$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].limit,
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$input$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["FieldInput"], {
                    field: {
                        name: 'limit',
                        kind: 'integer',
                        required: false
                    },
                    entry: limit,
                    label: "Limit",
                    absentLabel: "No limit",
                    onChange: (next)=>onChange({
                            ...value,
                            limit: next
                        })
                }, void 0, false, {
                    fileName: "[project]/presentation/view/order-controls.tsx",
                    lineNumber: 76,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/presentation/view/order-controls.tsx",
                lineNumber: 75,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/presentation/view/order-controls.tsx",
        lineNumber: 23,
        columnNumber: 5
    }, this);
}
_c = OrderControls;
var _c;
__turbopack_context__.k.register(_c, "OrderControls");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/view/page-frame.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "PageFrame",
    ()=>PageFrame
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/theme/theme.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$page$2d$frame$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/presentation/view/page-frame.module.css [app-client] (css module)");
;
;
;
function PageFrame({ applicationTitle, navigation, heading, children }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$page$2d$frame$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].frame,
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("a", {
                href: "#content",
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$page$2d$frame$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].skip,
                children: "Skip to content"
            }, void 0, false, {
                fileName: "[project]/presentation/view/page-frame.tsx",
                lineNumber: 23,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("header", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$page$2d$frame$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].header,
                ...__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["autoDirection"],
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                    className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$page$2d$frame$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].title,
                    children: applicationTitle
                }, void 0, false, {
                    fileName: "[project]/presentation/view/page-frame.tsx",
                    lineNumber: 27,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/presentation/view/page-frame.tsx",
                lineNumber: 26,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$page$2d$frame$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].body,
                children: [
                    navigation !== undefined && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("nav", {
                        "aria-label": "Main",
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$page$2d$frame$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].navigation,
                        children: navigation
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/page-frame.tsx",
                        lineNumber: 31,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("main", {
                        id: "content",
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$page$2d$frame$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].main,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$page$2d$frame$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].heading,
                                ...__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["autoDirection"],
                                children: heading
                            }, void 0, false, {
                                fileName: "[project]/presentation/view/page-frame.tsx",
                                lineNumber: 36,
                                columnNumber: 11
                            }, this),
                            children
                        ]
                    }, void 0, true, {
                        fileName: "[project]/presentation/view/page-frame.tsx",
                        lineNumber: 35,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/presentation/view/page-frame.tsx",
                lineNumber: 29,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/presentation/view/page-frame.tsx",
        lineNumber: 22,
        columnNumber: 5
    }, this);
}
_c = PageFrame;
var _c;
__turbopack_context__.k.register(_c, "PageFrame");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/view/record-form.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "RecordForm",
    ()=>RecordForm
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$fields$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/interaction/fields.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/theme/theme.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/button.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/feedback.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$label$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/field-label.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$input$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/field-input.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$related$2d$record$2d$choice$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/related-record-choice.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$shown$2d$field$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/shown-field.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$record$2d$form$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/presentation/view/record-form.module.css [app-client] (css module)");
;
var _s = __turbopack_context__.k.signature();
'use client';
;
;
;
;
;
;
;
;
;
;
function initial(fields, record) {
    const entries = {};
    for (const field of fields.filter(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$fields$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["isEnterable"])){
        const stored = record?.[field.name];
        if (record !== undefined && field.sensitive === true) {
            // A stored sensitive value is never put in front of the user.
            entries[field.name] = {
                state: 'empty'
            };
        } else if (record !== undefined && stored !== undefined) {
            entries[field.name] = stored === null ? field.required ? {
                state: 'empty'
            } : {
                state: 'absent'
            } : {
                state: 'value',
                value: stored
            };
        } else if (record === undefined && field.default !== undefined) {
            entries[field.name] = field.default === null ? {
                state: 'absent'
            } : {
                state: 'value',
                value: field.default
            };
        } else {
            entries[field.name] = {
                state: 'empty'
            };
        }
    }
    return entries;
}
function RecordForm({ fields, record, submitLabel, busy = false, problems = {}, related, onSubmit }) {
    _s();
    const [entries, setEntries] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])({
        "RecordForm.useState": ()=>initial(fields, record)
    }["RecordForm.useState"]);
    const submit = (event)=>{
        event.preventDefault();
        onSubmit(entries);
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("form", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$record$2d$form$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].form,
        onSubmit: submit,
        noValidate: true,
        ...__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["autoDirection"],
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$record$2d$form$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].fields,
                children: fields.map((field)=>{
                    const choice = field.relation !== undefined && related?.status === 'ready' ? related.choices[field.name] : undefined;
                    if ((0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$fields$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["isEnterable"])(field) && field.relation !== undefined && related?.status === 'loading') {
                        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Loading"], {
                            label: `Loading ${(0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$label$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["fieldLabel"])(field)}`
                        }, field.name, false, {
                            fileName: "[project]/presentation/view/record-form.tsx",
                            lineNumber: 99,
                            columnNumber: 15
                        }, this);
                    }
                    if (choice?.status === 'failed') {
                        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["ErrorNotice"], {
                            failure: choice.failure
                        }, field.name, false, {
                            fileName: "[project]/presentation/view/record-form.tsx",
                            lineNumber: 106,
                            columnNumber: 20
                        }, this);
                    }
                    if (choice?.status === 'ready') {
                        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$related$2d$record$2d$choice$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["RelatedRecordChoice"], {
                            field: field,
                            records: choice.records,
                            valueField: choice.valueField,
                            describe: choice.describe,
                            entry: entries[field.name] ?? {
                                state: 'empty'
                            },
                            problem: problems[field.name],
                            disabled: busy,
                            onChange: (next)=>setEntries((current)=>({
                                        ...current,
                                        [field.name]: next
                                    }))
                        }, field.name, false, {
                            fileName: "[project]/presentation/view/record-form.tsx",
                            lineNumber: 110,
                            columnNumber: 15
                        }, this);
                    }
                    return (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$interaction$2f$fields$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["isEnterable"])(field) ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$input$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["FieldInput"], {
                        field: field,
                        entry: entries[field.name] ?? {
                            state: 'empty'
                        },
                        problem: problems[field.name],
                        placeholder: record !== undefined && field.sensitive === true ? 'Leave empty to keep the current value' : undefined,
                        disabled: busy,
                        onChange: (next)=>setEntries((current)=>({
                                    ...current,
                                    [field.name]: next
                                }))
                    }, field.name, false, {
                        fileName: "[project]/presentation/view/record-form.tsx",
                        lineNumber: 126,
                        columnNumber: 13
                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$shown$2d$field$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["ShownField"], {
                        field: field,
                        value: record?.[field.name]
                    }, field.name, false, {
                        fileName: "[project]/presentation/view/record-form.tsx",
                        lineNumber: 142,
                        columnNumber: 13
                    }, this);
                })
            }, void 0, false, {
                fileName: "[project]/presentation/view/record-form.tsx",
                lineNumber: 87,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$record$2d$form$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].actions,
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
                    type: "submit",
                    variant: "primary",
                    disabled: busy,
                    children: submitLabel
                }, void 0, false, {
                    fileName: "[project]/presentation/view/record-form.tsx",
                    lineNumber: 151,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/presentation/view/record-form.tsx",
                lineNumber: 150,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/presentation/view/record-form.tsx",
        lineNumber: 81,
        columnNumber: 5
    }, this);
}
_s(RecordForm, "L5jk0+/qTKIesPZ6QflCO3lmvA8=");
_c = RecordForm;
var _c;
__turbopack_context__.k.register(_c, "RecordForm");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/view/record-table.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "RecordTable",
    ()=>RecordTable
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/theme/theme.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$concealed$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/concealed.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/feedback.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$label$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/field-label.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$value$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/field-value.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$record$2d$table$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/presentation/view/record-table.module.css [app-client] (css module)");
;
;
;
;
;
;
;
const NUMERIC = new Set([
    'integer',
    'float',
    'decimal'
]);
function Cell({ kind, value, sensitive }) {
    if (sensitive) {
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("td", {
            className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$record$2d$table$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].text,
            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$concealed$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Concealed"], {}, void 0, false, {
                fileName: "[project]/presentation/view/record-table.tsx",
                lineNumber: 45,
                columnNumber: 9
            }, this)
        }, void 0, false, {
            fileName: "[project]/presentation/view/record-table.tsx",
            lineNumber: 44,
            columnNumber: 7
        }, this);
    }
    if (value === null || value === undefined) {
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("td", {
            className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$record$2d$table$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].absent,
            "aria-label": "No value",
            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                "aria-hidden": "true",
                children: "–"
            }, void 0, false, {
                fileName: "[project]/presentation/view/record-table.tsx",
                lineNumber: 52,
                columnNumber: 9
            }, this)
        }, void 0, false, {
            fileName: "[project]/presentation/view/record-table.tsx",
            lineNumber: 51,
            columnNumber: 7
        }, this);
    }
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("td", {
        className: NUMERIC.has(kind) ? __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$record$2d$table$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].number : __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$record$2d$table$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].text,
        ...__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["autoDirection"],
        children: (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$value$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["valueText"])(value)
    }, void 0, false, {
        fileName: "[project]/presentation/view/record-table.tsx",
        lineNumber: 57,
        columnNumber: 5
    }, this);
}
_c = Cell;
function RecordTable({ fields, records, caption, emptyTitle = 'No records', emptyHint, rowActions }) {
    if (records.length === 0) {
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$feedback$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Empty"], {
            title: emptyTitle,
            children: emptyHint
        }, void 0, false, {
            fileName: "[project]/presentation/view/record-table.tsx",
            lineNumber: 76,
            columnNumber: 12
        }, this);
    }
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$record$2d$table$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].scroll,
        role: "region",
        "aria-label": caption,
        tabIndex: 0,
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("table", {
            className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$record$2d$table$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].table,
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("caption", {
                    className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$record$2d$table$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].caption,
                    children: caption
                }, void 0, false, {
                    fileName: "[project]/presentation/view/record-table.tsx",
                    lineNumber: 86,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("thead", {
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("tr", {
                        children: [
                            fields.map((field)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("th", {
                                    scope: "col",
                                    className: NUMERIC.has(field.kind) ? __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$record$2d$table$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].number : undefined,
                                    children: (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$label$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["fieldLabel"])(field)
                                }, field.name, false, {
                                    fileName: "[project]/presentation/view/record-table.tsx",
                                    lineNumber: 90,
                                    columnNumber: 15
                                }, this)),
                            rowActions !== undefined && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("th", {
                                scope: "col",
                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                    className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$record$2d$table$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].visuallyHidden,
                                    children: "Actions"
                                }, void 0, false, {
                                    fileName: "[project]/presentation/view/record-table.tsx",
                                    lineNumber: 100,
                                    columnNumber: 17
                                }, this)
                            }, void 0, false, {
                                fileName: "[project]/presentation/view/record-table.tsx",
                                lineNumber: 99,
                                columnNumber: 15
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/presentation/view/record-table.tsx",
                        lineNumber: 88,
                        columnNumber: 11
                    }, this)
                }, void 0, false, {
                    fileName: "[project]/presentation/view/record-table.tsx",
                    lineNumber: 87,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("tbody", {
                    children: records.map((record, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("tr", {
                            children: [
                                fields.map((field)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(Cell, {
                                        kind: field.kind,
                                        value: record[field.name],
                                        sensitive: field.sensitive === true
                                    }, field.name, false, {
                                        fileName: "[project]/presentation/view/record-table.tsx",
                                        lineNumber: 109,
                                        columnNumber: 17
                                    }, this)),
                                rowActions !== undefined && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("td", {
                                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$record$2d$table$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].actions,
                                        children: rowActions(record)
                                    }, void 0, false, {
                                        fileName: "[project]/presentation/view/record-table.tsx",
                                        lineNumber: 118,
                                        columnNumber: 19
                                    }, this)
                                }, void 0, false, {
                                    fileName: "[project]/presentation/view/record-table.tsx",
                                    lineNumber: 117,
                                    columnNumber: 17
                                }, this)
                            ]
                        }, index, true, {
                            fileName: "[project]/presentation/view/record-table.tsx",
                            lineNumber: 107,
                            columnNumber: 13
                        }, this))
                }, void 0, false, {
                    fileName: "[project]/presentation/view/record-table.tsx",
                    lineNumber: 105,
                    columnNumber: 9
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/presentation/view/record-table.tsx",
            lineNumber: 85,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/presentation/view/record-table.tsx",
        lineNumber: 79,
        columnNumber: 5
    }, this);
}
_c1 = RecordTable;
var _c, _c1;
__turbopack_context__.k.register(_c, "Cell");
__turbopack_context__.k.register(_c1, "RecordTable");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/view/related-record-choice.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "RelatedRecordChoice",
    ()=>RelatedRecordChoice
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/theme/theme.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$label$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/field-label.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$related$2d$record$2d$choice$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/presentation/view/related-record-choice.module.css [app-client] (css module)");
;
var _s = __turbopack_context__.k.signature();
'use client';
;
;
;
;
function RelatedRecordChoice({ field, records, valueField, describe, entry, onChange, hideLabel = false, label: given, absentLabel = 'No value', problem, disabled = false }) {
    _s();
    const id = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useId"])();
    const hint = `${id}-hint`;
    const absent = entry.state === 'absent';
    const chosen = entry.state === 'value' ? records.findIndex((record)=>record[valueField] === entry.value) : -1;
    const label = given ?? (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$label$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["fieldLabel"])(field);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$related$2d$record$2d$choice$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].field,
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                htmlFor: id,
                className: hideLabel ? __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$related$2d$record$2d$choice$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].visuallyHidden : __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$related$2d$record$2d$choice$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].label,
                children: [
                    label,
                    field.required && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$related$2d$record$2d$choice$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].required,
                        children: " (required)"
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/related-record-choice.tsx",
                        lineNumber: 61,
                        columnNumber: 28
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/presentation/view/related-record-choice.tsx",
                lineNumber: 56,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                id: id,
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$related$2d$record$2d$choice$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].control,
                disabled: disabled || absent,
                "aria-required": field.required,
                "aria-invalid": problem !== undefined,
                "aria-describedby": problem === undefined ? undefined : hint,
                value: chosen === -1 ? '' : String(chosen),
                onChange: (event)=>{
                    const index = event.target.value;
                    onChange(index === '' ? {
                        state: 'empty'
                    } : {
                        state: 'value',
                        value: records[Number(index)][valueField] ?? null
                    });
                },
                ...__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["autoDirection"],
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                        value: "",
                        children: "Choose"
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/related-record-choice.tsx",
                        lineNumber: 84,
                        columnNumber: 9
                    }, this),
                    records.map((record, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                            value: String(index),
                            children: describe(record)
                        }, index, false, {
                            fileName: "[project]/presentation/view/related-record-choice.tsx",
                            lineNumber: 86,
                            columnNumber: 11
                        }, this))
                ]
            }, void 0, true, {
                fileName: "[project]/presentation/view/related-record-choice.tsx",
                lineNumber: 63,
                columnNumber: 7
            }, this),
            !field.required && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$related$2d$record$2d$choice$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].absent,
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                        type: "checkbox",
                        checked: absent,
                        disabled: disabled,
                        onChange: (event)=>onChange(event.target.checked ? {
                                state: 'absent'
                            } : {
                                state: 'empty'
                            })
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/related-record-choice.tsx",
                        lineNumber: 93,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        children: absentLabel
                    }, void 0, false, {
                        fileName: "[project]/presentation/view/related-record-choice.tsx",
                        lineNumber: 103,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/presentation/view/related-record-choice.tsx",
                lineNumber: 92,
                columnNumber: 9
            }, this),
            problem !== undefined && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                id: hint,
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$related$2d$record$2d$choice$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].problem,
                role: "alert",
                children: problem
            }, void 0, false, {
                fileName: "[project]/presentation/view/related-record-choice.tsx",
                lineNumber: 107,
                columnNumber: 9
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/presentation/view/related-record-choice.tsx",
        lineNumber: 55,
        columnNumber: 5
    }, this);
}
_s(RelatedRecordChoice, "WhsuKpSQZEWeFcB7gWlfDRQktoQ=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useId"]
    ];
});
_c = RelatedRecordChoice;
var _c;
__turbopack_context__.k.register(_c, "RelatedRecordChoice");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/presentation/view/shown-field.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "ShownField",
    ()=>ShownField
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/theme/theme.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$concealed$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/concealed.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$label$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/field-label.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$value$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/presentation/view/field-value.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$shown$2d$field$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/presentation/view/shown-field.module.css [app-client] (css module)");
;
var _s = __turbopack_context__.k.signature();
;
;
;
;
;
;
function ShownField({ field, value }) {
    _s();
    const id = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useId"])();
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$shown$2d$field$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].field,
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                id: id,
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$shown$2d$field$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].label,
                children: (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$label$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["fieldLabel"])(field)
            }, void 0, false, {
                fileName: "[project]/presentation/view/shown-field.tsx",
                lineNumber: 20,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("output", {
                "aria-labelledby": id,
                className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$shown$2d$field$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].value,
                ...__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$theme$2f$theme$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["autoDirection"],
                children: field.sensitive === true ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$concealed$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Concealed"], {}, void 0, false, {
                    fileName: "[project]/presentation/view/shown-field.tsx",
                    lineNumber: 25,
                    columnNumber: 11
                }, this) : value === undefined || value === null ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                    className: __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$shown$2d$field$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].absent,
                    children: "No value"
                }, void 0, false, {
                    fileName: "[project]/presentation/view/shown-field.tsx",
                    lineNumber: 27,
                    columnNumber: 11
                }, this) : (0, __TURBOPACK__imported__module__$5b$project$5d2f$presentation$2f$view$2f$field$2d$value$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["valueText"])(value)
            }, void 0, false, {
                fileName: "[project]/presentation/view/shown-field.tsx",
                lineNumber: 23,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/presentation/view/shown-field.tsx",
        lineNumber: 19,
        columnNumber: 5
    }, this);
}
_s(ShownField, "WhsuKpSQZEWeFcB7gWlfDRQktoQ=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useId"]
    ];
});
_c = ShownField;
var _c;
__turbopack_context__.k.register(_c, "ShownField");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
]})(),
"[project]/presentation/preview/demo.module.css [app-client] (css module)", ((__turbopack_context__) => {

__turbopack_context__.v({
  "block": "demo-module__Vywchq__block",
  "chip": "demo-module__Vywchq__chip",
  "nav": "demo-module__Vywchq__nav",
  "note": "demo-module__Vywchq__note",
  "row": "demo-module__Vywchq__row",
  "stack": "demo-module__Vywchq__stack",
  "swatch": "demo-module__Vywchq__swatch",
  "swatches": "demo-module__Vywchq__swatches",
  "title": "demo-module__Vywchq__title",
});
}),
"[project]/presentation/view/aggregate-panel.module.css [app-client] (css module)", ((__turbopack_context__) => {

__turbopack_context__.v({
  "choices": "aggregate-panel-module__WaqF7q__choices",
  "panel": "aggregate-panel-module__WaqF7q__panel",
  "part": "aggregate-panel-module__WaqF7q__part",
  "result": "aggregate-panel-module__WaqF7q__result",
  "resultLabel": "aggregate-panel-module__WaqF7q__resultLabel",
  "run": "aggregate-panel-module__WaqF7q__run",
  "select": "aggregate-panel-module__WaqF7q__select",
});
}),
"[project]/presentation/view/button.module.css [app-client] (css module)", ((__turbopack_context__) => {

__turbopack_context__.v({
  "button": "button-module__Q6YdeG__button",
  "danger": "button-module__Q6YdeG__danger",
  "primary": "button-module__Q6YdeG__primary",
});
}),
"[project]/presentation/view/concealed.module.css [app-client] (css module)", ((__turbopack_context__) => {

__turbopack_context__.v({
  "concealed": "concealed-module__d7CArW__concealed",
  "visuallyHidden": "concealed-module__d7CArW__visuallyHidden" + " " + __turbopack_context__.i("[project]/presentation/view/visually-hidden.module.css [app-client] (css module)")["visuallyHidden"],
});
}),
"[project]/presentation/view/confirmation.module.css [app-client] (css module)", ((__turbopack_context__) => {

__turbopack_context__.v({
  "actions": "confirmation-module__J6w2rq__actions",
  "content": "confirmation-module__J6w2rq__content",
  "dialog": "confirmation-module__J6w2rq__dialog",
  "question": "confirmation-module__J6w2rq__question",
});
}),
"[project]/presentation/view/feedback.module.css [app-client] (css module)", ((__turbopack_context__) => {

__turbopack_context__.v({
  "details": "feedback-module__EK75ra__details",
  "empty": "feedback-module__EK75ra__empty",
  "emptyTitle": "feedback-module__EK75ra__emptyTitle",
  "error": "feedback-module__EK75ra__error",
  "loading": "feedback-module__EK75ra__loading",
  "message": "feedback-module__EK75ra__message",
  "spin": "feedback-module__EK75ra__spin",
  "spinner": "feedback-module__EK75ra__spinner",
  "success": "feedback-module__EK75ra__success",
});
}),
"[project]/presentation/view/field-input.module.css [app-client] (css module)", ((__turbopack_context__) => {

__turbopack_context__.v({
  "absent": "field-input-module__zgxNTW__absent",
  "control": "field-input-module__zgxNTW__control",
  "field": "field-input-module__zgxNTW__field",
  "label": "field-input-module__zgxNTW__label",
  "problem": "field-input-module__zgxNTW__problem",
  "required": "field-input-module__zgxNTW__required",
  "visuallyHidden": "field-input-module__zgxNTW__visuallyHidden" + " " + __turbopack_context__.i("[project]/presentation/view/visually-hidden.module.css [app-client] (css module)")["visuallyHidden"],
});
}),
"[project]/presentation/view/filter-editor.module.css [app-client] (css module)", ((__turbopack_context__) => {

__turbopack_context__.v({
  "condition": "filter-editor-module__4Tm2ya__condition",
  "editor": "filter-editor-module__4Tm2ya__editor",
  "legend": "filter-editor-module__4Tm2ya__legend",
  "list": "filter-editor-module__4Tm2ya__list",
  "none": "filter-editor-module__4Tm2ya__none",
  "part": "filter-editor-module__4Tm2ya__part",
  "problem": "filter-editor-module__4Tm2ya__problem",
  "select": "filter-editor-module__4Tm2ya__select",
  "value": "filter-editor-module__4Tm2ya__value",
  "values": "filter-editor-module__4Tm2ya__values",
});
}),
"[project]/presentation/view/order-controls.module.css [app-client] (css module)", ((__turbopack_context__) => {

__turbopack_context__.v({
  "controls": "order-controls-module__UZF33q__controls",
  "legend": "order-controls-module__UZF33q__legend",
  "limit": "order-controls-module__UZF33q__limit",
  "part": "order-controls-module__UZF33q__part",
  "select": "order-controls-module__UZF33q__select",
});
}),
"[project]/presentation/view/page-frame.module.css [app-client] (css module)", ((__turbopack_context__) => {

__turbopack_context__.v({
  "body": "page-frame-module__4Jttsa__body",
  "frame": "page-frame-module__4Jttsa__frame",
  "header": "page-frame-module__4Jttsa__header",
  "heading": "page-frame-module__4Jttsa__heading",
  "main": "page-frame-module__4Jttsa__main",
  "navigation": "page-frame-module__4Jttsa__navigation",
  "skip": "page-frame-module__4Jttsa__skip",
  "title": "page-frame-module__4Jttsa__title",
});
}),
"[project]/presentation/view/record-form.module.css [app-client] (css module)", ((__turbopack_context__) => {

__turbopack_context__.v({
  "actions": "record-form-module__x2EZnW__actions",
  "fields": "record-form-module__x2EZnW__fields",
  "form": "record-form-module__x2EZnW__form",
});
}),
"[project]/presentation/view/record-table.module.css [app-client] (css module)", ((__turbopack_context__) => {

__turbopack_context__.v({
  "absent": "record-table-module__PL-sTW__absent",
  "actions": "record-table-module__PL-sTW__actions",
  "caption": "record-table-module__PL-sTW__caption" + " " + __turbopack_context__.i("[project]/presentation/view/visually-hidden.module.css [app-client] (css module)")["visuallyHidden"],
  "number": "record-table-module__PL-sTW__number",
  "scroll": "record-table-module__PL-sTW__scroll",
  "table": "record-table-module__PL-sTW__table",
  "text": "record-table-module__PL-sTW__text",
  "visuallyHidden": "record-table-module__PL-sTW__visuallyHidden" + " " + __turbopack_context__.i("[project]/presentation/view/visually-hidden.module.css [app-client] (css module)")["visuallyHidden"],
});
}),
"[project]/presentation/view/related-record-choice.module.css [app-client] (css module)", ((__turbopack_context__) => {

__turbopack_context__.v({
  "absent": "related-record-choice-module__pmnUPG__absent" + " " + __turbopack_context__.i("[project]/presentation/view/field-input.module.css [app-client] (css module)")["absent"],
  "control": "related-record-choice-module__pmnUPG__control" + " " + __turbopack_context__.i("[project]/presentation/view/field-input.module.css [app-client] (css module)")["control"],
  "field": "related-record-choice-module__pmnUPG__field" + " " + __turbopack_context__.i("[project]/presentation/view/field-input.module.css [app-client] (css module)")["field"],
  "label": "related-record-choice-module__pmnUPG__label" + " " + __turbopack_context__.i("[project]/presentation/view/field-input.module.css [app-client] (css module)")["label"],
  "problem": "related-record-choice-module__pmnUPG__problem" + " " + __turbopack_context__.i("[project]/presentation/view/field-input.module.css [app-client] (css module)")["problem"],
  "required": "related-record-choice-module__pmnUPG__required" + " " + __turbopack_context__.i("[project]/presentation/view/field-input.module.css [app-client] (css module)")["required"],
  "visuallyHidden": "related-record-choice-module__pmnUPG__visuallyHidden" + " " + __turbopack_context__.i("[project]/presentation/view/visually-hidden.module.css [app-client] (css module)")["visuallyHidden"],
});
}),
"[project]/presentation/view/shown-field.module.css [app-client] (css module)", ((__turbopack_context__) => {

__turbopack_context__.v({
  "absent": "shown-field-module__xy-7ha__absent",
  "field": "shown-field-module__xy-7ha__field" + " " + __turbopack_context__.i("[project]/presentation/view/field-input.module.css [app-client] (css module)")["field"],
  "label": "shown-field-module__xy-7ha__label" + " " + __turbopack_context__.i("[project]/presentation/view/field-input.module.css [app-client] (css module)")["label"],
  "value": "shown-field-module__xy-7ha__value",
});
}),
"[project]/presentation/view/visually-hidden.module.css [app-client] (css module)", ((__turbopack_context__) => {

__turbopack_context__.v({
  "visuallyHidden": "visually-hidden-module__P-L1eG__visuallyHidden",
});
}),
]);

//# sourceMappingURL=presentation_1su2q-lleqjbt._.js.map