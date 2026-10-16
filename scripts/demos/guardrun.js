async page => {
  await page.waitForTimeout(1300);
  await page.getByRole('button', {name:'Secret read', exact:true}).click();
  await page.waitForTimeout(2500);
  await page.getByRole('button', {name:'Approval gate', exact:true}).click();
  await page.waitForTimeout(2500);
  await page.getByRole('button', {name:'Normal read', exact:true}).click();
  await page.waitForTimeout(1300);
}
