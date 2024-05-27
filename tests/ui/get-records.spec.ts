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

test("get records", async ({ page, baseURL, request }) => {
  await page.goto("/");
  const pagenav = page.waitForNavigation({ waitUntil: "load" });

  const form = await page.locator('.ui.form[role="search"]');
  await form.locator('button[type="submit"]').click();

  await pagenav;
  await expect(page).toHaveURL(
    `${baseURL}docs/?q=&l=list&p=1&s=10&sort=newest`
  );

  const response= await callAPI(baseURL, request, false, false);

  await expect(
    page.locator('[data-test-id="aggregation-count"]')
  ).toContainText(`${response.hits.total}`);
});

