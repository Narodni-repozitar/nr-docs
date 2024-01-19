// This file is part of Invenio-RDM-Records
// Copyright (C) 2020-2023 CERN.
// Copyright (C) 2020-2022 Northwestern University.
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio-RDM-Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React, { Component } from "react";
import PropTypes from "prop-types";
import { i18next } from "@translations/i18next";
import {
  IdentifiersField,
  authorityIdentifiersSchema,
} from "../IdentifiersField";

export class CreatibutorsIdentifiers extends Component {
  valuesToOptions = (options) =>
    options.map((option) => ({
      text: option,
      value: option,
      key: option,
    }));

  handleChange = ({ data, formikProps }) => {
    const { fieldPath } = this.props;
    formikProps.form.setFieldValue(fieldPath, data.value);
  };

  render() {
    const { fieldPath, label, placeholder } = this.props;

    return (
      <IdentifiersField
        className="modal-identifiers-field"
        options={authorityIdentifiersSchema}
        fieldPath={fieldPath}
        identifierLabel={i18next.t("Identifier")}
        noResultsMessage={i18next.t("Type the value of an identifier...")}
        label={label}
        placeholder={placeholder}
        multiple
        onChange={this.handleChange}
      />
    );
  }
}

CreatibutorsIdentifiers.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  label: PropTypes.string,
  placeholder: PropTypes.string,
};

CreatibutorsIdentifiers.defaultProps = {
  label: i18next.t("Identifiers"),
  placeholder: i18next.t("e.g. ORCID, ISNI or GND."),
};
