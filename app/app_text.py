intro_md_de = """
Willkommen beim **Münchener SB-Kassen Finder**, Ihrer Anlaufstelle für die Entdeckung von Geschäften mit SB-Kassen-Optionen in der ganzen Stadt!

Wir wissen, wie schwierig es sein kann, eine vollständige und aktuelle Liste von Geschäften zu finden, die SB-Kassen anbieten, insbesondere da die meisten vorhandenen Listen auf veralteten Community-Beiträgen basieren. Genau hier kommen wir ins Spiel! Unsere App bietet einen umfassenden Überblick, damit Sie schneller und smarter einkaufen können.

### So funktioniert die Web-App:
1. Wählen Sie eine Liste von Geschäften aus der Seitenleiste.
2. Zeichnen Sie einen Bereich auf der Karte.
3. Klicken Sie auf 'Auf Karte anzeigen'—und voilà! Markierungen für Geschäfte mit SB-Kassen erscheinen auf der Karte.

### So werden die Daten gesammelt:
Wir haben Bewertungen von Google Maps durchforstet, um Geschäfte mit Erwähnungen von SB-Kassen-Erfahrungen zu finden. Um die Genauigkeit sicherzustellen, führen wir sowohl automatische Texterkennung als auch eine manuelle Kontextprüfung durch, um Fehlalarme zu minimieren.

Die Daten wurden zuletzt am **25. Dezember 2024** aktualisiert. Während wir uns bemühen, sie aktuell zu halten, kann es dennoch sein, dass einige Geschäfte fehlen oder gelegentlich Fehler auftreten—bitte haben Sie Verständnis!

Wir hoffen, dass dieses Tool Ihr Einkaufserlebnis erleichtert. Viel Spaß beim Einkaufen! 🌟
"""

intro_md_en = """
Welcome to the **Munich Self-Checkout Finder**, your go-to web app for discovering shops with self-checkout options across the city!

We know how tricky it can be to find a complete and up-to-date list of shops offering self-checkout, especially since most lists out there rely on outdated community inputs. That’s where we come in! Our app provides a comprehensive overview, making it easier for you to shop faster and smarter.

### How the web app works:
1. Select a list of shops from the sidebar.
2. Draw an area on the map.
3. Click 'Show on Map'—and voilà! Markers for shops with self-checkout will appear on the map.

### How the data is collected:
We’ve scraped reviews from Google Maps to find stores with mentions of self-checkout experiences. To ensure accuracy, we run both automatic text detection and a manual context check to minimize any false alarms.

The data was last updated on **December 25, 2024**. While we’re committed to keeping it current, there may still be a few shops missing or occasional mismatches—please bear with us!

We hope this tool makes your shopping experience smoother. Happy shopping! 🌟
"""

popup_html_de = """
<h1>{}</h1><br>
<p>
Adresse: {}<br></p>
<p><b>{} Bewertung{}</b> erwähnte{} Erfahrungen mit SB-Kassen.<br> 
Die neueste Bewertung ist <b>{}</b>.<br></p>
<p><a href="{}" target="_blank">Gehe zu Google Maps</a>
</p>""".format

popup_html_en = """
<h1>{}</h1><br>
<p>
Address: {}<br></p>
<p><b>{} review{}</b> mentioned{} experiences related to self-checkout.<br> 
The latest review is <b>{}</b>.<br></p>
<p><a href="{}" target="_blank">Go to Google Map</a>
</p>""".format

app_text = {
    "de": {
        "title": "Münchener SB-Kassen Finder: Kluger einkaufen, nicht härter!",
        "intro_title": "Willkommen beim Münchener SB-Kassen Finder",
        "intro_md": intro_md_de,
        "help": "So funktioniert es",
        "selector": "Geschäfte wählen",
        "shops": "Geschäfte",
        "marker_choice": "Unify-Markierungen verwenden",
        "popup_html": popup_html_de,
        "popup_pl": "en",
        "popup_verb_tense": "n",
        "warning_no_shop_chosen": "Bitte wählen Sie mindestens ein Geschäft aus.",
        "warning_no_area": "Bitte zeichnen Sie einen Suchbereich.",
        "warning_multiple_area": "Bitte zeichnen Sie nur einen Bereich.",
        "warning_no_shop": "Bitte wählen Sie mindestens ein Geschäft aus.",
        "warning_not_200": "Etwas ist bei der Abfrage schiefgelaufen.",
        "warning_no_shop_found": "Kein Geschäft gefunden.",
        "show": "Auf Karte anzeigen",
        "clear": "Marker löschen",
    },
    "en": {
        "title": "Munich Self-Checkout Finder: Shop Smarter, Not Harder!",
        "intro_title": "Welcome to the Munich Self-Checkout Finder",
        "intro_md": intro_md_en,
        "help": "How it works",
        "selector": "Choose Shops",
        "shops": "Shops",
        "marker_choice": "Use Unify Markers",
        "popup_html": popup_html_en,
        "popup_pl": "s",
        "popup_verb_tense": "",
        "warning_no_shop_chosen": "Please select at least one shop.",
        "warning_no_area": "Please draw one searching area.",
        "warning_multiple_area": "Please draw only one area.",
        "warning_no_shop": "Please select at least one shop.",
        "warning_not_200": "Something went wrong when querying.",
        "warning_no_shop_found": "No shop found.",
        "show": "Show on Map",
        "clear": "Clear Markers",
    },
}

icon_html = """
<div style="width: 40px; height: 40px;">
    <img src="{}" width="40" height="40"/>
</div>
""".format
