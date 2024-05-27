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

test("successful form submit", async ({ baseURL, page, request }) => {
  try {
    await page.goto(`/docs/_new`);

    // title fill
    await page.locator(`[name='metadata.title']`).fill("test");

    // resource type selection
    await page.locator(`[name='metadata.resourceType']`).click();
    await page.waitForSelector('.tree-field');

    const response= await callAPI(baseURL, request, false, false);
  
    const resourceType = response.aggregations.metadata_resourceType;
    const firstLabel = resourceType.buckets[0].label;

    await page.locator(`button:has-text("${firstLabel}")`).click();

    await page.locator('.modal .actions .button').click()

    // select language

    await page.locator(`[name='metadata.languages']`).click();
    await page.waitForSelector('div[role="listbox"].visible.menu');

    const optionsLang = await page.$$(
      '[role="listbox"].visible.menu [role="option"]'
    );

    const randomIndexLang = Math.floor(Math.random() * optionsLang.length);
    const optionToClickLang = optionsLang[randomIndexLang];

    const optionNameLang = await optionToClickLang.getAttribute("name");

    await page.locator(`[name="${optionNameLang}"]`).click();

    // select access rights

    await page.locator(`[name='metadata.accessRights']`).click();
    await page.waitForSelector('div[role="listbox"].visible.menu');

    const optionsRights = await page.$$(
      '[role="listbox"].visible.menu [role="option"]'
    );

    const randomIndexRights = Math.floor(Math.random() * optionsRights.length);
    const optionToClickRights = optionsRights[randomIndexRights];

    const optionNameRights = await optionToClickRights.getAttribute("name");

    await page.locator(`[name="${optionNameRights}"]`).click();

    // creator input
    const addCreatorButtonSelector =
      '.field:has(label[for="metadata.creators"]) button';
    await page.waitForSelector(addCreatorButtonSelector);
    await page.click(addCreatorButtonSelector);
    await page.locator(`[name='family_name']`).fill("test");
    await page.locator(`[name='given_name']`).fill("test");
    await page.locator(`[name='submit']`).last().click();

    const pagenav = page.waitForNavigation({ waitUntil: "load" });
    await page.locator(`[name='save']`).click();

    await pagenav;

    expect(page.url().includes("edit")).toBeTruthy();
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
});

test("form validation", async ({ page }) => {
  try {
    await page.goto(`/docs/_new`);

    await page.locator('[data-test-id="validate-button"]').click();

    await page.waitForSelector(`.label[role='alert']`);

    const alertLabels = await page.$$('div.label[role="alert"]');

    expect(alertLabels.length).toBe(5);
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
});

test("file upload", async ({ page }) => {
  try {
    await page.goto(`/docs/_new`);

    await page.locator(`[name='save']`).click();
    await page.locator(`[name='save']`).click();

    const parentLocator = await page.locator(
      '[data-test-id="filesupload-button"]'
    );

    const buttonNotInTable = await parentLocator.locator('button:not(.ui.table button)');

    if (await buttonNotInTable.count() > 0) {
      await buttonNotInTable.click();
    } 

    await expect(page.locator(".uppy-Dashboard-inner")).toBeVisible();

    const filePath = "../../ui/branding/semantic-ui/less/images/background.png";

    const handle = await page.$('input[type="file"]');
    await handle.setInputFiles(filePath);

    await page.locator(".uppy-StatusBar-actionBtn--upload").click();
    await page.locator(".uppy-StatusBar-actionBtn--done").click();
    await page.locator(`[name='save']`).click();

    await expect(page.locator(".ui.form-feedback")).toBeVisible();
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
});
