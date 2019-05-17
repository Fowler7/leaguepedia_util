from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'Fix team gold & player gold if missed before'  # Set summary

limit = -1
# startat_page = 'asdf'
this_template = site.pages['Template:Scoreboard/Player']  # Set template
pages = this_template.embeddedin()

pages_var = list(pages)

pages_array = [p.name for p in pages_var]

try:
	startat = pages_array.index(startat_page)
except NameError as e:
	startat = -1
except ValueError as e:
	startat = -1
print(startat)

def fixGold(template, param):
	param = param if param else 'gold'
	if template.has(param):
		gold = template.get(param).value.strip()
		if gold != '':
			goldInt = float(gold)
			if (param == 'gold' and goldInt < 500) or goldInt < 1000:
				actualGold = int(goldInt * 1000)
				template.add(param, str(actualGold))

lmt = 0
for page in pages_var:
	if lmt == limit:
		break
	lmt += 1
	if lmt < startat:
		print("Skipping page %s" % page.name)
	else:
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		for template in wikitext.filter_templates():
			name = template.name.strip()
			if 'Scoreboard/Season' in name:
				fixGold(template, 'team1g')
				fixGold(template, 'team2g')
			elif name == 'Scoreboard/Player':
				fixGold(template, False)
				
		
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)