import React from "react";
import PropTypes from "prop-types";
import { Table, Popup } from "semantic-ui-react";
import { i18next } from "@translations/i18next";
import { humanReadableBytes } from "react-invenio-forms";
import { EditFileButton, DeleteFileButton } from "./FileUploaderButtons";
import _truncate from "lodash/truncate";

export const FileUploaderTable = ({ files, record, handleFileDeletion }) => {
  return (
    files?.length > 0 && (
      <Table compact>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell>{i18next.t("File name")}</Table.HeaderCell>
            <Table.HeaderCell textAlign="center">
              {i18next.t("File size")}
            </Table.HeaderCell>
            <Table.HeaderCell></Table.HeaderCell>
            <Table.HeaderCell></Table.HeaderCell>
          </Table.Row>
        </Table.Header>

        <Table.Body>
          {files?.map((file) => {
            const { key: fileName, size, file_id: fileId } = file;
            return (
              <Table.Row key={fileId}>
                <Table.Cell width={7}>
                  <a
                    href={file?.links?.content}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {fileName &&
                      _truncate(fileName, { length: 40, omission: "..." })}
                  </a>
                </Table.Cell>
                <Table.Cell textAlign="center">
                  {humanReadableBytes(size)}
                </Table.Cell>
                <Table.Cell width={1} textAlign="center">
                  <Popup
                    content={i18next.t("Edit file metadata")}
                    trigger={
                      <div>
                        <EditFileButton fileName={fileName} record={record} />
                      </div>
                    }
                  />
                </Table.Cell>
                <Table.Cell width={1} textAlign="center">
                  <Popup
                    content={i18next.t("Delete file")}
                    trigger={
                      <div>
                        <DeleteFileButton
                          file={file}
                          handleFileDeletion={handleFileDeletion}
                        />
                      </div>
                    }
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
