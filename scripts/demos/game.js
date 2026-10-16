async page => {
  await page.waitForTimeout(3500);
  await page.getByRole('button', {name:'Build menus', exact:true}).click();
  await page.waitForTimeout(4000);
  await page.getByRole('button', {name:'Gameplay', exact:true}).click();
  await page.waitForTimeout(2000);
}
