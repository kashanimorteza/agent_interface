import { Refine } from '@refinedev/core';
import routerProvider from '@refinedev/react-router';
import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { BrowserRouter, Navigate, Outlet, useRoutes } from 'react-router';
import { dataProvider } from './api/dataProvider';
import { entities } from './metadata/resources.config';
import { locationOf } from './navigation/locations';
import { Navigation } from './navigation/Navigation';
import { resources } from './navigation/resources';
import { pageRoutes } from './navigation/routes';
import { PageFrame } from './shell/PageFrame';
import { DisplayModeProvider } from './theme/DisplayMode';

function Frame() {
  return (
    <PageFrame navigation={<Navigation />}>
      <Outlet />
    </PageFrame>
  );
}

const [first] = entities;

function Pages() {
  const { t } = useTranslation();
  useEffect(() => {
    document.title = t('app.title');
  }, [t]);
  return useRoutes([
    {
      element: <Frame />,
      children: [
        ...(first === undefined
          ? []
          : [{ index: true, element: <Navigate to={`/${locationOf(first)}`} replace /> }]),
        ...pageRoutes,
        { path: '*', element: null },
      ],
    },
  ]);
}

/** Presentation: the pages of every Entity behind one menu, reaching API only through API Access. */
export function App() {
  return (
    <BrowserRouter>
      <DisplayModeProvider>
        <Refine
          dataProvider={dataProvider}
          routerProvider={routerProvider}
          resources={resources}
          options={{
            disableTelemetry: true,
            syncWithLocation: false,
            warnWhenUnsavedChanges: false,
            reactQuery: { clientConfig: { defaultOptions: { queries: { retry: false } } } },
          }}
        >
          <Pages />
        </Refine>
      </DisplayModeProvider>
    </BrowserRouter>
  );
}
