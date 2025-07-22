# Munich Self Checkout Kassen (SB Kassen) Finder Webapp

*Wo gibt es REWE SB Kassen?*

⚠️ Webapp is currently offline!

Discover shops with self checkout near you!

![snippet](https://github.com/yinyingip/sb-kassen-app/blob/main/snippet_with_shops.png)

## Technologies
```mermaid
flowchart TD
    GM[Shop info on Google Map] -->|Scraping data using Selenium|A(PostgreSQL Database)
    A -->B(FastAPI Backend)
    B --> C[Streamlit Frontend]
```
