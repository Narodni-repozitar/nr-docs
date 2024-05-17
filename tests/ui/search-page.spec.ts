import { test, expect } from "playwright/test";
const callAPI = require("./api-call.spec.ts");

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

test("search published", async ({ page, baseURL }) => {
  await page.goto("/docs");
  await page.locator("#invenio-burger-menu-icon").click();
  await page.locator(`.menu input[type='text']`).last().fill("test");
  await page.locator(`.menu input[type='text']`).last().press("Enter");
  await expect(page).toHaveURL(
    `${baseURL}docs/?q=test&l=list&p=1&s=10&sort=bestmatch`
  );

  const response = await page.evaluate(() =>
    fetch(`https://127.0.0.1:5000/api/docs/?q=test&page=1&size=10`).then(
      (res) => res.json()
    )
  );
  expect(response.hits.total).toBe(1);
});

test("filter published", async ({ page, baseURL, request }) => {
  await page.goto("/docs");
  await page.locator(".ui.basic.icon.button:has(.sliders.icon)").click();

  await expect(page.locator("aside .sidebar")).toBeVisible();

  const response = await page.evaluate(() => {
    return fetch(
      `https://127.0.0.1:5000/api/docs/?q=&page=1&size=10`
    ).then((response) => response.json());
  });

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

  // check response length
  const url = `/api/docs/?q=&page=1&size=10&metadata_resourceType=${firstKey}`;

  const responseData = await callAPI(baseURL, request, false, url);
  expect(responseData.hits.total).toBe(bucketCount);

  // check url
  await expect(page).toHaveURL(
    new RegExp(`metadata_resourceType%3A${firstKey}`)
  );

  await page.locator(".sidebar .header .mini.basic.button").click();
  await expect(page).toHaveURL(`${baseURL}`);
});

test("get records", async ({ page, baseURL }) => {
  await page.goto("/");

  await page.locator(`button:has(.search.icon)`).click();

  await expect(page).toHaveURL(
    `${baseURL}docs/?q=&l=list&p=1&s=10&sort=newest`
  );

  const response = await page.evaluate(() =>
    fetch(`https://127.0.0.1:5000/api/docs/?q=test&page=1&size=10`).then(
      (res) => res.json()
    )
  );
  expect(response.hits.total).toBe(1); // put here required testing amount
});
