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

test.afterAll(async () => {
  await apiContext.dispose();
});

test("get records", async ({ page, baseURL }) => {
  await page.goto("/");
  const pagenav = page.waitForNavigation({ waitUntil: "load" });

  const form = await page.locator('.ui.form[role="search"]');
  await form.locator('button[type="submit"]').click();

  await pagenav;
  await expect(page).toHaveURL(
    `${baseURL}docs/?q=&l=list&p=1&s=10&sort=newest`
  );

  await expect(page.getByTestId("aggregation-count")).toContainText("20");

  await expect(page.getByTestId("result-item")).toHaveCount(10);

  const resPerPage = page.locator('.computer div[role="listbox"]');

  await resPerPage.click();

  await resPerPage.locator("span", { hasText: "50" }).click();

  await expect(page.getByTestId("result-item")).toHaveCount(20);

  await page.locator("#invenio-burger-menu-icon").click();
  await page.getByTestId("searchbar").locator("input").locator("visible=true").fill("test");
  await page.getByTestId("searchbar").locator("input").locator("visible=true").press("Enter");

  await expect(page).toHaveURL(
    `${baseURL}docs/?q=test&l=list&p=1&s=10&sort=bestmatch`
  );

  await expect(page.getByTestId("aggregation-count")).toContainText("0");
});
