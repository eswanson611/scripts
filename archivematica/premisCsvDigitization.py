#!/usr/bin/env python

import os, csv, datetime

# get refid/find transfer directory
refid = raw_input('Enter the ArchivesSpace refid: ')
objects_directory = 'archivematica_sip_' + refid + '/objects/'
metadata_directory = 'archivematica_sip_' + refid + '/metadata/'
# filenames = os.listdir(objects_directory)
# print filenames

# GET COPYRIGHT BASIS INFO

# copyright status
def getCopyrightStatus():
    copyright_status_input = raw_input('Copyrighted? (y/n/u): ')
        if copyright_status_input.lower() == 'y' or copyright_status_input.lower() == 'yes':
            copyright_status = 'copyrighted'
        elif copyright_status_input.lower() == 'n' or copyright_status_input.lower() == 'no':
            copyright_status = 'publicdomain'
        elif copyright_status_input.lower() == 'u' or copyright_status_input.lower() == 'unknown':
            copyright_status = 'unknown'
        else:
            copyright_status = '???'
        return copyright_status

#copyright determination date
def getCopyrightDeterminationDate():
    now = datetime.datetime.now()
    copyright_determination = now.strftime("%Y-%m-%d")
    return copyright_determination

# copyright applicable start date
def getCopyrightStartDate():
    global copyright_start_year
    copyright_start_year = raw_input("Copyright start year (YYYY): ")
    copyright_start_month = raw_input("Copyright start month (MM): ")
    copyright_start_day = raw_input("Copyright start day (DD): ")
    copyright_start_date = copyright_start_year + "-" + copyright_start_month + "-" + copyright_start_day
    return copyright_start_date

# copyright applicable end date
def getCopyrightEndDate():
    copyright_term = raw_input("Copyright term length (years): ")
    copyright_end_year = int(copyright_start_year) + int(copyright_term)
    copyright_end_year = int(copyright_start_year) + 120
    copyright_end_date = str(copyright_end_year) + "-01-01"
    return copyright_end_date

# GET DONOR BASIS INFO


# ACT INFO
# get permission/restriction on the act
def getRestriction():
    restriction_input = raw_input("allow, conditional, or disallow (a,c,d)")
    if restriction_input.lower() == 'a' or restriction_input.lower() == 'allow':
        restriction = 'allow'
    elif restriction_input.lower() == 'c' or restriction_input.lower() == 'conditional':
        restriction = 'conditional'
    elif restriction_input.lower() == 'd' or restriction_input.lower() == 'disallow':
        restriction = 'disallow'
    else:
        print("invalid")
        getCopyrightRestriction()
    return restriction

# find and store all objects

#file	basis	status	determination_date	jurisdiction	start_date	end_date	terms	citation	note	grant_act	grant_restriction	grant_start_date	grant_end_date	grant_note	doc_id_type	doc_id_value	doc_id_role

def makeRow(filename,basis,status,determination_date,jurisdiction,start_date,end_date,note,grant_act,grant_restriction,grant_start_date,grant_end_date,grant_note):
    row = []
    row.append(filename)
    row.append(basis)
    row.append(status)
    row.append(determination_date)
    row.append(jurisdiction)
    row.append(start_date)
    row.append(end_date)
    row.append('') #terms
    row.append('') #citation   
    row.append(note)    
    row.append(grant_act)    
    row.append(grant_restriction)    
    row.append(grant_start_date)    
    row.append(grant_end_date)  
    row.append(grant_note)
    row.append('') #doc_id_type
    row.append('') #doc_id_value
    row.append('')  #doc_id_role
    writer.writerow(row)

def makeCopyrightRow(filename):
    filename = "objects/" + filename
    basis = 'copyright'
    status = getCopyrightStatus()
    determination_date = getCopyrightDeterminationDate()
    jurisdiction = 'us'
    start_date = getCopyrightStartDate()
    end_date =  getCopyrightEndDate()
    note = 'This Item is protected by copyright and/or related rights. You are free to use this Item in any way that is permitted by the copyright and related rights legislation that applies to your use. For other uses you need to obtain permission from the rights-holder(s).'
    grant_act = 'publish'
    print(grant_act)
    grant_restriction = getRestriction()
    grant_start_date = '2018-06-01'
    grant_end_date = 'open'
    grant_note = ''
    makeRow(filename,basis,status,determination_date,jurisdiction,start_date,end_date,note,grant_act,grant_restriction,grant_start_date,grant_end_date,grant_note)


def makeDonorRow(filename):
    basis = 'donor'
    status = ''
    determination_date = ''
    jurisdiction = ''
    start_date = '???'
    end_date = '???'
    note = '???'
    grant_act = 'disseminate'
    grant_restriction = '???'
    grant_start_date = '???'
    grant_end_date = '???'
    grant_note = '???'
    makeRow(filename,basis,status,determination_date,jurisdiction,start_date,end_date,note,grant_act,grant_restriction,grant_start_date,grant_end_date,grant_note)

#for each object, write copyright and donor rows


print 'Creating a csv'
#os.chdir(metadata_directory)
spreadsheet = 'rights.csv'
writer = csv.writer(open(spreadsheet, 'w'))
column_headings = ["file","basis","status","determination_date","jurisdiction","start_date","end_date","terms","citation","note","grant_act","grant_restriction","grant_start_date","grant_end_date","grant_note","doc_id_type","doc_id_value","doc_id_role"]
print column_headings
writer.writerow(column_headings)
#for f in filenames:
#    makeCopyrightRow(f)
#    makeDonorRow(f)
#print 'Done!'