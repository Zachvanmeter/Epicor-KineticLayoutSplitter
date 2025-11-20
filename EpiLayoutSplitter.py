from sys import exit

import json
from bs4 import BeautifulSoup


def GenLegibleLayoutFile(PathToLayout):

	# We need to convert the unformatted <> characters for beautiful soup
	#  The .clean file can be discarded, or combed through. It cant be 
	#  imported which is why we need to use the Recode Function later
	
	with open(PathToLayout,'r') as f:
		lines = f.read().split('\n')

	OutputFile = PathToLayout+'.clean'
	
	with open(OutputFile,'w') as f:
		for line in lines:
			line = line.replace('&lt;','<')
			line = line.replace('&gt;','>')
			f.write(line+'\n')
	
	return OutputFile

def GenSoup(url):
	with open(url, 'r', encoding='utf-8') as f:
		return BeautifulSoup(f.read(),'xml')
	
def Recode(s):
	return str(s).replace('<','&lt;').replace('>','&gt;')

###########################
#### Parsing Fucntions ####

def GenHeaderDict(soup):	
	TagType = 'ShellLayout'
	for tag in soup.find_all(TagType):
		HeaderDict = \
		{
			'ShellLayoutDataSet':	'<ShellLayoutDataSet xmlns="http://www.epicor.com/Ice/300/BO/ShellLayout/ShellLayout">',
			'ShellLayout':			'<ShellLayout>',
			'TenantID':				tag.TenantID,
			'LayoutID':				tag.LayoutID,
			'AuthorID':				tag.AuthorID,
			'DateModified':			tag.DateModified,
			'SysRevID':				'<SysRevID>0</SysRevID>',
			'SysRowID':				'<SysRowID>00000000-0000-0000-0000-000000000000</SysRowID>',
			'Published':			tag.Published,
			'HomePageType':			tag.HomePageType,
			'SubType':				tag.SubType,
			'LayoutDescription':	tag.LayoutDescription,
			'IsHomeDefault':		tag.IsHomeDefault,
			'Version':				tag.Version,
			'BitFlag':				tag.BitFlag,
			'RowMod':				tag.RowMod,
			'ShellHomePage':		'<ShellHomePage>&lt;HomePageDataSet xmlns="http://www.epicor.com/Ice/300/BO/ShellLayout/HomePage"&gt;',
		}
	return HeaderDict

def GenFooterList():
	FooterList = \
	[
		'&lt;LayoutInfo&gt;',
		'&lt;IsDefaultLayout&gt;false&lt;/IsDefaultLayout&gt;',
		'&lt;LayoutID /&gt;',
		'&lt;SysRowID&gt;00000000-0000-0000-0000-000000000000&lt;/SysRowID&gt;',
		'&lt;RowMod&gt;A&lt;/RowMod&gt;',
		'&lt;/LayoutInfo&gt;',
		'&lt;/HomePageDataSet&gt;</ShellHomePage>',
	]
	return FooterList
		
def GenSubFooterList():
	SubFooterList = \
	[
		'</ShellLayout>',
		'</ShellLayoutDataSet>',
	]
	return SubFooterList

def GenLayoutTabDict(soup, AlwaysIncludedList):
	LayoutTabDict = {}
	TagType = 'HomeTileGroup'
	Resequence = 0
	for mybool in [False, True]:
		for tag in soup.find_all(TagType):
			GroupID = tag.GroupID.text
			if (GroupID in AlwaysIncludedList) == mybool:
				print(tag.Title.text)
			
				# When groups are in the always included tab, I dont want them to appear to the left of
				#  the primary layouts that our users might have
				
				WebPropertyDict = json.loads(tag.WebProperties.text)
				WebPropertyDict['sequence'] = str(Resequence)
				
				LayoutTabDict[GroupID] = \
				{
					'GroupID':				tag.GroupID,
					'Title':				tag.Title,
					'IsFaveDefault':		tag.IsFaveDefault,
					'Sequence':				tag.Sequence,
					'WebProperties':		'<WebProperties>'+json.dumps(WebPropertyDict)+'</WebProperties>',
					'Type':					tag.Type,
					'Retain':				tag.Retain,
					'SysRowID':				tag.SysRowID,
					'RowMod':				tag.RowMod,
					'HomeTileList':			[]
				}
				Resequence += 1
	return LayoutTabDict

