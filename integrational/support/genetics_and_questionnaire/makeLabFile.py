import csv
import psycopg2

rs_chr = {}
rs_pos = {}
rs_snpindex = {}
rs_change = {}
snpindex = 1
with open("artificial_dict.txt", 'r') as f:
	reader=csv.reader(f,delimiter='\t')
	for row in reader:
		rs_chr[row[7]] = row[5]
		rs_pos[row[7]] = row[6]
		rs_snpindex[row[7]] = snpindex
		snpindex = snpindex + 1
		if row[3] == '-':
			rs_change[row[7]] = '[I/D]'
		elif row[4] == '-':
			rs_change[row[7]] = '[D/I]'
		else:
			rs_change[row[7]] = '[' + row[3] + '/' + row[4] + ']'

files = ['_female_1.input.rsid.txt', '_male_1.input.rsid.txt', '_male_2.input.rsid.txt']




#barcode = 10000000
sample_index = 1
for f in files:
	with open('result.txt', 'a') as res:
		with open(f, 'r') as ff:
			writer = csv.writer(res, delimiter='\t')
			next(ff)
			reader=csv.reader(ff,delimiter='\t')
			
			for row in reader:
				if row[0] in rs_chr.keys():
					#bar = str(barcode)[0:4] + '-' + str(barcode)[4:9]
					if ('_male_' in f and rs_chr[row[0]] == 'X') or rs_chr[row[0]] == 'Y' or rs_chr[row[0]] == 'MT':

						if (rs_change[row[0]] == '[I/D]' or rs_change[row[0]] == '[D/I]') and row[1] == '-':
							row[1] = 'D'
						elif (rs_change[row[0]] == '[I/D]' or rs_change[row[0]] == '[D/I]') and row[1] != '-':
							row[1] = 'I'

						writer.writerow([row[0], f, row[1], row[1], '-', '-', '-', '-', row[1], row[1], row[1], row[1], row[1], row[1], '-', '-', rs_chr[row[0]], rs_pos[row[0]], '-', '-', rs_change[row[0]], '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'])
					else:
						if (rs_change[row[0]] == '[I/D]' or rs_change[row[0]] == '[D/I]') and row[1] == '-':
							row[1] = 'D'
						elif (rs_change[row[0]] == '[I/D]' or rs_change[row[0]] == '[D/I]') and row[1] != '-':
							row[1] = 'I'

						if (rs_change[row[0]] == '[I/D]' or rs_change[row[0]] == '[D/I]') and row[2] == '-':
							row[2] = 'D'
						elif (rs_change[row[0]] == '[I/D]' or rs_change[row[0]] == '[D/I]') and row[2] != '-':
							row[2] = 'I'


						writer.writerow([row[0], f, row[1], row[2], '-', '-', '-', '-', row[1], row[1], row[1], row[1], row[1], row[1], '-', '-', rs_chr[row[0]], rs_pos[row[0]], '-', '-', rs_change[row[0]],  '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'])

	#barcode = barcode + 1


