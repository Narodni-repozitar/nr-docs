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

test.afterAll(async ({}) => {
  await apiContext.dispose();
});

test("search draft", async ({ page, baseURL }) => {
  await page.goto("/me/records/");
  await page.locator(`input[type='text']`).last().fill("test");
  await page.locator(`input[type='text']`).last().press("Enter");
  await expect(page).toHaveURL(
    `${baseURL}me/records/?q=test&l=list&p=1&s=10&sort=bestmatch`
  );

  const response = await page.evaluate(() =>
    fetch(
      `https://127.0.0.1:5000/api/user/docs/?q=test&sort=bestmatch&page=1&size=10`
    ).then((res) => res.json())
  );
  expect(response.hits.total).toBe(46);
});

test("filter draft", async ({ page, baseURL, request }) => {
  await page.goto("/me/records/");
  await page.locator(".ui.basic.icon.button:has(.sliders.icon)").click();

  //click checkbox
  const checkbox = await page.locator(
    '.sidebar input[type="checkbox"][value="article"]'
  );
  await checkbox.click({ force: true });

  // check if is checked
  const isChecked = await checkbox.evaluate((element) => element.checked);
  expect(isChecked).toBeTruthy();

  // check response length
  const url = "/api/user/docs/?q=&page=1&size=10&metadata_resourceType=article";

  const responseData = await callAPI(baseURL, request, false, url);
  expect(responseData.hits.total).toBe(4);

  // check url
  await expect(page).toHaveURL(/metadata_resourceType%3Aarticle/);

  // clear filters
  await page.locator('.tablet.row button[name="clear"]').click();
  await expect(page).toHaveURL(
    `${baseURL}me/records/?q=&l=list&p=1&s=10&sort=newest`
  );
});

test("redirection to form", async ({ page, baseURL }) => {
  await page.goto("/me/records/");
  const btn = await page.locator(
    ".tablet.row .ui.icon.primary.button:has(.plus.icon)"
  );

  await btn.click({ force: true });
  await expect(page).toHaveURL(`${baseURL}docs/_new`);
});

test("pagination", async ({ page, baseURL }) => {
  await page.goto("/me/records/");
  await page.locator("a").filter({ hasText: "5" }).click();
  await expect(page).toHaveURL(
    `${baseURL}me/records/?q=&l=list&p=5&s=10&sort=newest`
  );
});
