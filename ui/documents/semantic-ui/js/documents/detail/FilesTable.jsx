import React, { useState } from "react";
import {
  Icon,
  Button,
  TableRow,
  TableHeaderCell,
  TableHeader,
  TableCell,
  TableBody,
  Table,
} from "semantic-ui-react";
import { getCaption } from "./index";
import { i18next } from "@translations/i18next";
import { FilePreviewerComponent } from "./FilesPreviewer";

export const FilesSection = ({ filesCollection }) => {
  const [openPreview, setOpenPreview] = useState(false);

  const showPreview = () => {
    setOpenPreview(!openPreview);
  };

  const getFileSize = (bytes, decimals = 2) => {
    if (!+bytes) return "0 Bytes";

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = [
      "Bytes",
      "KiB",
      "MiB",
      "GiB",
      "TiB",
      "PiB",
      "EiB",
      "ZiB",
      "YiB",
    ];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
  };

  const formatDate = (date) => {
    const options = { year: "numeric", month: "long", day: "numeric" };
    return new Date(date).toLocaleDateString(undefined, options);
  };

  return (
    <>
      <Table celled>
        <TableHeader>
          <TableRow>
            <TableHeaderCell>{i18next.t("Name")}</TableHeaderCell>
            <TableHeaderCell>{i18next.t("Size")}</TableHeaderCell>
            <TableHeaderCell>{i18next.t("Date")}</TableHeaderCell>
            <TableHeaderCell>{i18next.t("Download")}</TableHeaderCell>
            <TableHeaderCell>{i18next.t("Preview")}</TableHeaderCell>
          </TableRow>
        </TableHeader>

        <TableBody>
          {filesCollection?.map((file) => (
            <TableRow key={file.file_id}>
              <TableCell> {getCaption(file)}</TableCell>
              <TableCell> {getFileSize(file.size)}</TableCell>
              <TableCell> {formatDate(file.created)}</TableCell>
              <TableCell>
                {" "}
                <a href={file.links.content}>
                  <Icon name="download" />
                </a>
              </TableCell>
              <TableCell>
                {" "}
                <Button color="transparent" onClick={showPreview}>
                  <Icon name="search" />
                </Button>
              </TableCell>
              {openPreview && <FilePreviewerComponent link={[file.links.content]} />}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </>
  );
};
