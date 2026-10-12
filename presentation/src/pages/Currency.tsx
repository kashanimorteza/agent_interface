import { PlusOutlined } from '@ant-design/icons';
import type { BaseKey } from '@refinedev/core';
import { Button, Drawer, Flex, Modal, Space, Typography } from 'antd';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { servedOperations } from '../api/served';
import { FilterEditor } from '../components/FilterEditor';
import { OrderControl } from '../components/OrderControl';
import { RecordActions } from '../components/RecordActions';
import { RecordDetails } from '../components/RecordDetails';
import { RecordForm } from '../components/RecordForm';
import { RecordTable } from '../components/RecordTable';
import { rowIdentity } from '../components/rowIdentity';
import { useRecordList } from '../components/useRecordList';
import { currency } from '../metadata/resources.config';

const served = servedOperations.currency;

type Open = { kind: 'add' } | { kind: 'edit'; id: BaseKey } | { kind: 'view'; id: BaseKey } | null;

export function CurrencyPage() {
  const { t } = useTranslation();
  const list = useRecordList(currency);
  const [open, setOpen] = useState<Open>(null);
  const close = () => {
    setOpen(null);
  };
  return (
    <Space direction="vertical" size="middle" style={{ width: '100%' }}>
      <Flex align="center" justify="space-between" gap={16}>
        <Typography.Title level={3} style={{ margin: 0 }}>
          {currency.name}
        </Typography.Title>
        {served.add && (
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => {
              setOpen({ kind: 'add' });
            }}
          >
            {t('actions.add')}
          </Button>
        )}
      </Flex>
      {served.list && (
        <>
          <FilterEditor list={list} />
          <OrderControl list={list} />
          <RecordTable
            list={list}
            actions={(row) => {
              const id = rowIdentity(currency, row);
              return (
                <Space size="small">
                  {id !== null && served.view && (
                    <Button
                      size="small"
                      onClick={() => {
                        setOpen({ kind: 'view', id });
                      }}
                    >
                      {t('actions.view')}
                    </Button>
                  )}
                  {id !== null && served.edit && (
                    <Button
                      size="small"
                      onClick={() => {
                        setOpen({ kind: 'edit', id });
                      }}
                    >
                      {t('actions.edit')}
                    </Button>
                  )}
                  <RecordActions entity={currency} row={row} />
                </Space>
              );
            }}
          />
        </>
      )}
      <Modal
        open={open?.kind === 'add' || open?.kind === 'edit'}
        title={open?.kind === 'edit' ? t('actions.edit') : t('actions.add')}
        footer={null}
        destroyOnHidden
        onCancel={close}
      >
        {open?.kind === 'add' && (
          <RecordForm entity={currency} mode="add" onSaved={close} onCancel={close} />
        )}
        {open?.kind === 'edit' && (
          <RecordForm entity={currency} mode="edit" id={open.id} onSaved={close} onCancel={close} />
        )}
      </Modal>
      <Drawer
        open={open?.kind === 'view'}
        title={currency.name}
        width={560}
        destroyOnHidden
        onClose={close}
      >
        {open?.kind === 'view' && <RecordDetails entity={currency} id={open.id} />}
      </Drawer>
    </Space>
  );
}
