import csv

illumina_rs = {}
rs_change_main = {}
rs_change_alt = {}
rs_chr = {}
with open('artificial_dict.txt', 'r') as f:
	reader = csv.reader(f, delimiter = '\t')
	for row in reader:
		illumina_rs[row[0]] = row[7]
		rs_change_main[row[0]] = row[3]
		rs_change_alt[row[0]] = row[4]
		rs_chr[row[0]] = row[5]


def writestr(row, illumina_rs, rs_change_main, rs_change_alt):
	with open(row[1] + '_splitbydict.txt', 'a') as f:
		writer = csv.writer(f, delimiter='\t')
		if row[0] in rs_change_main.keys() and rs_chr[row[0]] != 'Y' and rs_chr[row[0]] != 'MT' and (rs_chr[row[0]] != 'X' or 'female' in row[1]):
			if row[2] == 'D' and row[3] == 'D':
				if rs_change_alt[row[0]] == '-':
					writer.writerow([ illumina_rs[row[0]], rs_change_alt[row[0]], rs_change_alt[row[0]] ])
				elif rs_change_main[row[0]] == '-':
					writer.writerow([ illumina_rs[row[0]], rs_change_main[row[0]], rs_change_main[row[0]] ])
			elif row[2] == 'I' and row[3] == 'D':
				if rs_change_alt[row[0]] == '-':
					writer.writerow([ illumina_rs[row[0]], rs_change_main[row[0]], rs_change_alt[row[0]] ])
				elif rs_change_main[row[0]] == '-':
					writer.writerow([ illumina_rs[row[0]], rs_change_alt[row[0]], rs_change_main[row[0]] ])
			elif row[2] == 'D' and row[3] == 'I':
				if rs_change_alt[row[0]] == '-':
					writer.writerow([ illumina_rs[row[0]], rs_change_alt[row[0]], rs_change_main[row[0]] ])
				elif rs_change_main[row[0]] == '-':
					writer.writerow([ illumina_rs[row[0]], rs_change_main[row[0]], rs_change_alt[row[0]] ])
			elif row[2] == 'I' and row[3] == 'I':
				if rs_change_main[row[0]] == '-':
					writer.writerow([ illumina_rs[row[0]], rs_change_alt[row[0]], rs_change_alt[row[0]] ])
				elif rs_change_alt[row[0]]  == '-':
					writer.writerow([ illumina_rs[row[0]], rs_change_main[row[0]], rs_change_main[row[0]] ])
			else:
				if row[2] == rs_change_main[row[0]] or row[3] == rs_change_main[row[0]] or row[2] == rs_change_alt[row[0]] or row[3] == rs_change_alt[row[0]]:
					writer.writerow([ illumina_rs[row[0]], row[2], row[3] ])
		else:
			if row[2] == 'D' and row[3] == 'D':
				if rs_change_alt[row[0]] == '-':
					writer.writerow([ illumina_rs[row[0]], rs_change_alt[row[0]], '' ])
				elif rs_change_main[row[0]] == '-':
					writer.writerow([ illumina_rs[row[0]], rs_change_main[row[0]], '' ])
			elif row[2] == 'I' and row[3] == 'I':
				if rs_change_main[row[0]] == '-':
					writer.writerow([ illumina_rs[row[0]], rs_change_alt[row[0]], '' ])
				elif rs_change_alt[row[0]]  == '-':
					writer.writerow([ illumina_rs[row[0]], rs_change_main[row[0]], '' ])
			else:
				if row[2] == rs_change_main[row[0]] or row[3] == rs_change_main[row[0]] or row[2] == rs_change_alt[row[0]] or row[3] == rs_change_alt[row[0]]:
					writer.writerow([ illumina_rs[row[0]], row[2], '' ])


with open('raw_data.test.txt', 'r') as f:
	reader = csv.reader(f, delimiter = '\t')
	for row in reader:
		if len(row) > 20 and row[0] != 'SNP Name':
			writestr(row, illumina_rs, rs_change_main, rs_change_alt)
