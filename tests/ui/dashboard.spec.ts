import { test, expect } from "playwright/test";
import { callAPI } from "./api-call.js";

let apiContext;

test.beforeAll(async ({ playwright }) => {
  apiContext = await playwright.request.newContext({
    baseURL: "https://127.0.0.1:5000",
    extraHTTPHeaders: {
      Accept: "application/vnd.inveniordm.v1+json",
      Authorization: `token ${process.env.API_TOKEN}`,
    },
  });
});

test.afterAll(async () => {
  await apiContext.dispose();
});

test("search draft", async ({ page, baseURL, request }) => {
  await page.goto("/me/records/");
  await page.locator(`input[type='text']`).last().fill("test");
  await page.locator(`input[type='text']`).last().press("Enter");
  await expect(page).toHaveURL(
    `${baseURL}me/records/?q=test&l=list&p=1&s=10&sort=bestmatch`
  );

  const response= await callAPI(baseURL, request, false, `${baseURL}/api/user/docs/?q=test`);

  await expect(
    page.locator('[data-test-id="aggregation-count"]')
  ).toContainText(`${response.hits.total}`);
});

test("filter draft", async ({ page, baseURL, request }) => {
  await page.goto("/me/records/");
  await page.locator('[data-test-id="filter-button"]').click();

  const response= await callAPI(baseURL, request, false, `${baseURL}/api/user/docs/?q=test`);

  const resourceType = response.aggregations.metadata_resourceType;
  const firstKey = resourceType.buckets[0].key;
  const bucketCount = resourceType.buckets[0].doc_count;

  //click checkbox
  const checkbox = await page.locator(
    `.sidebar input[type="checkbox"][value="${firstKey}"]`
  );
  await checkbox.click({ force: true });

  // check if is checked
  const isChecked = await checkbox.evaluate((element) => element.checked);
  expect(isChecked).toBeTruthy();

  // check url
  await expect(page).toHaveURL(
    new RegExp(`metadata_resourceType%3A${firstKey}`)
  );

  await expect(
    page.locator('[data-test-id="aggregation-count"]')
  ).toContainText(`${bucketCount}`);

  // clear filters
  await page.locator('.tablet.row button[name="clear"]').click();
  await expect(page).toHaveURL(
    `${baseURL}me/records/?q=&l=list&p=1&s=10&sort=newest`
  );
});

test("redirection to form", async ({ page, baseURL }) => {
  await page.goto("/me/records/");
  await page.locator('#invenio-burger-toggle').click()
  const btn = await page.locator('[data-test-id="newupload-button"]');

  await btn.click({ force: true });
  await expect(page).toHaveURL(`${baseURL}docs/_new`);
});

test("pagination", async ({ page, baseURL }) => {
  await page.goto("/me/records/");
  await page.locator(".pagination a").filter({ hasText: /^5$/ }).click();
  await expect(page).toHaveURL(
    `${baseURL}me/records/?q=&l=list&p=5&s=10&sort=newest`
  );
});

test("get records", async ({ page, baseURL, request }) => {
  await page.goto("/me/records");
  await page.locator('#invenio-burger-toggle').click()
  await page.locator('[data-test-id="dashboard-redir-btn"]').click();

  await expect(page).toHaveURL(
    `${baseURL}me/records/?q=&l=list&p=1&s=10&sort=newest`
  );
  const response= await callAPI(baseURL, request, false, false);

  await expect(
    page.locator('[data-test-id="aggregation-count"]')
  ).toContainText(`${response.hits.total}`);
});
