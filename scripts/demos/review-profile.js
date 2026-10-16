async page => {
  await page.setViewportSize({width:1000,height:1100});
  await page.locator('article img').last().waitFor();
  await page.waitForFunction(() => Array.from(document.querySelectorAll('article img')).every(img => img.complete && img.naturalWidth > 0));
  await page.screenshot({path:'output/playwright/profile-desktop.png'});
  await page.setViewportSize({width:375,height:812});
  const layout = await page.evaluate(() => ({width:innerWidth,content:document.documentElement.scrollWidth,images:document.images.length}));
  if(layout.content > layout.width || layout.images !== 6) throw new Error(JSON.stringify(layout));
  await page.screenshot({path:'output/playwright/profile-mobile.png'});
  await page.setViewportSize({width:1000,height:1100});
}
