import React from "react";
import PropTypes from "prop-types";
import { Table } from "semantic-ui-react";
import { dummyFiles } from "./dummyfiles";
import { i18next } from "@translations/docs_app/i18next";
import { humanReadableBytes } from "./humanReadableBytes";
import { EditFileButton, DeleteFileButton } from "./FileUploaderButtons";

export const FileUploaderTable = ({
  files = dummyFiles,
  removeFile,
  record,
}) => {
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
        {files?.entries?.map((file) => {
          const { key, size } = file;
          return (
            <Table.Row key={key}>
              <Table.Cell>{key}</Table.Cell>
              <Table.Cell>{humanReadableBytes(size)}</Table.Cell>
              <Table.Cell>
                <EditFileButton key={key} record={record} />
              </Table.Cell>
              <Table.Cell>
                <DeleteFileButton file={file} />
              </Table.Cell>
            </Table.Row>
          );
        })}
      </Table.Body>
    </Table>
  );
};
