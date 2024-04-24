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

test("failed form submit", async ({ page }) => {
  try {
    await page.goto(`/docs/_new`);

    await page.locator(`[name='save']`).click();
    await page.locator(`[name='save']`).click();
    await expect(page.locator(`.negative.form-feedback`)).toBeVisible();
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
});

test("successful form submit", async ({ page }) => {
  try {
    await page.goto(`/docs/_new`);

    // title fill
    await page.locator(`[name='metadata.title']`).fill("test");

    // resource type selection
    await page.locator(`[name='metadata.resourceType']`).click();
    await page.waitForSelector('div[role="listbox"].visible.menu');

    const optionsRes = await page.$$(
      '[role="listbox"].visible.menu [role="option"]'
    );

    const randomIndexRes = Math.floor(Math.random() * optionsRes.length);
    const optionToClickRes = optionsRes[randomIndexRes];

    const optionNameRes = await optionToClickRes.getAttribute("name");
    console.log(`Clicking on option: ${optionNameRes}`);

    await page.locator(`[name="${optionNameRes}"]`).click();

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
      'button.ui.icon.left.labeled.button:has-text("Add creator")';
    await page.waitForSelector(addCreatorButtonSelector);
    await page.click(addCreatorButtonSelector);
    await page.locator(`[name='family_name']`).fill("test");
    await page.locator(`[name='given_name']`).fill("test");
    await page.locator(`[name='submit']`).last().click();

    const pagenav = page.waitForNavigation({ waitUntil: "networkidle" });
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

    await page.locator(`.ui.fluid.card .green.icon.button`).last().click();

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

    await page.waitForSelector("button.ui.primary.button:has(.upload.icon)");

    await page.locator("button.ui.primary.button:has(.upload.icon)").click();

    //   const inputField =  page.locator('input[type="file"]').nth(1);

    //   const filePath = "./ui/branding/semantic-ui/less/images/background.png";

    //   await page.setInputFiles(inputField, filePath);

    //   await page.locator("text=fixture.pdf").click();

    await page.setInputFiles(
      "#photo-upload",
      "./ui/branding/semantic-ui/less/images/background.png"
    );
    const $photoUpload = await page.$("#photo-upload");
    const $photoUploadParent = await $photoUpload.$("xpath=..");
    const $photoUploadFigure = await $photoUploadParent.$$("figure");
    expect($photoUploadFigure).toHaveLength(1);
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
});
