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

test("successful form submit", async ({ page, baseURL, request }) => {
  try {
    await page.goto(`/communities/new`);

    const rand = Math.random().toString().substring(2, 8);
    // title fill
    await page.locator(`[name='metadata.title']`).fill(rand);

    // id fill
    await page.locator(`[name='slug']`).fill(rand);

    const pagenav = page.waitForNavigation({ waitUntil: "load" });
    await page.locator(`button.positive[type='button']`).click();

    await pagenav;

    expect(page.url().includes(`communities/${rand}/settings`)).toBeTruthy();

    await page.locator(".stackable.menu a:has(.users.icon)").click();
    await page.locator("button.negative:has(.log.out.icon)").click();

    await expect(page.locator(".modal")).toBeVisible();

    await page.locator(".modal .actions .negative.button").click();
    await expect(page.locator(".content .negative.message")).toBeVisible();

    await page.locator(".actions button:has(.cancel.icon)").click();

    await page.goto(`/communities`);
    await page
      .locator(`.page-subheader-outer input[type='text']`)
      .last()
      .fill(rand);
    await page
      .locator(`.page-subheader-outer input[type='text']`)
      .last()
      .press("Enter");

    expect(page.url().includes(`/communities/search?q=${rand}`)).toBeTruthy();

    await page.locator(".ui.basic.icon.button:has(.sliders.icon)").click();
    await expect(page.locator(".left.sidebar")).toBeVisible();

    const checkbox = await page.locator(
      '.left.sidebar input[type="checkbox"][value="public"]'
    );
    await checkbox.click({ force: true });

    // check if is checked
    const isChecked = await checkbox.evaluate((element) => element.checked);
    expect(isChecked).toBeTruthy();

    // check response length
    const url =
      "/api/communities?q=955368&sort=bestmatch&page=1&size=10&visibility=public";

    const responseData = await callAPI(baseURL, request, false, url);
    expect(responseData.hits.total).toBe(1);

    // check url
    await expect(page).toHaveURL(/visibility%3Apublic/);

    await page.locator(".tablet.community-item  a:has(.edit.icon)").click();
    expect(page.url().includes(`/communities/${rand}/settings`)).toBeTruthy();

    const response = await callAPI(baseURL, request, false, url);
    expect(response.hits.total).toBe(1);
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
});
