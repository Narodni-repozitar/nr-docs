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

test("successful form submit", async ({ page }) => {
  try {
    await page.goto(`/docs/_new`);
    // title fill
    await page.locator(`[name='metadata.title']`).fill("test");

    // resource type selection
    await page.locator(`[name='metadata.resourceType']`).click();
    await page.waitForSelector(".tree-field", { state: "visible" });

    const numberOfOptions = await page
      .locator(".tree-column .row")
      .locator("visible=true")
      .count();

    const randomIndex = Math.floor(Math.random() * numberOfOptions);

    await page
      .locator(".tree-column .row")
      .locator("visible=true")
      .nth(randomIndex)
      .click();

    // select language

    await page.locator(`[name='metadata.languages']`).click();
    await page.waitForSelector('.visible.menu[role="listbox"]', {
      state: "visible",
    });

    const optionsLang = await page.$$(
      '.visible.menu[role="listbox"] [role="option"]'
    );

    const randomIndexLang = Math.floor(Math.random() * optionsLang.length);
    const optionToClickLang = optionsLang[randomIndexLang];

    const optionNameLang = await optionToClickLang.getAttribute("name");

    await page.locator(`[name="${optionNameLang}"]`).click();

    // select access rights

    await page.locator(`[name='metadata.accessRights']`).click();
    await page.waitForSelector('.visible.menu[role="listbox"]', {
      state: "visible",
    });

    const optionsRights = await page.$$(
      '.visible.menu[role="listbox"] [role="option"]'
    );

    const randomIndexRights = Math.floor(Math.random() * optionsRights.length);

    const optionToClickRights = optionsRights[randomIndexRights];

    const optionNameRights = await optionToClickRights.getAttribute("name");

    await page.locator(`[name="${optionNameRights}"]`).click();

    // creator input
    const addCreatorButtonSelector =
      '.field:has(label[for="metadata.creators"]) button';
    await page.waitForSelector(addCreatorButtonSelector, { state: "visible" });
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

    await page.getByTestId("validate-button").click();

    await page.waitForSelector(`.label[role='alert']`, { state: "visible" });

    const alertLabels = await page.$$('.label[role="alert"]');

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

    const parentLocator = page.getByTestId("filesupload-button");

    const buttonNotInTable = parentLocator.locator(
      "button:not(.ui.table button)"
    );

    if ((await buttonNotInTable.count()) > 0) {
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

test("tree-field manipulation and selected result check", async ({ page }) => {
  await page.goto("/docs/_new");

  const singleTreeField = page.locator(`[name='metadata.resourceType']`);
  singleTreeField.click();

  await page.waitForSelector(".tree-field", { state: "visible" });

  const numberOfOptionsSingle = await page
    .locator(".tree-column .row:visible")
    .count();

  const randomIndexSingle = Math.floor(Math.random() * numberOfOptionsSingle);

  const selectedOption = page
    .locator(".tree-column .row:visible")
    .nth(randomIndexSingle);

  await selectedOption.click();

  const selectedOptionText = await selectedOption.innerText();

  await expect(
    singleTreeField
      .locator(".text span")
      .filter({ hasText: selectedOptionText })
  ).toHaveCount(1);

  // multiple
  const multipleTreeField = page.locator(`[name='metadata.subjectCategories']`);
  await multipleTreeField.click();
  await page.waitForSelector(".tree-field", { state: "visible" });

  const numberOfOptionsMultiple = await page
    .locator(".tree-column .row")
    .locator("visible=true")
    .count();
  const randomIndexMultiple = Math.floor(
    Math.random() * numberOfOptionsMultiple
  );

  await page
    .locator(".tree-column .row.spaced")
    .nth(randomIndexMultiple)
    .locator(".checkbox")
    .click();

  const checkedButtonText = await page
    .locator(".tree-column .row.spaced")
    .nth(randomIndexMultiple)
    .innerText();

  const labelLocator = page.locator(".actions .row .ui.label").last();
  await labelLocator.waitFor({ state: "visible" });

  const lastLabelBreadcrumbText = await labelLocator
    .locator(".ui.breadcrumb")
    .innerText();

  expect(lastLabelBreadcrumbText).toContain(checkedButtonText);

  const multipleTreeFieldSubmitButton = page.locator(
    ".actions button:not(.ui.label button)"
  );
  await multipleTreeFieldSubmitButton.click();

  await expect(page.locator(".tree-field")).toBeHidden();
  await expect(
    page.locator("a").filter({ hasText: checkedButtonText })
  ).toHaveCount(1);
});
