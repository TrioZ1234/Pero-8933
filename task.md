## Task
Build approved Russian landing page for Перо Измерений using v2 images, v3 text, trioz.ru reference. Recipient sales@trioz.ru.

## Decisions
- Managed React/Vite/Hono app, web only.
- No email credentials supplied; mailto draft fallback, clear visitor-facing copy. Automatic email prepared for later configuration.
- Keep correct v3 army composition: 8 ordinary shields, 3 sword guards.

## Progress
- [x] Research attachments and official reference; plan approved
- [x] Initialize app and document design
- [x] Extract images and content; implement landing and API
- [x] Build and lint, desktop/mobile browser verification
- [ ] Deliver running website

## Verification
`bun run build` and `bun run lint` passed. Browser tests passed: map/rules dialogs, Escape/focus, faction selection, combat card flips, gods accordion, mobile navigation, form validation and mailto draft. No emails sent. All images loaded, no console errors, no horizontal overflow at 1440/390/320/768px. API health returns ok. Web server running on assigned port 4200 in tmux pero-web.

## Remaining configuration
Automatic email needs RESEND_API_KEY and ORDER_EMAIL_FROM on verified domain. Current visitor flow clearly opens a mail draft; does not claim an order is sent or stored.