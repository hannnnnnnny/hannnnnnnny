async page => {
  await page.waitForTimeout(1000);
  await page.getByRole('link', { name: 'Explore the finds', exact: true }).click();
  await page.waitForTimeout(2000);
  await page.getByRole('searchbox', { name: 'Search', exact: true }).fill('bike');
  await page.getByRole('button', { name: 'Search', exact: true }).click();
  await page.waitForTimeout(2500);
}
