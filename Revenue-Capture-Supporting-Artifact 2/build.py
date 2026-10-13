from pathlib import Path
import base64

root = Path(__file__).resolve().parent
src = root / 'src'
html = (src / 'index.html').read_text()
html = html.replace('<link rel="stylesheet" href="style.css">', '<style>' + (src / 'style.css').read_text() + '</style>')
html = html.replace('<script defer src="app.js"></script>', '')
html = html.replace('</body>', '<script>' + (src / 'app.js').read_text() + '</script></body>')
logo = base64.b64encode((src / 'assets/razorpay-logo.svg').read_bytes()).decode()
html = html.replace('assets/razorpay-logo.svg', 'data:image/svg+xml;base64,' + logo)
(root / 'Revenue Capture.html').write_text(html)
print('Built Revenue Capture.html')
