from wp_post import wp_post
import os
from pydocx import PyDocX

#grab the most recent Word doc from current directory
files = sorted(filter(os.path.isfile, os.listdir('.')), key=os.path.getmtime, reverse=True)
for file_itter in files:
	if '.docx' in file_itter:
		file = file_itter
		break

#convert to HTML using PyDocX
html = PyDocX.to_html(file)
post_content=html[html.find('<p>'):html.find('</body>')]

## Post to WP Site
tga_passwd = os.environ.get('TGA_ATA_pass')
username = 'xxx'

tga = wp_post('https://www.thegoldanalyst.com/wp-admin/', username, tga_passwd)
tga.alt_text = 'Gold'
tga.create_post(title='test',
		contents=post_content,
		#excerpt='sample excerpt',
		category='News',
		tags= ['News', 'Metals']
		#ft_img = '\\Pictures\\gold.PNG'
		)