# MICRO_500 shadowanalyse — 21 juli 2026

## Samenvatting

De eerste volledige 120-cyclirun was technisch stabiel, maar economisch niet
winstgevend. Orion voltooide twee Amerikaanse round-trips. De gerapporteerde
cashstijging van EUR 0,54 was bruto; na EUR 2,39 geraamde round-tripkosten was
het gezamenlijke resultaat EUR -1,86 en de correcte eindcash EUR 498,14.

| Symbool | Bruto P/L | Kosten | Netto P/L | Exit |
| --- | ---: | ---: | ---: | --- |
| DIS | EUR -0,85 | EUR 1,21 | EUR -2,06 | 90-minuten tijdstop |
| QCOM | EUR 1,38 | EUR 1,18 | EUR 0,20 | 90-minuten tijdstop |

Beide entries hadden een geldige BUY-thesis en passeerden RiskManager. Het
verlies ontstond dus niet door een technische fout in de entry- of risicogate,
maar door één normale verliezende koersbeweging, hoge vaste kosten ten opzichte
van kleine posities en een nettowinstdoel dat binnen 90 minuten zelden haalbaar
was.

## Haalbaarheid van het oude winstdoel

De analyse gebruikte de lokaal opgeslagen vijf handelsdagen 5-minutencandles.
Voor ieder geldig 90-minutenvenster is de maximaal gunstige koersbeweging
berekend. Dit leverde 15.000 Amerikaanse en 20.357 Europese vensters op.

Amerikaanse resultaten:

- mediane maximaal gunstige beweging: 0,363%;
- 90e percentiel: 1,306%;
- 2,20% bereikt: 3,13% van de vensters;
- 2,50% bereikt: 2,23% van de vensters.

Europese resultaten:

- mediane maximaal gunstige beweging: 0,314%;
- 90e percentiel: 0,998%;
- 2,00% bereikt: 1,40% van de vensters;
- 2,50% bereikt: 0,61% van de vensters.

Voor DIS en QCOM vereiste het oude nettodoel van EUR 2,50 na kosten ongeveer
2,2–2,5% bruto koerswinst. Dat lag ver boven de normale 90-minutenbeweging.
QCOM bereikte tijdens de positie op een voltooide 5-minutencandle wel ongeveer
EUR 0,54 geschatte nettowinst, maar wachtte op EUR 2,50 en sloot uiteindelijk
met EUR 0,20 netto. DIS was tijdens de volledige positie nooit netto positief;
zijn beste intrabarresultaat bleef circa EUR -1,53 na kosten.

## Openingsgedrag

Orion opende DIS en QCOM kort na de Amerikaanse opening. Dat is niet op basis
van deze dataset als fout aangemerkt. In 1.500 openingsvensters was de mediane
gunstige beweging 0,710% en eindigde 53,53% positief; latere vensters hadden
respectievelijk 0,337% en 43,84%. Er is daarom geen ongefundeerde openingspauze
toegevoegd.

## Doorgevoerde correcties

- Shadow round-tripkosten worden bij een volledige exit werkelijk van cash
  afgetrokken, niet alleen in het journal vermeld.
- MICRO_500-cash wordt bij starten deterministisch gereconcilieerd uit EUR 500
  startkapitaal, voltooide nettoresultaten en de kostbasis van open posities.
- De oude bruto peak equity is teruggezet naar de netto basis van EUR 500,
  zodat toekomstige drawdown niet tegen een fictieve brutowinst wordt gemeten.
- Alle nieuwe trade-journaltimestamps zijn UTC-aware.
- De bestaande state en 6.317 historische timestamps zijn gemigreerd; de twee
  houdtijden zijn hersteld naar circa 91 minuten.
- Het netto micro-winstdoel is EUR 0,50 voor VS en EU.
- De economische entrygate accepteert maximaal 1,6% vereiste brutobeweging,
  inclusief kosten, nettodoel en EUR 0,50 onzekerheidsbuffer.

De strengere haalbaarheidsgate betekent dat Europese micro-entries bij de
huidige minimumcommissies en positiegrootte meestal terecht worden afgewezen.
Dit is geen uitschakeling van Europese analyse: Orion blijft de markt meten en
kan alleen alloceren wanneer de volledige economie daadwerkelijk past.

## Niet geconcludeerd

Twee trades zijn onvoldoende om winstgevendheid, winrate of expectancy aan te
tonen. De verlieslimieten en 90-minuten tijdstop zijn daarom niet op deze ene
dag geoptimaliseerd. De aangepaste strategie moet meerdere weken afzonderlijke
shadowdata verzamelen. Beoordeling gebeurt uitsluitend op nettoresultaat na
alle kosten, niet op bruto cash of het aantal transacties.
