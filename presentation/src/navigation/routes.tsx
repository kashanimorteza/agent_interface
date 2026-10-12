import type { RouteObject } from 'react-router';
import { UserPage } from '../pages/User';
import { TradingPlatformPage } from '../pages/TradingPlatform';
import { InstancePage } from '../pages/Instance';
import { CurrencyPage } from '../pages/Currency';
import { BrokerPage } from '../pages/Broker';
import { AssetPage } from '../pages/Asset';
import { AccountGroupPage } from '../pages/AccountGroup';
import { AccountPage } from '../pages/Account';
import { TrailingGroupPage } from '../pages/TrailingGroup';
import { TrailingRulePage } from '../pages/TrailingRule';
import { PartialGroupPage } from '../pages/PartialGroup';
import { PartialRulePage } from '../pages/PartialRule';
import { ActionGroupPage } from '../pages/ActionGroup';
import { ActionPage } from '../pages/Action';
import { PositionPage } from '../pages/Position';
import {
  user,
  tradingPlatform,
  instance,
  currency,
  broker,
  asset,
  accountGroup,
  account,
  trailingGroup,
  trailingRule,
  partialGroup,
  partialRule,
  actionGroup,
  action,
  position,
} from '../metadata/resources.config';
import { locationOf } from './locations';

/** One location for every Entity page; a location only presents its page. */
export const pageRoutes: RouteObject[] = [
  { path: locationOf(user), element: <UserPage /> },
  { path: locationOf(tradingPlatform), element: <TradingPlatformPage /> },
  { path: locationOf(instance), element: <InstancePage /> },
  { path: locationOf(currency), element: <CurrencyPage /> },
  { path: locationOf(broker), element: <BrokerPage /> },
  { path: locationOf(asset), element: <AssetPage /> },
  { path: locationOf(accountGroup), element: <AccountGroupPage /> },
  { path: locationOf(account), element: <AccountPage /> },
  { path: locationOf(trailingGroup), element: <TrailingGroupPage /> },
  { path: locationOf(trailingRule), element: <TrailingRulePage /> },
  { path: locationOf(partialGroup), element: <PartialGroupPage /> },
  { path: locationOf(partialRule), element: <PartialRulePage /> },
  { path: locationOf(actionGroup), element: <ActionGroupPage /> },
  { path: locationOf(action), element: <ActionPage /> },
  { path: locationOf(position), element: <PositionPage /> },
];
