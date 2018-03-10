#!/usr/bin/env python

import json, os

# Set up some variables to make life a bit easier. 

web_root = '/home3/neg501/public_html/ugly_roster'
web_root = '~/stormtrooperguy/Code/501neg'

rostercache = "./roster.json"
categories = "%s/categories.html" % (web_root)
welcome = "%s/staff.html" % (web_root)

# Load up the JSON file with the roster data. It is assumed that this is being updated via a cron job somewhere. 
# we could pull it every time if we wanted to, but I'm trying to be merciful. 

try:
  with open(rostercache) as jh:
    roster = json.load(jh)
except:
    print('Clever failed to load message here')


# Assign pretty names to costume categories. Someday this could be a feed from the Legion

cat_names = {
  'TK': 'Stormtrooper',
  'TI': 'TIE Pilot',
  'BH': 'Bounty Hunter',
  'TS': 'Snowtrooper',
  'DZ': 'Denizens of the Empire',
  'DS': 'Dark Side Adept',
  'TX': 'Special Operations',
  'TR': 'Royal Guards',
  'TD': 'Sandtroopers',
  'TB': 'Scout Troopers',
  'TC': 'Clone Troopers (EP II)',
  'TA': 'AT-AT Drivers',
  'CC': 'Clone Commanders',
  'CB': 'Kashyyk Troopers',
  'IS': 'AT-ST Drivers',
  'RC': 'Republic Commandos',
  'IN': 'Imperial Navy',
  'GM': 'Galactic Marines',
  'ID': 'Imperial Officer',
  'IG': 'Imperial Gunner',
  'CT': 'Clone Trooper (EP III)',
  'ST': 'Shoretroopers', 
  'SL': 'Sith Lords',
  'IC': 'Imperial Crew'
}

# Placeholders
cat_members = {}
member_data = {}


# First we write out the intro page for the roster. This is what you see when you first load the page. 

with open(welcome, 'w') as wh:

  wh.write("<h1>NEG Roster</h1>\n")
  wh.write("<p>The NEG has %s active members across Maine, New Hampshire, Vermont, Massachusetts and Rhode Island.</p>" % (roster['unit']['unitSize']))
  wh.write("<p>The NEG command staff this term is:</p>")

  wh.write("<table>\n")

  for officer in roster['unit']['officers']:
    wh.write("<tr>\n")

    wh.write("<td><img src='%s'></td>\n" % officer['primaryThumbnail'])
    wh.write("<td>\n")

    wh.write("<a href='%s.html'>%s</a><br />\n" % (officer['legionId'], officer['fullName']) )
    wh.write("%s (%s)<br />\n" % (officer['officeAcronym'], officer['office']))
    wh.write(" <br />\n")

    wh.write("</td>")

    wh.write("</tr>\n")

  wh.write("</table>\n")

# Now loop over the members. We are going to dissect the JSON data and store the bits we need in some dicts that are easy to loop over. 

for member in roster['unit']['members']:

  # The current format of legionId includes a text prefix. Remove it
  legion_id = str(member['legionId'].split(';')[1])

  # This is our "main data" for each person...
  member_data[legion_id] = {
    'name': member['fullName'],
    'thumbnail': member['thumbnail'],
    'legionid': legion_id
  }

  # Go through all of the costumes. Build a list of which costumes we actually have in the garrison. 
  for costume in member['costumes']:

    if costume['prefix'] in cat_members:
      if not legion_id in cat_members[costume['prefix']]:
        cat_members[costume['prefix']].append(legion_id)
    else:
      cat_members[costume['prefix']] = [ legion_id ]

  # Each person gets a flat HTML file. Seems pretty bland but it's all that we need really. 
  profile_file = "%s/members/%s.html" % (web_root, legion_id)

  # Ugly table is ugly. I don't know CSS. Get off my lawn!!!
  with open(profile_file, 'w') as ph:
    ph.write("<table>\n")
    ph.write("<tr>\n")
    ph.write("<td><img src='%s'><br />\n</td>\n" % (member['thumbnail']))
    ph.write("<td>")
    ph.write("Name: %s<br />\n" % (member['fullName']))
    ph.write("LegionId: %s<br />\n" % (legion_id))
    ph.write("Legion Profile: <a href='%s' target=_new>501st.com profile</a><br />\n" % (member['link']))
    ph.write("</td>")
    ph.write("</tr>")
    ph.write("</table>")
    ph.write("Costumes:<br/>\n\n")

    td_count = 0

    ph.write("<table>")

    for costume in member['costumes']:

      if td_count == 0:
        ph.write("<tr>")

      ph.write("<td>")
      ph.write("%s<br />\n" % (costume['costumeName']))
      ph.write("<img src='%s'><br />\n" % (costume['thumbnail']))
      ph.write("</td>")

      td_count += 1

      if td_count == 4:
        ph.write("</tr>")
        td_count = 0

    ph.write("</table>")

# Build the categories index. 

with open(categories, 'w') as cats_h:

  cats_h.write("<a href='staff.html' target='main'>Staff Directory</a><br />\n")
  cats_h.write("&nbsp<br />\n")

  for cat,members in cat_members.items():

    # Since our list of category names is internally maintained it is bound to get out of date. Handle it as gracefully as possible 
    # given what we have to work with. 
    if cat in cat_names:
      cat_title = cat_names[cat]
    else:
      cat_title = "%s Costumes" % (cat)

    # Write out links to eah of the gategories, and to the home/staff page. 

    cats_h.write("<a href='%s.html' target='main'>%s</a><br />\n" % (cat, cat_title))

    catlist_file = "%s/%s.html" % (web_root, cat)

    with open(catlist_file, 'w') as catlist_h:

      catlist_h.write("<h1>%s</h1>\n" % (cat_title))

      for member in members:
        catlist_h.write("<a href='members/%s.html'>%s (%s-%s)</a><br />\n" % (member, member_data[member]['name'], cat, member_data[member]['legionid'], ))





