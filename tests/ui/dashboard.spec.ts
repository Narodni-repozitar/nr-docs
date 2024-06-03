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

test("search draft", async ({ page, baseURL }) => {
  await page.goto("/me/records/");
  await page.locator(`input[type='text']`).last().fill("test");
  await page.locator(`input[type='text']`).last().press("Enter");
  await expect(page).toHaveURL(
    `${baseURL}me/records/?q=test&l=list&p=1&s=10&sort=bestmatch`
  );

  await expect(page.getByTestId("aggregation-count")).toContainText("0");
});

test("filter draft", async ({ page, baseURL }) => {
  await page.goto("/me/records/");
  // await page.getByTestId("filter-button").click();
  await page.locator(".button:has(.sliders)").click();

  await expect(page.locator(".sidebar .facet-list")).toBeVisible();
  // get all aggregation buckets
  const numberOfAggs = await page
    .locator(".sidebar .ui.facet")
    .locator("visible=true")
    .count();

  const randomAggIndex = Math.floor(Math.random() * numberOfAggs);

  const selectedAgg = page
    .locator(".ui.facet")
    .locator("visible=true")
    .nth(randomAggIndex);

  // get all checkboxes in certain bucket
  const numberOfCheckboxes = await selectedAgg
    .locator(".list .item .checkbox")
    .locator("visible=true")
    .count();

  const randomCheckboxIndex = Math.floor(Math.random() * numberOfCheckboxes);

  const selectedCheckbox = selectedAgg
    .locator(".list .item .checkbox input")
    .nth(randomCheckboxIndex);

  const selectedBucketCount = await selectedAgg
    .locator(".list .item .facet-count")
    .filter({ has: page.locator("visible=true") })
    .nth(randomCheckboxIndex)
    .textContent()
    .then((text) => {
      if (!text) throw new Error("Count content is empty");
      const index = text.indexOf(" ");
      return text.substring(0, index);
    });

  //click the checkbox
  await selectedCheckbox.click({ force: true });

  const isChecked = await selectedCheckbox.evaluate(
    (element) => element.checked
  );
  expect(isChecked).toBeTruthy();

  await expect(page.getByTestId("aggregation-count")).toContainText(
    `${selectedBucketCount}`
  );
  // clear filters
  await page.locator('.tablet.row button[name="clear"]').click();
  await expect(page).toHaveURL(
    `${baseURL}me/records/?q=&l=list&p=1&s=10&sort=newest`
  );
});

test("redirection to form", async ({ page, baseURL }) => {
  await page.goto("/me/records/");
  await page.locator("#invenio-burger-toggle").click();
  const btn = await page.getByTestId("newupload-button");

  await btn.click({ force: true });
  await expect(page).toHaveURL(`${baseURL}docs/_new`);
});

test("pagination", async ({ page, baseURL }) => {
  await page.goto("/me/records/");
  await page.locator(".pagination a").filter({ hasText: /^5$/ }).click();
  await expect(page).toHaveURL(
    `${baseURL}me/records/?q=&l=list&p=5&s=10&sort=newest`
  );
});

test("get records", async ({ page, baseURL }) => {
  await page.goto("/me/records");
  await page.locator("#invenio-burger-toggle").click();
  await page.getByTestId("dashboard-redir-btn").click();

  await expect(page).toHaveURL(
    `${baseURL}me/records/?q=&l=list&p=1&s=10&sort=newest`
  );

  await expect(page.getByTestId("aggregation-count")).toContainText("20");

  await expect(page.getByTestId("result-item")).toHaveCount(10);

  const perpageComponent = page
    .getByTestId("pages-component")
    .locator("visible=true");

  const resPerPage = perpageComponent.locator(".ui.dropdown");
  await expect(resPerPage).toBeVisible();
  await expect(resPerPage).toBeEnabled();

  await resPerPage.click();

  await resPerPage.locator(".menu span", { hasText: "50" }).click();

  await expect(page.getByTestId("result-item")).toHaveCount(20);
});
