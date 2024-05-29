import { test, expect } from "playwright/test";

test.use({ storageState: { cookies: [], origins: [] } });


test("falsy search", async ({ page }) => {
  await page.goto("/docs");
  const response = await page.waitForResponse((response) =>
    response.url().includes("/api/docs")
  );

  const responseData = await response.json();
  expect(responseData).toStrictEqual({
    message: "Permission denied.",
    status: 403,
  });
});
