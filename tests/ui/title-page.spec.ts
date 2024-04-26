import { test, expect } from "playwright/test";

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

test("search and check URL", async ({ page, baseURL }) => {
  await page.goto("/");
  await page.locator(`input[name='q']`).fill("test");
  await page.locator(`input[name='q']`).press("Enter");
  await expect(page).toHaveURL(
    `${baseURL}docs/?q=test&l=list&p=1&s=10&sort=bestmatch`
  );
});

test("redirection to title page", async ({ page, baseURL }) => {
  await page.goto("/docs/_new");
  await page.locator(".logo-link").click();
  await expect(page).toHaveURL(`${baseURL}`);
});

test("sign out", async ({ page, baseURL }) => {
  await page.goto("/");
  await page.locator('#invenio-burger-menu-icon').click();
  await page.locator(".tablet .item:has(.sign-out.icon)").click();
  await expect(page).toHaveURL(`${baseURL}`);
});
