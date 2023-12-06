import React from "react";
import PropTypes from "prop-types";
import { Table } from "semantic-ui-react";
import { dummyFiles } from "./dummyfiles";
import { i18next } from "@translations/docs_app/i18next";
import { humanReadableBytes } from "./humanReadableBytes";
import { EditFileButton, DeleteFileButton } from "./FileUploaderButtons";
import _truncate from "lodash/truncate";

export const FileUploaderTable = ({
  files = dummyFiles,
  record,
  handleFileDeletion,
}) => {
  return (
    files?.length > 0 && (
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
          {files?.map((file) => {
            const { key: fileName, size, file_id: fileId } = file;
            return (
              <Table.Row key={fileId}>
                <Table.Cell>
                  <a href={file?.links?.content}>
                    {fileName &&
                      _truncate(fileName, { length: 40, omission: "..." })}
                  </a>
                </Table.Cell>
                <Table.Cell>{humanReadableBytes(size)}</Table.Cell>
                <Table.Cell>
                  <EditFileButton fileName={fileName} record={record} />
                </Table.Cell>
                <Table.Cell>
                  <DeleteFileButton
                    file={file}
                    handleFileDeletion={handleFileDeletion}
                  />
                </Table.Cell>
              </Table.Row>
            );
          })}
        </Table.Body>
      </Table>
    )
  );
};

FileUploaderTable.propTypes = {
  files: PropTypes.array,
  record: PropTypes.object,
  handleFileDeletion: PropTypes.func,
};
