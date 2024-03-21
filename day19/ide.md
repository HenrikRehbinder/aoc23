Jag är på rätt spår med partitioneringen. Det som saknas är att ta den hela vägen.   
 -- Alla variabler ska delas in i områden av limits. Tricket är att använda olikhetsrelationerna och sedan låta (inre) limits vara ett område av bredd 1. Om x har limits 1, 1000, 2000, 4000 så blir områdena 
 1-999 (bredd 999), 1000-1000 (b 1), 1001-1999 (b 999), 2000-2000 (b 1), 2001-4000 (b 1999)
 Sen skapar man kartesisk produkt av alla områden, räknar ut dess 4d-volym och gör som jag gjorde med de inre områdena. De produkter som kommer av 4 st bredd 1-områden ska då få volym 1. 

 Tänk på: 
  - Kolla att det finns volym 1-områden. 
  - Rensa i limits (redan gjort)
  - Bra att visualisera i 2D (eller försöka i 3D ) om det blir problem 

21/3
 - det börjar bli jobbigt nu.
 - Iden ovan fungerar på testdata. Det tar bara otroligt lång tid
 - Datamängden blir för stor när man tar alla kombinationer. 
 - Jag utnyttjar ju inte A/R när jag konstruerar partitionen. Kanske måste jag göra det. 
 - Jag har testat att utgå ifrån R istället men det blir typ samma. 
 - limits verkar vara samma. 
 - Hur utnyttja detta? 
Måste städa kod, den är så stökig så nåt kan bli fel 
 - Om jag kodar koordinaterna som strängar kan jag utnyttja mängdalgebran. Är det bra? 
 - Har jag något ut av att använda union(A_i) = compl(inters(compl(A_i)))
 - Innan jag drar iväg måste jag minnas att så länge som jag utgår ifrån partitioneringen som den är gjord nu så får jag en ohanterbar loop Det är där problemet ligger.
 - Är det så att man ska på något sätt utnyttja dynp/rekursion här? Det finns ju tydliga avbrottskritrier som nås ganska snart. Kanske backa från R eller A? 
 - typ att man för alla avbrottskriterier backar tills man nått "in" och succesivt snävar ner mängden
 - eller så gör man så framåt. 
 - hursomhelst så hamnar man i en graf. det är ju så man brukar göra...

2024-03-22: 
Jag är fast...
Mina terminating-kedjor är inte rätt, det finns en del av dem som inte genererar A 
Jag har glömt regeln att det är det första uppfyllda villkoret i en kedja som
bestämmer vad som händer. Vet egentligen inte om det spelar roll. Men måste tänka på det. 
I mina limits så är det nog fel eftersom de baserar sig på 
felaktiga terminations. Det här kan vara bra om det ger färre limits. 
Det finns reddittrådar om att man ska göra som jag gör men jag undrar om de ens testat den koden. 
För mig tar det för lång tid helt enkelt. 

Jag har tänkt på att man skulle kunna bilda en intersektionsmatris och göra nån smart snitt/unionsalgebra
på den men jag fattar inte hur det ska göras. 