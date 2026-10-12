import type { ResourceProps } from '@refinedev/core';
import { entities } from '../metadata/resources.config';
import { locationOf } from './locations';

/** The framework's resources, one for every Entity of the metadata, leading to its location. */
export const resources: ResourceProps[] = entities.map((entity) => ({
  name: entity.segment,
  list: `/${locationOf(entity)}`,
  meta: { label: entity.name },
}));
