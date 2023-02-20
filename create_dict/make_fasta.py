def make_fasta(config, rs1_file, rs2_file):
	illumina_rs = open(config['manifest'])
	reads1_38 = open(rs1_file, 'w')
	reads2_38 = open(rs2_file, 'w')

	for line in illumina_rs:
		line_sp = line.split(',')
		if len(line_sp) < 10 or 'IlmnID' in line:
			continue
		if 'I/D' in line:
			indel_length = len(line_sp[-2].split(']')[0].split('/')[-1])
		elif 'D/I' in line:
			indel_length = 0
		else:
			indel_length = 1
		chrom = line_sp[9]
		pos = line_sp[10]
		change = line_sp[-2].split('[')[1].split(']')[0]
		reads1_38.write('>' + line_sp[1] + '_' + change + '_' + str(indel_length) + '_' + pos + '_' + chrom + '\n')
		reads1_38.write((line_sp[-2].split('[')[0]).upper() + '\n')
		reads2_38.write('>' + line_sp[1] + '_' + change + '_' + str(indel_length) + '_' + pos + '_' + chrom + '\n')
		reads2_38.write((line_sp[-2].split(']')[1]).upper() + '\n')
	
	reads1_38.close()
	reads2_38.close()
	illumina_rs.close()