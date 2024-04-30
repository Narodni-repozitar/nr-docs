import React from "react";
import ReactDOM from "react-dom";
import { FilesSection } from "./FilesTable";

const filesTableComp = document.getElementById("files-table");

let filesCollection = [];
let data;

const fetchFiles = async () => {
  try {
    const apiUrl = filesTableComp.dataset.files.replace(/"/g, "");
    const response = await fetch(apiUrl);

    data = await response.json();

    await Promise.all(
      data?.entries?.map(async (item) => {
        if (item?.metadata?.fileType) {
          filesCollection.push(item);
        }
        return null;
      })
    );
  } catch (error) {
    console.error("Error fetching files");
  }
};

export const getCaption = (d) => {
  if (d?.metadata && d?.metadata?.caption) {
    if (
      d.metadata.caption === "default_image_name" ||
      d.metadata.caption === "default_pdf_name"
    ) {
      return d?.key;
    } else {
      return d.metadata.caption;
    }
  } else {
    return d?.key;
  }
};

async function fetchAndRender() {
  try {
    await fetchFiles();
    ReactDOM.render(
      <FilesSection filesCollection={filesCollection} />,
      filesTableComp
    );
  } catch (error) {
    console.error("Error rendering component");
  }
}

fetchAndRender();