def AddHomeTiles(soup, LayoutTabDict):
	TagType = 'HomeTile'
	for tag in soup.find_all(TagType):
		GroupID = tag.GroupID.text
		
		d = \
		{
			'TileID':				tag.TileID,
			'GroupID':				tag.GroupID,
			'Type':					tag.Type,
			'Path':					tag.Path,
			'LinkType':				tag.LinkType,
			'DisplayType':			tag.DisplayType,
			'DisplayPath':			tag.DisplayPath,
			'LineLinkType':			tag.LineLinkType,
			'LinePath':				tag.LinePath,
			'BaqId':				tag.BaqId,
			'Color':				tag.Color,
			'Title':				tag.Title,
			'DefaultWidth':			tag.DefaultWidth,
			'DefaultHeight':		tag.DefaultHeight,
			'MaxWidth':				tag.MaxWidth,
			'MaxHeight':			tag.MaxHeight,
			'ListImage':			tag.ListImage,
			'FavoriteFolderSeq':	tag.FavoriteFolderSeq,
			'ExpandedFlag':			tag.ExpandedFlag,
			'BaqColumnList':		tag.BaqColumnList,
			'Sequence':				tag.Sequence,
			'RelatedMenuId':		tag.RelatedMenuId,
			'RefreshInterval':		tag.RefreshInterval,
			'Company':				tag.Company,
			'Appserver':			tag.Appserver,
			'BaqContextColumn':		tag.BaqContextColumn,
			'Plant':				tag.Plant,
			'MetricAggregate':		tag.MetricAggregate,
			'MetricTextPrefix':		tag.MetricTextPrefix,
			'MetricTextSuffix':		tag.MetricTextSuffix,
			'MetricImage':			tag.MetricImage,
			'MetricTextFontSize':	tag.MetricTextFontSize,
			'ImageRowID':			tag.ImageRowID,
			'ImageBlob':			tag.ImageBlob,
			'ImageFilename':		tag.ImageFilename,
			'WebProperties':		tag.WebProperties,
			'OpenInNewTab':			tag.OpenInNewTab,
			'SysRowID':				tag.SysRowID,
			'RowMod':				tag.RowMod,
		}
		LayoutTabDict[GroupID]['HomeTileList'].append(d)
	return LayoutTabDict

def GenUserOptionsDict(soup):
	UserOptionsDict = {}
	TagType = 'UserOptionsDataSet'
	for tag in soup.find_all(TagType):
		UserOptionsDict = \
		{
			'tag':tag
		}
	return UserOptionsDict

	
def Main(PathToLayout, AlwaysIncludedList):
	OutputFile = GenLegibleLayoutFile(PathToLayout)
	soup = GenSoup(OutputFile)
	HeaderDict = GenHeaderDict(soup)
	FooterList = GenFooterList()
	SubFooterList = GenSubFooterList()
	LayoutTabDict = GenLayoutTabDict(soup, AlwaysIncludedList)
	LayoutTabDict = AddHomeTiles(soup, LayoutTabDict)
	UserOptionsDict = GenUserOptionsDict(soup)
	
	# This is where we actually create the files. One day, I'd like to wrap this function in a
	#  GUI so it could load up all of the tabs and add them to the AlwaysIncludedList based on 
	#  some kind of user selection. Whenever I do that, I'll also refactor this code so we 
	#  arent repeating the 'always included' hometiles and group iterators.
	
	for GroupID in LayoutTabDict:
		Title = LayoutTabDict[GroupID]['Title'].text
		print('LayoutTab Title:', Title, 'GroupID:', GroupID)
		with open(Title+'.layout', 'w') as f:
			
			
			# First we output the Header Info, which is a hybrid of actual and static data
			for k,v in HeaderDict.items():
				f.write(str(v)+'\n')
			
			# We grab one tab per layout
			f.write(Recode('<HomeTileGroup>\n'))
			for k in LayoutTabDict[GroupID]:
				if k not in ['HomeTileList']:
					f.write(Recode(LayoutTabDict[GroupID][k])+'\n')
			f.write(Recode('</HomeTileGroup>\n'))
			
			
			# The Alwasys Included tabs have already resequenced in GenLayoutTabDict
			if AlwaysIncludedList != [] and GroupID not in AlwaysIncludedList:
				for sparetabGroupID in AlwaysIncludedList:
					f.write(Recode('<HomeTileGroup>\n'))
					for k in LayoutTabDict[sparetabGroupID]:
						if k not in ['HomeTileList']:
							f.write(Recode(LayoutTabDict[sparetabGroupID][k])+'\n')
					f.write(Recode('</HomeTileGroup>\n'))
			
			
			# Add the individual Buttons, BAQs, links and more
			for d in LayoutTabDict[GroupID]['HomeTileList']:
				print('\t',d['Title'].text)
				f.write(Recode('<HomeTile>\n'))
				for k in d:
					f.write(Recode(d[k])+'\n')
				f.write(Recode('</HomeTile>\n'))
				
			
			# Add the individual Buttons, BAQs, links and more
			if AlwaysIncludedList != [] and GroupID not in AlwaysIncludedList:
				for sparetabGroupID in AlwaysIncludedList:
					for d in LayoutTabDict[sparetabGroupID]['HomeTileList']:
						print('\t',d['Title'].text)
						f.write(Recode('<HomeTile>\n'))
						for k in d:
							f.write(Recode(d[k])+'\n')
						f.write(Recode('</HomeTile>\n'))
			
			
			# We have to break the footer into bits. 
			for line in FooterList:
				f.write(line+'\n')
			
			
			# This is likely not something that we will need to change import to import, it mainly relates
			#  to classic colors and such
			f.write('<ShellUserOptions>'+'\n')
			f.write(Recode(UserOptionsDict['tag'])+'\n')
			f.write('</ShellUserOptions>'+'\n')
			
			
			# We have to break the footer into bits. 
			for line in SubFooterList:
				f.write(line+'\n')	
	
	print('Process Complete.')
	
if __name__ == '__main__':
	# The saved file of your "all screen" or multi layout save
	PathToLayout = 'ALL_SCREEN.layout'
	if PathToLayout == '':
		print('Heyo, you cant just run this script, you need to edit the PathToLayout variable by'
				+'opening this script in a text editor like notepad++')
		print('Press enter to close...')
		input()
		exit()
	
	# This is all of the GroupIDs that you want included on the sub-layouts
	AlwaysIncludedList = ['37','46']
	
	Main(PathToLayout, AlwaysIncludedList)

