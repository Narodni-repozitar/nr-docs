import { test as setup, expect } from "playwright/test";

const authFile = "playwright/.auth/user.json";

setup("authenticate", async ({ page, baseURL }) => {
  await page.goto(`/login`);
  await page.locator(`[name='email']`).fill("test@test.cz"); 
  await page.locator(`[name='password']`).fill("test1");
  await page.locator('.submit.button').click();

  expect(await page.waitForURL(`${baseURL}`));

  await page.context().storageState({ path: authFile });
});
