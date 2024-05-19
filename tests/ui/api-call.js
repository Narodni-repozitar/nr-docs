
import { expect } from "playwright/test";

async function callAPI(baseURL, request, oneItem, certainURL) {
    const url = certainURL || `${baseURL}api/user/docs/?q=&sort=newest&page=2&size=10`;
    const response = await request.get(url);
  
    expect(response.ok()).toBeTruthy();
  
    const responseBody = await response.body();
    const responseData = JSON.parse(responseBody.toString());
    return oneItem ? responseData.hits.hits[4] : responseData;
}

export { callAPI };