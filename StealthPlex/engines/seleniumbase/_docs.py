from StealthPlex.engines.docs import ENGINE_INFO, proxy_doc

SELENIUMBASE_GITHUB = ENGINE_INFO["seleniumbase"].github
CDP_DOCS = "https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/ReadMe.md"

SB_UC_CDP = """
UC + CDP Mode (recommended — not plain WebDriver):

    with fetch.SB(uc=True) as sb:
        sb.activate_cdp_mode(url)   # disconnects WebDriver; enables sb.cdp.*
        sb.cdp.click(selector)      # stealth CDP click
        sb.solve_captcha()          # CAPTCHA via CDP
        sb.get_page_source()        # works while disconnected (routes to CDP)

Pure CDP Mode (no WebDriver):

    sb = fetch.sb_cdp.Chrome(url)
    sb.solve_captcha()
    sb.driver.stop()
"""

PROXY_CLASS = f"""
seleniumbase — same API as ``import seleniumbase`` (UC Mode + CDP Mode, not plain Driver).

Primary: ``with fetch.SB(uc=True) as sb: sb.activate_cdp_mode(url)`` then ``sb.cdp.*`` / ``sb.solve_captcha()``.
Also: ``fetch.sb_cdp``, ``fetch.cdp_driver`` for Pure CDP Mode.

CDP docs: {CDP_DOCS}
Project: {SELENIUMBASE_GITHUB}
"""

CLIENT_SELENIUMBASE = proxy_doc("seleniumbase")
