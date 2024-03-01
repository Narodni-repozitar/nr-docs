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
  render() {
    const { fieldPath, label, placeholder } = this.props;

    return (
      <IdentifiersField
        className="modal-identifiers-field"
        options={authorityIdentifiersSchema}
        fieldPath={fieldPath}
        identifierLabel={i18next.t("Identifier")}
        label={label}
        helpText={i18next.t(
          "Choose from the menu identifier type. Write the identifier without prefix (i.e. https://orcid.org/0009-0004-8646-7185 or jk01051816)."
        )}
        selectOnBlur={false}
        placeholder={placeholder}
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
  label: i18next.t("Personal identifier"),
  placeholder: i18next.t("e.g. ORCID, ISNI or GND."),
};
