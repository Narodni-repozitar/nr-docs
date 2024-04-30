import React, { useState, useEffect } from "react";
import { Modal } from "semantic-ui-react";

export const FilePreviewerComponent1 =  ({ link }) => {
  const [modalOpen, setModalOpen] = useState(link && true);

  const handleCloseModal = () => {
    setModalOpen(false);
  };

  const getfile = async () => {
    await Promise.all(
      link?.map(async (l) => {
        const response = await fetch(l);
        const blob = await response.blob();
        return (fileLink = URL.createObjectURL(blob));
      })
    );
  };

  let fileLink =  getfile();

  useEffect(()=>{
    console.log(fileLink)
  }, [fileLink])

  return (
    <Modal open={modalOpen} onClose={handleCloseModal} size="large" closeIcon>
      <Modal.Content>
        <iframe src={fileLink} style={{ width: "100%", height: "80vh" }} />
      </Modal.Content>
    </Modal>
  );
};

export const FilePreviewerComponent = ({ link }) => {
  const [modalOpen, setModalOpen] = useState(false);
  const [fileLink, setFileLink] = useState("");

  useEffect(() => {
    if (link) {
      setModalOpen(true);
      getFile();
    }
  }, [link]);

  const handleCloseModal = () => {
    setModalOpen(false);
  };

  const getFile = async () => {
    const response = await fetch(link);
    // const blob = await response.blob();
    const blob = new Blob([response], {type: 'application/pdf'})
    const url = URL.createObjectURL(blob);
    setFileLink(url);
  };

  return (
    <Modal open={modalOpen} onClose={handleCloseModal} size="large" closeIcon>
      <Modal.Content>
        <iframe
          src={fileLink}
          style={{ width: "100%", height: "80vh", marginBottom: "10px" }}
        />
      </Modal.Content>
    </Modal>
  );
};