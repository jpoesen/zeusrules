import yaml
import gdata.spreadsheet.service
import gdata.service
import gdata.spreadsheet

def main():
	stream = file('config.yaml', 'r')
	config = yaml.load(stream)

	client = gdata.spreadsheet.service.SpreadsheetsService()
	client.email 		= config['email']
	client.password = config['password']
	client.source 	= config['app_source']
	client.ProgrammaticLogin()

	DocKey = config['gdoc_key']
	DocWorkSheetId = 'od6' # defaults to 'od6', don't ask why.
	SourceDomain = 'http://www.mathsrevision.net'

	rows = client.GetListFeed(DocKey, DocWorkSheetId)

	# file opening (wraps the generated entries)
	ZeusRules = '## Zeus web server rewrite rules.' + "\n"
	ZeusRules += '## CAUTION: This file is generated automatically. Manual changes will be lost next time this file is regenerated.' + "\n"
	ZeusRules += "\n\n"
	ZeusRules += 'insensitive match IN:Host into $ with ^www\.mathsrevision\.net$ ' + "\n"
	ZeusRules += 'if matched ' + "\n"

	# generate entries

	for row in rows.entry:
		# remove the domain part from the url
		src = row.custom['source'].text.split(SourceDomain)[1]

		# escape the string (dots, question marks)
		src = src.replace('.', '\.')
		src = src.replace('?', '\?')

		dest = row.custom['destination'].text

		rule = "\n"
		rule += '  insensitive match URL into $ with ^{source}$' + "\n"
		rule += '  if matched ' + "\n"
		rule += '    set OUT:Location = {destination}' + "\n"
		rule += '    set OUT:Content-Type = text/html' + "\n"
		rule += '    set RESPONSE = 301' + "\n"
		rule += '    set BODY = Moved' + "\n"
		rule += '    goto END' + "\n"
		rule += '  endif' + "\n"

		ZeusRules += rule.format(source=src, destination=dest)

	# file closing
	ZeusRules += 'endif'

	# save to file
	outfile = file("rewrite.script", 'w')
	print >> outfile, ZeusRules
	outfile.close()

if __name__ == "__main__":
    main()
