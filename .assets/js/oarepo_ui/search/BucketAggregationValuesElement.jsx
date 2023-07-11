import React from "react";

import { ContribBucketAggregationValuesElement } from "@js/invenio_search_ui/components";

export const BucketAggregationValuesElement = ({ bucket, ...rest }) => {
  return (
    <ContribBucketAggregationValuesElement
      bucket={{ ...bucket, key: bucket.key.toString() }}
      {...rest}
    />
  );
};
