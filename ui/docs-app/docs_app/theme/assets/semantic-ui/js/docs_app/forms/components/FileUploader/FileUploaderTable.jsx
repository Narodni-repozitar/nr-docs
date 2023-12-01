import React from "react";
import PropTypes from "prop-types";
import { Table } from "semantic-ui-react";
import { dummyFiles } from "./dummyfiles";
import { i18next } from "@translations/docs_app/i18next";
import { humanReadableBytes } from "react-invenio-forms";

export const FileUploaderTable = ({ files = dummyFiles, removeFile }) => {
  return (
    <Table>
      <Table.Header>
        <Table.Row>
          <Table.HeaderCell>{i18next.t("File name")}</Table.HeaderCell>
          <Table.HeaderCell>{i18next.t("File size")}</Table.HeaderCell>
          <Table.HeaderCell>{i18next.t("Update file")}</Table.HeaderCell>
          <Table.HeaderCell>{i18next.t("Delete file")}</Table.HeaderCell>
        </Table.Row>
      </Table.Header>

      <Table.Body>
        {files?.entries?.map(({ key, size }) => (
          <Table.Row key={key}>
            <Table.Cell>{key}</Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    </Table>
  );
};
