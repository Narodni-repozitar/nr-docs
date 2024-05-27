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

test("search published", async ({ page, baseURL, request }) => {
  await page.goto("/docs");
  await page.locator("#invenio-burger-menu-icon").click();
  await page.locator(`.menu input[type='text']`).last().fill("test");
  await page.locator(`.menu input[type='text']`).last().press("Enter");
  await expect(page).toHaveURL(
    `${baseURL}docs/?q=test&l=list&p=1&s=10&sort=bestmatch`
  );

  const response= await callAPI(false, request, false, `${baseURL}api/docs/?q=test&page=1&size=10`);

  await expect(
    page.locator('[data-test-id="aggregation-count"]')
  ).toContainText(`${response.hits.total}`);
});

