import { test, expect } from "playwright/test";

test.use({ storageState: { cookies: [], origins: [] } });


test("falsy search", async ({ page }) => {
  await page.goto("/docs");
  expect(page.getByTestId("denied-content")).toBeVisible()
});
