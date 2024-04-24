import { expect } from "playwright/test";

module.exports = async function callAPI( baseURL, request, oneItem=true, certainURL ) {
  const response = await request.get(
    certainURL?  certainURL : `${baseURL}api/user/docs/?q=&sort=newest&page=2&size=10`
  );
  
  expect(response.ok()).toBeTruthy();

  const responseBody = await response.body();
  const responseData = JSON.parse(responseBody.toString());
  return oneItem? responseData.hits.hits[4] : responseData;
};
