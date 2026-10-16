async page => {
  await page.waitForTimeout(1000);
  await page.getByRole('link', { name: 'Matte Black Road Bike Matte Black Road Bike $650.00 $1,600.00 Good Hamilton', exact:true }).click();
  await page.getByRole('heading', { name:'Matte Black Road Bike', exact:true }).waitFor();
  await page.waitForTimeout(2300);
  await page.mouse.wheel(0, 300);
  await page.waitForTimeout(1700);
}
