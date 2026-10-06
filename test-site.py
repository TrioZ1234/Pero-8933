import asyncio, json
from pathlib import Path
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        page = await browser.new_page(viewport={ 'width': 1440, 'height': 1000 }, reduced_motion='reduce')
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        await page.goto('http://localhost:4200', wait_until='networkidle')
        await page.screenshot(path='/home/user/pero-desktop-final.png')
        assert await page.get_by_role('link', name='Вернуться наверх страницы', exact=True).is_visible()
        assert await page.title() == 'Перо Измерений: Вельд’Эран | TrioZ Entertainment'
        await page.locator('#world').scroll_into_view_if_needed()
        await page.locator('.world-map').click()
        assert await page.locator('.image-dialog').is_visible()
        await page.keyboard.press('Escape')
        assert await page.locator('.image-dialog').count() == 0
        await page.get_by_role('tab', name='Суббгары').click()
        assert 'Гиганты фьордов' in await page.locator('#faction-panel').inner_text()
        await page.locator('#factions').screenshot(path='/home/user/pero-factions.png')
        card = page.get_by_role('button', name='Перевернуть боевую карту 3', exact=True)
        await card.click()
        assert await card.get_attribute('aria-pressed') == 'true'
        await card.click()
        assert await card.get_attribute('aria-pressed') == 'false'
        await page.locator('#battle').screenshot(path='/home/user/pero-battle.png')
        await page.locator('.god-row').first.locator('summary').click()
        assert await page.locator('.god-row').first.get_attribute('open') is not None
        await page.locator('.rules-accordion > summary').click()
        assert await page.locator('.rules-scans').is_visible()
        await page.locator('.rules-scans button').first.click()
        assert await page.locator('.image-dialog').is_visible()
        await page.keyboard.press('Escape')
        await page.locator('#order').scroll_into_view_if_needed()
        await page.get_by_role('button', name='Подробнее', exact=True).click()
        assert await page.locator('.privacy-dialog').is_visible()
        await page.keyboard.press('Escape')
        assert not await page.locator('.privacy-dialog').is_visible()
        await page.locator('input[name=name]').fill('Тестовый посетитель')
        await page.locator('input[name=email]').fill('test@example.com')
        await page.locator('textarea[name=message]').fill('Проверка формы без отправки email')
        options = await page.locator('select[name=quantity] option').all_text_contents()
        assert len(options) == 6 and 'Оптом' in options[-1]
        await page.locator('select[name=quantity]').select_option('5')
        await page.locator('select[name=quantity]').select_option('wholesale')
        assert await page.locator('.wholesale-hint').is_visible()
        await page.locator('input[name=consent]').check()
        assert await page.get_by_role('button', name='Подготовить письмо').is_visible(), 'Automatic email unexpectedly configured; do not submit test email'
        await page.get_by_role('button', name='Подготовить письмо').click()
        await page.get_by_text('Письмо подготовлено, но ещё не отправлено', exact=True).wait_for()
        href = await page.get_by_role('link', name='Открыть письмо ещё раз').get_attribute('href')
        assert href.startswith('mailto:sales@trioz.ru?')
        from urllib.parse import unquote
        assert 'Оптом — 6 и более экземпляров' in unquote(href)
        await page.locator('#order').screenshot(path='/home/user/pero-order.png')
        for section in ['#world', '#factions', '#battle', '#armies', '#gods', '#play', '#rules', '#order', '#ecosystem']:
            await page.locator(section).scroll_into_view_if_needed()
        await page.wait_for_load_state('networkidle')
        broken = await page.evaluate('Array.from(document.images).filter(x => x.complete && !x.naturalWidth).map(x => x.src)')
        assert not broken, broken
        assert not errors, errors
        assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        mobile = await browser.new_page(viewport={'width': 390, 'height': 844}, is_mobile=True, device_scale_factor=1, reduced_motion='reduce')
        await mobile.goto('http://localhost:4200', wait_until='networkidle')
        await mobile.screenshot(path='/home/user/pero-mobile-top.png')
        await mobile.get_by_role('button', name='Открыть меню').click()
        assert await mobile.locator('.mobile-nav').is_visible()
        await mobile.locator('.mobile-nav a[href="#factions"]').click()
        assert await mobile.locator('.mobile-nav').count() == 0
        await mobile.get_by_role('tab', name='Тролли', exact=False).click()
        assert 'возрождения' in await mobile.locator('#faction-panel').inner_text()
        await mobile.locator('#factions').screenshot(path='/home/user/pero-mobile-factions.png')
        await mobile.locator('#order').scroll_into_view_if_needed()
        await mobile.screenshot(path='/home/user/pero-mobile-order.png')
        await mobile.get_by_role('link', name='Вернуться наверх страницы', exact=True).click()
        assert await mobile.evaluate('window.scrollY') == 0
        assert await mobile.evaluate('document.documentElement.scrollWidth <= innerWidth')
        await mobile.set_viewport_size({'width': 320, 'height': 740})
        assert await mobile.evaluate('document.documentElement.scrollWidth <= innerWidth')
        await mobile.set_viewport_size({'width': 768, 'height': 1024})
        assert await mobile.evaluate('document.documentElement.scrollWidth <= innerWidth')
        print(json.dumps({'desktop': 'passed', 'mobile': 'passed', 'images': 'all loaded', 'consoleErrors': errors, 'order': 'mailto draft verified; no email sent'}, ensure_ascii=False))
        await browser.close()

asyncio.run(main())