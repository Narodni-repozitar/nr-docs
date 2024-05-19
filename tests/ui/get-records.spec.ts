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

test("get records", async ({ page, baseURL }) => {
  await page.goto("/");
  const pagenav = page.waitForNavigation({ waitUntil: "load" });

  await page.locator(`button:has(.search.icon)`).click();
  await pagenav;
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
