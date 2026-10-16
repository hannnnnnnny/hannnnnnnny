async page => {
  await page.waitForTimeout(1200);
  await page.getByRole('link', { name: 'This weekend', exact: true }).click();
  await page.waitForTimeout(2200);
  await page.getByRole('link', { name: 'Markets', exact: true }).click();
  await page.waitForTimeout(2200);
  await page.getByRole('button', { name: 'Ask KiwiCue', exact: true }).click();
  await page.waitForTimeout(2200);
}
