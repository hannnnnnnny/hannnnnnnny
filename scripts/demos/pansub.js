async page => {
  await page.waitForTimeout(1000);
  await page.locator('#overlayTheme').click();
  await page.locator('#overlayTheme').selectOption('glass');
  await page.waitForTimeout(1500);
  await page.locator('#displayMode').click();
  await page.locator('#displayMode').selectOption('translation');
  await page.waitForTimeout(1500);
  await page.locator('#displayMode').click();
  await page.locator('#displayMode').selectOption('bilingual');
  await page.locator('#overlayTheme').click();
  await page.locator('#overlayTheme').selectOption('light');
  await page.waitForTimeout(1500);
  await page.locator('#overlayTheme').click();
  await page.locator('#overlayTheme').selectOption('classic');
  await page.waitForTimeout(1500);
}
