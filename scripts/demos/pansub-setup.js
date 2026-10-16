async page => {
  await page.addInitScript(() => {
    const store = {pansubEnabled:true, pansubSettings:{interfaceLanguage:'en'}, pansubCache:{}};
    window.chrome = {storage:{local:{
      get(keys, callback) { const result={}; for(const key of (Array.isArray(keys)?keys:[keys])) result[key]=store[key]; callback(result); },
      set(values, callback) { Object.assign(store, values); callback?.(); },
      remove(keys, callback) { for(const key of (Array.isArray(keys)?keys:[keys])) delete store[key]; callback?.(); }
    },onChanged:{addListener(){}}},runtime:{lastError:null,openOptionsPage(callback){callback?.();},sendMessage(){}}};
  });
  await page.goto('http://127.0.0.1:64363/output/playwright/sources/pansub/options.html');
  await page.waitForSelector('body:not(.is-loading)');
  await page.locator('a[href="#subtitles"]').click();
  await page.waitForTimeout(1500);
}
