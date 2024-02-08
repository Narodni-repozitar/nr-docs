import React from "react";
import { i18next } from "@translations/i18next";
import { http } from "react-invenio-forms";
import { useQuery } from "@tanstack/react-query";

export const UserDashboardComputerNav = () => {
  const {
    isLoading: isLoadingRecords,
    isError: isRecordsError,
    data: records,
    error: errorRecords,
  } = useQuery({
    queryKey: ["records"],
    queryFn: () => http.get("/api/docs").then((res) => res.data.hits),
  });
  const {
    isLoading: isLoadingCommunities,
    isError: isCommunitiesError,
    data: communities,
    error: errorCommunities,
  } = useQuery({
    queryKey: ["communities"],
    queryFn: () =>
      http.get("/api/user/communities").then((res) => res.data.hits),
  });
  const {
    isLoading: isLoadingRequests,
    isError: isRequestsError,
    data: requests,
    error: errorRequests,
  } = useQuery({
    queryKey: ["requests"],
    queryFn: () => http.get("/api/requests").then((res) => res.data.hits),
  });
  console.log(records);
  return (
    <React.Fragment>
      <div>
        {records?.hits?.map((record) => (
          <div>{record.metadata.title}</div>
        ))}
      </div>
    </React.Fragment>
  );
};
